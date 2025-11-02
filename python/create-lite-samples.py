import argparse
import os
import numpy as np
from scipy.io import wavfile

def apply_tpdf_dither(data, bit_depth):
    """Apply triangular probability density function dithering"""
    lsb = 1.0 / (2 ** (bit_depth - 1))
    dither = np.random.uniform(-lsb, lsb, data.shape) 
    dither += np.random.uniform(-lsb, lsb, data.shape)
    return data + dither

def convert_to_mono(data):
    """Convert stereo to mono with proper rounding"""
    if data.ndim == 2 and data.shape[1] == 2:
        if data.dtype.kind == 'i':
            float_data = data.astype(np.float64)
            mono = np.mean(float_data, axis=1)
            mono = np.round(mono).astype(data.dtype)
        else:
            mono = np.mean(data, axis=1)
        return mono
    return data

def convert_32bit_to_16bit(data):
    """Convert 32-bit audio to 16-bit with dithering"""
    target_dtype = np.int16
    max_int16 = np.iinfo(target_dtype).max
    
    if data.dtype == np.float32:
        scaled = data * max_int16
    elif data.dtype == np.int32:
        scaled = data.astype(np.float64)
        max_val = np.max(np.abs(scaled))
        if max_val > 0:
            scaled *= max_int16 / max_val
    else:
        return data
    
    dithered = apply_tpdf_dither(scaled, 16)
    return dithered.clip(-max_int16, max_int16).astype(target_dtype)

def process_file(input_path, output_path):
    """Process and save as lite version"""
    try:
        rate, data = wavfile.read(input_path)
    except Exception as e:
        print(f"Error reading {input_path}: {e}")
        return

    # Skip if already 16-bit mono
    if data.dtype == np.int16 and (data.ndim == 1 or data.shape[1] == 1):
        print(f"Skipped (already 16-bit mono): {input_path}")
        return

    # Process audio
    mono_data = convert_to_mono(data)
    converted_data = convert_32bit_to_16bit(mono_data)

    # Create output directory if needed
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    try:
        wavfile.write(output_path, rate, converted_data)
        print(f"Created lite version: {output_path}")
    except Exception as e:
        print(f"Error writing {output_path}: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="Create lite versions of sample instruments",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("input_folder", help="Directory containing original WAV files")
    parser.add_argument("output_folder", help="Directory to save lite versions")
    parser.add_argument("-r", "--recursive", action="store_true",
                        help="Process directories recursively")
    args = parser.parse_args()

    if not os.path.isdir(args.input_folder):
        print(f"Error: {args.input_folder} is not a valid directory")
        return

    # Create output root directory
    os.makedirs(args.output_folder, exist_ok=True)

    for root, dirs, files in os.walk(args.input_folder):
        # Calculate relative path for output directory
        rel_path = os.path.relpath(root, args.input_folder)
        output_dir = os.path.join(args.output_folder, rel_path)

        for f in files:
            if f.lower().endswith(".wav"):
                input_path = os.path.join(root, f)
                
                # Create output filename with _lite suffix
                filename, ext = os.path.splitext(f)
                output_filename = f"{filename}_lite{ext}"
                output_path = os.path.join(output_dir, output_filename)

                process_file(input_path, output_path)
        
        if not args.recursive:
            dirs[:] = []  # Stop recursion

if __name__ == "__main__":
    main()