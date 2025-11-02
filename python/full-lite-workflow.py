import argparse
import os
import re
import numpy as np
from scipy.io import wavfile
from pathlib import Path

# ------------------------- Audio Processing -------------------------
def apply_tpdf_dither(data, bit_depth):
    lsb = 1.0 / (2 ** (bit_depth - 1))
    dither = np.random.uniform(-lsb, lsb, data.shape) 
    dither += np.random.uniform(-lsb, lsb, data.shape)
    return data + dither

def convert_to_mono(data):
    if data.ndim == 2 and data.shape[1] == 2:
        if data.dtype.kind == 'i':
            float_data = data.astype(np.float64)
            mono = np.mean(float_data, axis=1)
            mono = np.round(mono).astype(data.dtype)
        else:
            mono = np.mean(data, axis=1)
        return mono
    return data

def process_wav(input_path, output_path):
    try:
        rate, data = wavfile.read(input_path)
    except Exception as e:
        print(f"Error reading {input_path}: {e}")
        return False

    # Skip if already 16-bit mono
    if data.dtype == np.int16 and (data.ndim == 1 or data.shape[1] == 1):
        print(f"Skipped (already 16-bit mono): {input_path}")
        return False

    # Process audio
    mono_data = convert_to_mono(data)
    
    # Convert to 16-bit with dithering
    target_dtype = np.int16
    max_int16 = np.iinfo(target_dtype).max
    
    if mono_data.dtype == np.float32:
        scaled = mono_data * max_int16
    elif mono_data.dtype == np.int32:
        scaled = mono_data.astype(np.float64)
        max_val = np.max(np.abs(scaled))
        if max_val > 0:
            scaled *= max_int16 / max_val
    else:
        scaled = mono_data.astype(np.float64)
    
    dithered = apply_tpdf_dither(scaled, 16)
    converted = dithered.clip(-max_int16, max_int16).astype(target_dtype)

    # Save output
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    try:
        wavfile.write(output_path, rate, converted)
        print(f"Created lite WAV: {output_path}")
        return True
    except Exception as e:
        print(f"Error writing {output_path}: {e}")
        return False

# ------------------------- SFZ Processing -------------------------
def process_sfz(input_path, output_path):
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {input_path}: {e}")
        return False

    # Update sample references
    updated_content = re.sub(
        r'(\bsample\s*=\s*["\']?)(.*?)(\.wav\b)(["\']?)',
        lambda m: f"{m.group(1)}{m.group(2)}_lite{m.group(3)}{m.group(4)}",
        content,
        flags=re.IGNORECASE
    )

    # Save processed SFZ
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        print(f"Created lite SFZ: {output_path}")
        return True
    except Exception as e:
        print(f"Error writing {output_path}: {e}")
        return False

# ------------------------- Main Logic -------------------------
def process_item(input_path, output_root, input_root):
    """Process either WAV or SFZ file"""
    # Generate output path
    rel_path = os.path.relpath(input_path, input_root)
    output_path = os.path.join(output_root, rel_path)
    
    # Add _lite suffix
    dirname, filename = os.path.split(output_path)
    base, ext = os.path.splitext(filename)
    output_path = os.path.join(dirname, f"{base}_lite{ext}")
    
    # Dispatch to appropriate processor
    if input_path.lower().endswith('.wav'):
        return process_wav(input_path, output_path)
    elif input_path.lower().endswith('.sfz'):
        return process_sfz(input_path, output_path)
    return False

def main():
    parser = argparse.ArgumentParser(
        description="Create Lite Versions of Sample Libraries",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("input_folder", help="Root directory containing original files")
    parser.add_argument("output_folder", help="Target directory for lite versions")
    parser.add_argument("-r", "--recursive", action="store_true",
                        help="Process directories recursively")
    args = parser.parse_args()

    if not os.path.exists(args.input_folder):
        print(f"Error: Input directory {args.input_folder} does not exist")
        return

    # Create output root directory
    Path(args.output_folder).mkdir(parents=True, exist_ok=True)

    # Process files
    processed_count = {'wav': 0, 'sfz': 0}
    
    for root, dirs, files in os.walk(args.input_folder):
        for file in files:
            if file.lower().endswith(('.wav', '.sfz')):
                input_path = os.path.join(root, file)
                success = process_item(input_path, args.output_folder, args.input_folder)
                
                if success:
                    if file.lower().endswith('.wav'):
                        processed_count['wav'] += 1
                    else:
                        processed_count['sfz'] += 1

        if not args.recursive:
            dirs[:] = []

    # Summary
    print(f"\nProcessing complete:")
    print(f"- Converted {processed_count['wav']} WAV files to 16-bit mono")
    print(f"- Processed {processed_count['sfz']} SFZ files")
    print(f"Output directory: {args.output_folder}")

if __name__ == "__main__":
    main()