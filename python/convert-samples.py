#!/usr/bin/env python3
"""
sample_processor.py

Recursively searches a root folder for .wav sample files (which follow a naming convention
that ends with _<Note>.wav, e.g. "snare_C4.wav"). For each “sample set” (files sharing the same base
name) the program:

  1. Copies the folder structure (and non‐wav files) from the input root to the output root.
  2. Processes the .wav files by converting them to 44.1 kHz, 16‑bit, mono audio (with high‐quality dithering).
  3. Extracts the pitch from each file name.
  4. Checks, given a note range (e.g. C1–F4) passed on the command line, which notes are missing.
  5. For each missing note, creates a new sample by pitch shifting from the nearest available sample.
  
Usage:
    python sample_processor.py INPUT_ROOT OUTPUT_ROOT NOTE_RANGE
Example:
    python sample_processor.py /path/to/input /path/to/output C1-F4
"""

import os
import re
import argparse
import shutil

import numpy as np
import librosa
import soundfile as sf

# === Note conversion helpers =====================================

def note_name_to_midi(note):
    """
    Convert a note name (e.g. "C4" or "C#4") to a MIDI number.
    Uses the convention that C4 is MIDI 60.
    """
    # mapping from note names to semitone numbers within an octave
    note_map = {'C': 0, 'C#': 1, 'D': 2, 'D#': 3,
                'E': 4, 'F': 5, 'F#': 6, 'G': 7,
                'G#': 8, 'A': 9, 'A#': 10, 'B': 11}
    # Allow for two or three character note names (e.g. "C4" or "C#4")
    if len(note) == 2:
        key = note[0].upper()
        octave = int(note[1])
    elif len(note) == 3:
        key = note[0:2].upper()
        octave = int(note[2])
    else:
        raise ValueError(f"Invalid note format: {note}")
    midi = (octave + 1) * 12 + note_map[key]
    return midi

def midi_to_note_name(midi):
    """
    Convert a MIDI note number to a note name string.
    Uses the convention that MIDI 60 is C4.
    """
    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F',
                  'F#', 'G', 'G#', 'A', 'A#', 'B']
    octave = midi // 12 - 1
    note = note_names[midi % 12]
    return f"{note}{octave}"

def parse_note_range(note_range_str):
    """
    Parse a note range string like "C1-F4" and return a list of MIDI numbers.
    """
    try:
        start_note, end_note = note_range_str.split('-')
        start_midi = note_name_to_midi(start_note.strip())
        end_midi = note_name_to_midi(end_note.strip())
    except Exception as e:
        raise ValueError(f"Could not parse note range '{note_range_str}': {e}")
    if start_midi > end_midi:
        raise ValueError("Invalid note range: start note is higher than end note.")
    return list(range(start_midi, end_midi + 1))

# === Audio processing functions ===================================

def load_audio(file_path):
    """
    Load an audio file using librosa.
    Force sample rate to 44100 Hz and mono conversion.
    """
    y, sr = librosa.load(file_path, sr=44100, mono=True)
    return y, sr

def pitch_shift(y, sr, semitones):
    """
    Pitch shift an audio signal by a number of semitones.
    """
    return librosa.effects.pitch_shift(y, sr, n_steps=semitones)

def process_audio(y, sr):
    """
    Process an audio array:
      - Apply high-quality dithering (TPDF dithering) before quantizing to 16-bit.
      - Clip the values to the valid range [-1, 1].
    The audio is assumed to be in float32 format with values in [-1, 1].
    """
    # For 16-bit PCM the smallest step is 1/32768.
    LSB = 1.0 / 32768
    # Generate two independent uniform noises in [-LSB/2, LSB/2] and sum them.
    dither = (np.random.uniform(-LSB/2, LSB/2, size=y.shape) +
              np.random.uniform(-LSB/2, LSB/2, size=y.shape))
    y_dithered = y + dither
    # Ensure no clipping
    y_dithered = np.clip(y_dithered, -1.0, 1.0)
    return y_dithered

def save_audio(y, sr, dst):
    """
    Save an audio array to a file in 16-bit PCM format.
    """
    sf.write(dst, y, sr, subtype='PCM_16')

def process_and_copy_file(src, dst):
    """
    Load a wav file, process it (resample, mono, dither), and write it out.
    """
    y, sr = load_audio(src)
    y_processed = process_audio(y, sr)
    save_audio(y_processed, sr, dst)

# === Directory traversal and sample-set processing =============

def process_directory(input_root, output_root, note_range_midi):
    """
    Walk the directory tree under input_root. For each directory:
      - Recreate the directory in output_root.
      - For non-wav files, copy them as-is.
      - For .wav files matching the naming convention (ending with _<Note>.wav)
        group them into a "sample set" by their base name (everything before the _<Note>).
      - Process each wav file so that it is 44.1 kHz, 16-bit, mono, and dithered.
      - Within each sample set, detect missing MIDI notes from the given note_range.
        For each missing note, find the nearest available sample and generate a new file by
        pitch shifting.
    """
    # Regular expression to detect file names ending with _<Note>.wav.
    # Example: "snare_C4.wav" or "kick_A#3.wav"
    pattern = re.compile(r'^(.*)_([A-G][#]?\d)\.wav$', re.IGNORECASE)

    for dirpath, dirnames, filenames in os.walk(input_root):
        # Compute the relative directory path and re-create it under the output root.
        rel_dir = os.path.relpath(dirpath, input_root)
        out_dir = os.path.join(output_root, rel_dir)
        os.makedirs(out_dir, exist_ok=True)

        # First, copy over any non-wav files.
        for fname in filenames:
            if not fname.lower().endswith('.wav'):
                src_file = os.path.join(dirpath, fname)
                dst_file = os.path.join(out_dir, fname)
                shutil.copy2(src_file, dst_file)

        # Group wav files by “sample set” (base name without the note part).
        sample_sets = {}
        # Also keep a list for wav files that do not match our naming pattern.
        non_matching_wavs = []
        for fname in filenames:
            if not fname.lower().endswith('.wav'):
                continue
            match = pattern.match(fname)
            if match:
                base_name = match.group(1)  # part before the final _<Note>
                note_str = match.group(2)
                try:
                    midi = note_name_to_midi(note_str)
                except Exception as e:
                    print(f"Warning: Could not parse note in filename '{fname}': {e}")
                    continue
                full_path = os.path.join(dirpath, fname)
                if base_name not in sample_sets:
                    sample_sets[base_name] = {}
                sample_sets[base_name][midi] = full_path
            else:
                # For wav files not matching the expected pattern, just process & copy.
                non_matching_wavs.append(fname)

        for fname in non_matching_wavs:
            src = os.path.join(dirpath, fname)
            dst = os.path.join(out_dir, fname)
            process_and_copy_file(src, dst)

        # Now process each sample set.
        for base, samples in sample_sets.items():
            # Determine which MIDI notes in the given range are missing.
            missing_midis = [m for m in note_range_midi if m not in samples]
            # Process and copy the original samples.
            for midi_val, src in samples.items():
                target_note = midi_to_note_name(midi_val)
                new_fname = f"{base}_{target_note}.wav"
                dst = os.path.join(out_dir, new_fname)
                process_and_copy_file(src, dst)
            # For each missing note, generate a new sample by pitch shifting
            # from the nearest available sample.
            for target_midi in missing_midis:
                # Find the available sample with the minimal semitone distance.
                nearest_midi = min(samples.keys(), key=lambda m: abs(m - target_midi))
                src = samples[nearest_midi]
                try:
                    y, sr = load_audio(src)
                except Exception as e:
                    print(f"Error loading '{src}': {e}")
                    continue
                semitones = target_midi - nearest_midi
                if semitones != 0:
                    try:
                        y_shifted = pitch_shift(y, sr, semitones)
                    except Exception as e:
                        print(f"Error pitch shifting '{src}': {e}")
                        continue
                else:
                    y_shifted = y
                y_processed = process_audio(y_shifted, sr)
                target_note = midi_to_note_name(target_midi)
                new_fname = f"{base}_{target_note}.wav"
                dst = os.path.join(out_dir, new_fname)
                save_audio(y_processed, sr, dst)
                print(f"Generated missing sample: {dst}")

# === Main ========================================================

def main():
    parser = argparse.ArgumentParser(
        description="Recursively process .wav sample files: copy folder structure, convert audio to 44.1 kHz/16-bit/mono with dithering, "
                    "and for each sample set (files named ..._<Note>.wav) generate missing notes via pitch shifting.")
    parser.add_argument("input_root", help="Input root directory to search for samples")
    parser.add_argument("output_root", help="Output root directory where processed samples will be written")
    parser.add_argument("note_range", help="Note range (e.g. 'C1-F4') to fill in missing notes")
    args = parser.parse_args()

    try:
        note_range_midi = parse_note_range(args.note_range)
    except Exception as e:
        print(f"Error parsing note range: {e}")
        return

    process_directory(args.input_root, args.output_root, note_range_midi)

if __name__ == "__main__":
    main()
