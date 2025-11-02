#!/usr/bin/env python3
"""
copyAndExtendSamples.py

Recursively searches a root folder for .wav sample files. For pitched instruments,
the file names are expected to follow a naming convention that ends with a note (e.g. 'piano_C4.wav').
For non‑pitched percussion instruments, no note is required.

For pitched instruments (when a note range is provided via --note-range), the program:
  1. Copies the folder structure (and non‑wav files) from the input root to the output roots.
  2. Processes the .wav files—applying pitch shifting via Rubberband when needed and preserving loop markers.
  3. Determines missing notes (within the provided range) and generates new samples from the nearest candidate.
  4. Writes the processed files to the primary output folder.
  5. Additionally, mirrors the entire structure in a second folder, converting every WAV file to monaural
     using high‑quality SoX conversion (with loop markers re‑embedded).

Usage examples:
  Pitched instruments:
      python copyAndExtendSamples.py INPUT_ROOT OUTPUT_ROOT MONO_OUTPUT_ROOT --note-range C1-F4 [--skip-existing]
  Non‑pitched instruments:
      python copyAndExtendSamples.py INPUT_ROOT OUTPUT_ROOT MONO_OUTPUT_ROOT [--skip-existing]
"""

import os                # For file system operations.
import re                # For regex matching of filenames.
import argparse          # For command‑line argument parsing.
import shutil            # For copying files.
import subprocess        # To call external tools (Rubberband and SoX).
import tempfile          # For temporary file creation.
import struct            # For binary data manipulation (WAV headers).

import numpy as np       # For numerical operations.
import soundfile as sf   # For reading and writing audio files.

# === Helper for safe printing =========================================
def safe_str(s):
    """Return a safe UTF‑8 version of s, replacing surrogates with the replacement character."""
    return s.encode('utf-8', 'replace').decode('utf-8')

# === Filename Sanitization =========================================
def sanitize_filename(name):
    """Replace surrogate characters with a hyphen."""
    return ''.join(c if not (0xD800 <= ord(c) <= 0xDFFF) else '-' for c in name)

def sanitize_directory(dirpath, filenames):
    """
    Rename any file in the directory if its name contains errant surrogate characters.
    
    If the sanitized name conflicts with an existing file, a numeric suffix is added.
    """
    new_names = {}
    for i, fname in enumerate(filenames):
        sanitized = sanitize_filename(fname)
        if sanitized != fname:
            orig_path = os.path.join(dirpath, fname)
            new_path = os.path.join(dirpath, sanitized)
            counter = 1
            base, ext = os.path.splitext(sanitized)
            while os.path.exists(new_path):
                new_path = os.path.join(dirpath, f"{base}_{counter}{ext}")
                counter += 1
            try:
                os.rename(orig_path, new_path)
                print(f"Renamed '{safe_str(orig_path)}' to '{safe_str(new_path)}' due to invalid characters.")
                new_names[fname] = os.path.basename(new_path)
                filenames[i] = os.path.basename(new_path)
            except Exception as e:
                print(f"Error renaming '{safe_str(orig_path)}': {e}")
    return filenames

# === MIDI Offset Filename Renaming Helper =========================
def modify_filename(filename, note_range_midi=None):
    """
    If the filename contains a MIDI offset in the form of <number>-(up|do)
    and a note immediately before the '.wav' extension, then compute a start-note by 
    applying the offset to the end-note. Insert the start-note and a hyphen before the end-note.
    
    Additionally, if a note_range_midi list is provided and the computed start-note 
    (as a MIDI number) is out of range, return None so that the file will be skipped.
    
    For example:
      "BP_02leg_p_8-up_E3.wav" -> "BP_02leg_p_8-up_G#2-E3.wav" 
      (assuming G#2 is within the note range).
      
    If no MIDI offset is found, returns the original filename.
    """
    midi_offset_pattern = re.compile(r'(\d+)-(up|do)')
    note_pattern = re.compile(r'([A-G]#?\d)(?=\.wav$)', re.IGNORECASE)
    note_match = note_pattern.search(filename)
    if not note_match:
        return filename
    end_note = note_match.group(1)
    offset_match = midi_offset_pattern.search(filename)
    if not offset_match:
        return filename
    number = int(offset_match.group(1))
    direction = offset_match.group(2)
    # "do" translates to a positive offset; "up" to a negative offset.
    offset = number if direction == 'do' else -number
    try:
        end_midi = note_name_to_midi(end_note)
    except Exception:
        return filename
    start_midi = end_midi + offset
    # If a note range is provided, skip the file if start_midi is out-of-range.
    if note_range_midi is not None:
        if start_midi < note_range_midi[0] or start_midi > note_range_midi[-1]:
            return None
    start_note = midi_to_note_name(start_midi)
    insertion_index = note_match.start()
    new_filename = filename[:insertion_index] + f"{start_note}-" + filename[insertion_index:]
    return new_filename

# === Helper for safe file reading =========================================
def safe_sf_read(file_path, dtype='float32'):
    """
    Encode the file path to handle surrogates and open the file in binary mode.
    """
    encoded_path = os.fsencode(file_path)
    with open(encoded_path, 'rb') as f:
        return sf.read(f, dtype=dtype)

# === WAV Integrity Check =====================================
def is_valid_wav(file_path):
    """
    Verify a file is a valid WAV by checking its header.
    """
    try:
        with open(file_path, "rb") as f:
            header = f.read(12)
        if header[0:4] != b'RIFF' or header[8:12] != b'WAVE':
            return False
        return True
    except Exception:
        return False

# === Note Conversion Helpers =====================================
def note_name_to_midi(note):
    """
    Convert a note (e.g. 'C#4') to its corresponding MIDI number.
    """
    note_map = {'C': 0, 'C#': 1, 'D': 2, 'D#': 3,
                'E': 4, 'F': 5, 'F#': 6, 'G': 7,
                'G#': 8, 'A': 9, 'A#': 10, 'B': 11}
    if len(note) == 2:
        key = note[0].upper()
        octave = int(note[1])
    elif len(note) == 3:
        key = note[0:2].upper()
        octave = int(note[2])
    else:
        raise ValueError(f"Invalid note format: {note}")
    # MIDI numbers: octave + 1 is used so that C4 becomes MIDI 60.
    midi = (octave + 1) * 12 + note_map[key]
    return midi

def midi_to_note_name(midi):
    """
    Convert a MIDI number back to its note representation.
    """
    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F',
                  'F#', 'G', 'G#', 'A', 'A#', 'B']
    octave = midi // 12 - 1
    note = note_names[midi % 12]
    return f"{note}{octave}"

def parse_note_range(note_range_str):
    """
    Parse a note range string (e.g. 'C1-F4') into a list of MIDI numbers.
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

# === Loop Marker Helpers =========================================
def get_loop_markers(file_path):
    """
    Extract loop markers from a 'smpl' chunk in the WAV file.
    """
    try:
        encoded_path = os.fsencode(file_path)
        with open(encoded_path, 'rb') as f:
            data = f.read()
        index = data.find(b'smpl')
        if index == -1:
            return None
        chunk_size = struct.unpack('<I', data[index+4:index+8])[0]
        if chunk_size < 36:
            return None
        smpl_header = data[index+8:index+8+36]
        header_values = struct.unpack('<9I', smpl_header)
        num_loops = header_values[7]
        loops_data = data[index+8+36: index+8+36+num_loops*24]
        loop_markers = []
        for i in range(num_loops):
            loop_chunk = loops_data[i*24:(i+1)*24]
            values = struct.unpack('<6I', loop_chunk)
            start = values[2]
            end = values[3]
            loop_markers.append((start, end))
        return loop_markers if loop_markers else None
    except Exception as e:
        print(f"Warning: Could not read loop markers from '{safe_str(file_path)}': {e}")
        return None

def embed_loop_markers(wav_path, loop_markers, sr, orig_length, new_length):
    """
    Embed loop markers into the WAV file by appending a 'smpl' chunk.
    Loop marker positions are adjusted proportionally if the sample length changes.
    """
    try:
        encoded_path = os.fsencode(wav_path)
        with open(encoded_path, 'rb') as f:
            wav_bytes = f.read()
        sample_period = int(1e9 / sr)
        num_loops = len(loop_markers)
        smpl_header = struct.pack('<9I', 0, 0, sample_period, 60, 0, 0, 0, num_loops, 0)
        loop_data = b''
        for i, (start, end) in enumerate(loop_markers):
            loop_data += struct.pack('<6I', i, 0, start, end, 0, 0)
        smpl_chunk_data = smpl_header + loop_data
        smpl_chunk_size = len(smpl_chunk_data)
        smpl_chunk = b'smpl' + struct.pack('<I', smpl_chunk_size) + smpl_chunk_data

        new_wav_bytes = wav_bytes + smpl_chunk
        new_riff_size = len(new_wav_bytes) - 8
        new_wav_bytes = new_wav_bytes[:4] + struct.pack('<I', new_riff_size) + new_wav_bytes[8:]
        with open(encoded_path, 'wb') as f:
            f.write(new_wav_bytes)
    except Exception as e:
        print(f"Warning: Could not embed loop markers in '{safe_str(wav_path)}': {e}")

# === Audio Processing Functions ==================================
def load_audio(file_path):
    """
    Load an audio file without forcing a conversion in sample rate or bit depth.
    """
    y, sr = safe_sf_read(file_path, dtype='float32')
    return y, sr

def apply_pitch_shift(y, sr, semitones):
    """
    Pitch shift audio using Rubberband.
    
    Writes the audio to a temporary file, applies pitch shifting via Rubberband, then reads the result.
    """
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tf_in:
        input_filename = tf_in.name
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tf_out:
        output_filename = tf_out.name
    try:
        sf.write(input_filename, y, sr, subtype='FLOAT')
        cmd = ['rubberband', '-p', str(semitones), '--fine', input_filename, output_filename]
        result = subprocess.run(cmd, capture_output=True)
        if result.returncode != 0:
            err = result.stderr.decode('utf-8').strip()
            raise RuntimeError(f"rubberband pitch shifting failed: {err}")
        y_shifted, sr_out = sf.read(output_filename, dtype='float32')
        if y_shifted.ndim > 1:
            y_shifted = y_shifted.mean(axis=1)
    finally:
        if os.path.exists(input_filename): os.remove(input_filename)
        if os.path.exists(output_filename): os.remove(output_filename)
    return y_shifted

def process_audio(y, sr):
    """
    Apply TPDF dithering to reduce quantization error and clip the signal to [-1, 1].
    """
    LSB = 1.0 / 32768
    dither = (np.random.uniform(-LSB/2, LSB/2, size=y.shape) +
              np.random.uniform(-LSB/2, LSB/2, size=y.shape))
    y_dithered = y + dither
    return np.clip(y_dithered, -1.0, 1.0)

def save_audio(y, sr, dst):
    """
    Save the processed audio as a 16‑bit PCM WAV file.
    """
    sf.write(dst, y, sr, subtype='PCM_16')

def process_and_copy_file(src, dst, skip_existing):
    """
    Process a WAV file (load, apply dithering, and re‑embed loop markers) and save it.
    
    If skip_existing is True and the destination file exists and is valid, the processing is skipped.
    """
    if skip_existing and os.path.exists(dst):
        if not is_valid_wav(dst):
            print(f"Found invalid/incomplete file '{safe_str(dst)}'; overwriting.")
            os.remove(dst)
        else:
            print(f"Skipping processing of '{safe_str(dst)}' (already exists).")
            return
    y, sr = load_audio(src)
    loop_markers = get_loop_markers(src)
    y_processed = process_audio(y, sr)
    if skip_existing and os.path.exists(dst):
        if not is_valid_wav(dst):
            print(f"Found invalid/incomplete file '{safe_str(dst)}'; overwriting.")
            os.remove(dst)
            save_audio(y_processed, sr, dst)
        else:
            print(f"Skipping generation of '{safe_str(dst)}' (already exists).")
    else:
        save_audio(y_processed, sr, dst)
    if loop_markers:
        orig_length = len(y)
        new_length = len(y_processed)
        adjusted = [(int(start * new_length / orig_length), int(end * new_length / orig_length))
                    for (start, end) in loop_markers]
        embed_loop_markers(dst, adjusted, sr, orig_length, new_length)

def convert_file_to_mono(src, dst, skip_existing):
    """
    Convert a WAV file to monaural using SoX and re‑embed loop markers.
    
    Skips conversion if the destination file already exists and is valid.
    """
    if skip_existing and os.path.exists(dst):
        if not is_valid_wav(dst):
            print(f"Found invalid/incomplete mono file '{safe_str(dst)}'; overwriting.")
            os.remove(dst)
        else:
            print(f"Skipping mono conversion of '{safe_str(dst)}' (already exists).")
            return
    cmd = ['sox', src, '-c', '1', dst]
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0:
        err = result.stderr.decode('utf-8').strip()
        raise RuntimeError(f"SoX mono conversion failed for '{safe_str(src)}': {err}")
    loop_markers = get_loop_markers(src)
    if loop_markers:
        y_src, sr_src = safe_sf_read(src, dtype='float32')
        y_dst, sr_dst = safe_sf_read(dst, dtype='float32')
        orig_length = len(y_src)
        new_length = len(y_dst)
        adjusted = [(int(start * new_length / orig_length), int(end * new_length / orig_length))
                    for (start, end) in loop_markers]
        embed_loop_markers(dst, adjusted, sr_dst, orig_length, new_length)

# === Directory Traversal and Sample‑Set Processing =============
def process_directory(input_root, output_root, mono_output_root, note_range_midi, skip_existing):
    """
    Walk through input_root and process sample files.
    
    Filenames in each directory are sanitized and the folder structure is recreated in both output roots.
    
    When a note range is provided (pitched mode), files are grouped based on their base name and the pitch
    immediately before the ".wav" extension. For each group, missing notes within the specified range are filled
    in by pitch-shifting the nearest candidate.
    
    If no note range is provided, all .wav files are simply processed as-is.
    """
    for dirpath, dirnames, filenames in os.walk(input_root):
        filenames = sanitize_directory(dirpath, filenames)
        
        rel_dir = os.path.relpath(dirpath, input_root)
        out_dir = os.path.join(output_root, rel_dir)
        mono_dir = os.path.join(mono_output_root, rel_dir)
        os.makedirs(out_dir, exist_ok=True)
        os.makedirs(mono_dir, exist_ok=True)

        # Copy non‑wav files unchanged.
        for fname in filenames:
            if fname.startswith('.') or fname.lower().endswith('.wav'):
                continue
            src_file = os.path.join(dirpath, fname)
            dst_file = os.path.join(out_dir, fname)
            mono_dst = os.path.join(mono_dir, fname)
            if not (skip_existing and os.path.exists(dst_file)):
                shutil.copy2(src_file, dst_file)
            if not (skip_existing and os.path.exists(mono_dst)):
                shutil.copy2(src_file, mono_dst)

        if note_range_midi is None:
            # Non‑pitched mode: simply process all .wav files.
            for fname in filenames:
                if fname.startswith('.') or not fname.lower().endswith('.wav'):
                    continue
                new_fname = modify_filename(fname, note_range_midi)
                # For files with a MIDI offset, if out-of-range then skip.
                if new_fname is None:
                    print(f"Skipping {fname} because MIDI offset note is out-of-range.")
                    continue
                src = os.path.join(dirpath, fname)
                dst = os.path.join(out_dir, new_fname)
                process_and_copy_file(src, dst, skip_existing)
                mono_dst = os.path.join(mono_dir, new_fname)
                try:
                    convert_file_to_mono(dst, mono_dst, skip_existing)
                except Exception as e:
                    print(f"Error converting '{safe_str(dst)}' to mono: {e}")
        else:
            # Pitched mode: group files by base name using only the pitch immediately before the extension.
            pattern = re.compile(r'^(.*)_([A-G][#]?\d)\.wav$', re.IGNORECASE)
            sample_sets = {}
            non_matching_wavs = []
            for fname in filenames:
                if fname.startswith('.') or not fname.lower().endswith('.wav'):
                    continue
                match = pattern.match(fname)
                if match:
                    base_name = match.group(1)
                    pitch_str = match.group(2)
                    try:
                        midi = note_name_to_midi(pitch_str)
                    except Exception as e:
                        print(f"Warning: Could not parse note in filename '{safe_str(fname)}': {e}")
                        continue
                    full_path = os.path.join(dirpath, fname)
                    sample_sets.setdefault(base_name, []).append((midi, full_path))
                else:
                    non_matching_wavs.append(fname)
            
            # Process non-matching .wav files as-is.
            for fname in non_matching_wavs:
                new_fname = modify_filename(fname, note_range_midi)
                if new_fname is None:
                    print(f"Skipping {fname} because MIDI offset note is out-of-range.")
                    continue
                src = os.path.join(dirpath, fname)
                dst = os.path.join(out_dir, new_fname)
                process_and_copy_file(src, dst, skip_existing)
                mono_dst = os.path.join(mono_dir, new_fname)
                try:
                    convert_file_to_mono(dst, mono_dst, skip_existing)
                except Exception as e:
                    print(f"Error converting '{safe_str(dst)}' to mono: {e}")
            
            # Process each sample set.
            for base, candidates in sample_sets.items():
                # Process each original candidate file.
                for midi, src in candidates:
                    new_fname = f"{base}_{midi_to_note_name(midi)}.wav"
                    new_fname = modify_filename(new_fname, note_range_midi)
                    if new_fname is None:
                        print(f"Skipping candidate {src} because generated MIDI offset note is out-of-range.")
                        continue
                    dst = os.path.join(out_dir, new_fname)
                    process_and_copy_file(src, dst, skip_existing)
                    mono_dst = os.path.join(mono_dir, new_fname)
                    try:
                        convert_file_to_mono(dst, mono_dst, skip_existing)
                    except Exception as e:
                        print(f"Error converting '{safe_str(dst)}' to mono: {e}")
                provided_notes = {midi for midi, _ in candidates}
                missing_midis = [m for m in note_range_midi if m not in provided_notes]
                for target_midi in missing_midis:
                    # Choose the candidate that minimizes the absolute pitch difference.
                    candidate = min(candidates, key=lambda c: abs(c[0] - target_midi))
                    source_midi, src = candidate
                    semitones = target_midi - source_midi
                    new_fname = f"{base}_{midi_to_note_name(target_midi)}.wav"
                    new_fname = modify_filename(new_fname, note_range_midi)
                    if new_fname is None:
                        print(f"Skipping missing note generation for {src} because generated MIDI offset note is out-of-range.")
                        continue
                    try:
                        y, sr = load_audio(src)
                    except Exception as e:
                        print(f"Error loading '{safe_str(src)}': {e}")
                        continue
                    try:
                        y_shifted = apply_pitch_shift(y, sr, semitones) if semitones != 0 else y
                    except Exception as e:
                        print(f"Error pitch shifting '{safe_str(src)}': {e}")
                        continue
                    y_processed = process_audio(y_shifted, sr)
                    dst = os.path.join(out_dir, new_fname)
                    if skip_existing and os.path.exists(dst):
                        if not is_valid_wav(dst):
                            print(f"Found invalid/incomplete file '{safe_str(dst)}'; overwriting.")
                            os.remove(dst)
                        else:
                            print(f"Skipping generation of '{safe_str(dst)}' (already exists).")
                            continue
                    save_audio(y_processed, sr, dst)
                    loop_markers = get_loop_markers(src)
                    if loop_markers:
                        orig_length = len(y)
                        new_length = len(y_processed)
                        adjusted = [(int(start * new_length / orig_length), int(end * new_length / orig_length))
                                    for (start, end) in loop_markers]
                        embed_loop_markers(dst, adjusted, sr, orig_length, new_length)
                    print(f"Generated missing sample: {safe_str(dst)}")
                    mono_dst = os.path.join(mono_dir, new_fname)
                    try:
                        convert_file_to_mono(dst, mono_dst, skip_existing)
                    except Exception as e:
                        print(f"Error converting '{safe_str(dst)}' to mono: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="Process .wav samples: copy folder structure, generate pitch‑shifted samples via Rubberband, "
                    "and mirror the output in a second tree with high‑quality mono conversion (loop markers preserved). "
                    "Optional flags: --note-range for pitched instruments, --skip-existing to avoid reprocessing."
    )
    parser.add_argument("input_root", help="Input root directory to search for samples")
    parser.add_argument("output_root", help="Primary output root directory for processed samples")
    parser.add_argument("mono_output_root", help="Output root directory for high‑quality mono‑converted samples")
    parser.add_argument("--note-range", help="Optional note range (e.g. 'C1-F4') to fill in missing notes. Omit for non‑pitched samples.")
    parser.add_argument("--skip-existing", action="store_true", help="Skip processing if destination file exists.")
    args = parser.parse_args()

    if args.note_range:
        try:
            note_range_midi = parse_note_range(args.note_range)
        except Exception as e:
            print(f"Error parsing note range: {e}")
            return
    else:
        note_range_midi = None

    process_directory(args.input_root, args.output_root, args.mono_output_root, note_range_midi, args.skip_existing)

if __name__ == "__main__":
    main()
