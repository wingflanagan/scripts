#!/usr/bin/env python3
import sys
import glob
import os
import re
import struct
import chunk
import subprocess

# Try importing pyperclip for clipboard support; fallback to Tkinter if needed.
try:
    import pyperclip
except ImportError:
    pyperclip = None

def note_to_midi(note):
    """
    Convert a note name (like "C#1") to its MIDI number.
    """
    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    m = re.match(r'([A-G]#?)(\d+)', note)
    if not m:
        return None
    pitch = m.group(1)
    octave = int(m.group(2))
    try:
        index = note_names.index(pitch)
    except ValueError:
        return None
    return index + octave * 12

def parse_smpl_chunk(filepath):
    """
    Use Python's built-in chunk module to parse the 'smpl' chunk from a WAV file.
    Returns (loop_start, loop_end) in frames; if not found, returns (0, 0).
    """
    loop_start = 0
    loop_end = 0
    try:
        with open(filepath, 'rb') as f:
            # Open the RIFF container.
            riff = chunk.Chunk(f, bigendian=False)
            if riff.getname() != b'RIFF':
                return loop_start, loop_end
            # The next 4 bytes indicate the file type; should be "WAVE"
            wave_type = f.read(4)
            if wave_type != b'WAVE':
                return loop_start, loop_end
            # Iterate over subchunks until we find "smpl"
            while True:
                try:
                    subchunk = chunk.Chunk(f, bigendian=False)
                except EOFError:
                    break
                if subchunk.getname() == b'smpl':
                    data = subchunk.read()
                    # The SMPL header is 36 bytes (9 x 4-byte integers)
                    if len(data) < 36:
                        break
                    # At offset 28 (bytes 28-31) is the number of sample loops.
                    num_loops = int.from_bytes(data[28:32], 'little')
                    if num_loops > 0 and len(data) >= 36 + 24:
                        # Each loop entry is 24 bytes; the first loop's structure:
                        #  0-3: cuePointID, 4-7: type, 8-11: start, 12-15: end, etc.
                        loop_start = int.from_bytes(data[36+8:36+12], 'little')
                        loop_end   = int.from_bytes(data[36+12:36+16], 'little')
                    break
                else:
                    subchunk.skip()
    except Exception as e:
        print(f"Error reading {filepath}: {e}", file=sys.stderr)
    return loop_start, loop_end

def get_loop_points_with_pymusiclooper(filepath):
    """
    Execute the pymusiclooper command to extract loop points from a sample file.
    Returns (loop_start, loop_end) as integers.
    """
    try:
        result = subprocess.run(
            ["pymusiclooper", "-s", "export-points", "--path", filepath, "--alt-export-top", "1"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        output_line = result.stdout.strip()
        if output_line:
            # Expected output format:
            # "56817 146412 0.16471360623836517 0.3210785304588626 0.9910307241335954"
            parts = output_line.split()
            if len(parts) >= 2:
                try:
                    loop_start = int(parts[0])
                    loop_end = int(parts[1])
                    return loop_start, loop_end
                except ValueError as ve:
                    # Log the error along with the tokens that failed to parse.
                    print(f"Error running pymusiclooper on {filepath}: {ve} - output tokens: {parts[:2]}", file=sys.stderr)
    except Exception as e:
        print(f"Error running pymusiclooper on {filepath}: {e}", file=sys.stderr)
    return 0, 0

def format_sample_line(filepath, note, loop_start, loop_end):
    """
    Format the sample entry line for DecentSampler dspreset.
    """
    relative_path = os.path.relpath(filepath, os.getcwd())
    return (f'<sample path="{relative_path}" rootNote="{note}" '
            f'loNote="{note}" hiNote="{note}" loopStart="{loop_start}" loopEnd="{loop_end}"/>')

def copy_to_clipboard(text):
    """
    Copy the given text to the system clipboard using pyperclip or Tkinter.
    """
    if pyperclip is not None:
        try:
            pyperclip.copy(text)
        except Exception as e:
            print(f"Clipboard copy failed using pyperclip: {e}", file=sys.stderr)
    else:
        try:
            import tkinter as tk
            root = tk.Tk()
            root.withdraw()
            root.clipboard_clear()
            root.clipboard_append(text)
            root.update()  # Keeps the clipboard content after the window is closed
            root.destroy()
        except Exception as e:
            print(f"Clipboard copy failed using Tkinter: {e}", file=sys.stderr)

def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <path with wildcards>", file=sys.stderr)
        sys.exit(1)
    
    # If the shell already expands the wildcard, sys.argv will contain multiple filenames.
    if len(sys.argv) > 2:
        files = sys.argv[1:]
    else:
        pattern = sys.argv[1]
        files = glob.glob(pattern)
    
    sample_data = []
    for filepath in files:
        base = os.path.basename(filepath)
        name_without_ext, _ = os.path.splitext(base)
        # Look for note patterns like A#1, C2, etc. and use the last occurrence.
        matches = re.findall(r'([A-G]#?\d+)', name_without_ext)
        if not matches:
            print(f"Skipping {base}: no note found", file=sys.stderr)
            continue
        note = matches[-1]
        midi_val = note_to_midi(note)
        if midi_val is None:
            print(f"Skipping {base}: invalid note '{note}'", file=sys.stderr)
            continue
        
        ls, le = parse_smpl_chunk(filepath)
        # If no loop points found in the smpl chunk, try pymusiclooper.
        if ls == 0 and le == 0:
            ls_alt, le_alt = get_loop_points_with_pymusiclooper(filepath)
            if ls_alt != 0 or le_alt != 0:
                ls, le = ls_alt, le_alt
        
        sample_data.append((filepath, note, ls, le, midi_val))
    
    # Sort by MIDI note number.
    sample_data.sort(key=lambda x: x[4])
    
    formatted_lines = []
    for data in sample_data:
        line = format_sample_line(data[0], data[1], data[2], data[3])
        formatted_lines.append(line)
        print(line)  # This goes to stdout.
    
    # Join the formatted lines and copy them to the clipboard.
    clipboard_text = "\n".join(formatted_lines)
    copy_to_clipboard(clipboard_text)

if __name__ == '__main__':
    main()
