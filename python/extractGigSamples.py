#!/usr/bin/env python3
"""
extract_samples.py - Improved Version in Python

Usage:
    python extractGigSamples.py /path/to/source /path/to/destination

This script recursively walks the source directory and reproduces its folder structure in the destination.
For each .gig file found, it creates a folder (named after the file without its extension) in the corresponding destination.
Inside that folder, a "samples" subfolder is created and the external command `gigextract` is used to extract sample .wav files.
The script then removes numeric prefixes from the extracted .wav files and sanitizes all filenames and directory names by
replacing any non-US English character (outside a–z, A–Z, 0–9, period, hash, underscore, and hyphen) with a hyphen (`-`).

Any file conflicts are resolved by appending a counter to the filename.
"""

import os
import sys
import shutil
import subprocess
import re
import string

ERROR_LOG_FILE = 'errors.txt'

def log_error(message):
    """Logs errors to a text file and prints to stderr."""
    sys.stderr.write(message + "\n")
    with open(ERROR_LOG_FILE, 'a') as f:
        f.write(message + "\n")

def remove_numeric_prefix(filename):
    """
    Removes a numeric prefix from a filename.
    E.g., "97_sample.wav" becomes "sample.wav".
    """
    return re.sub(r'^\d+_', '', filename)

def sanitize_filename(name):
    """
    Walks through the filename character by character.
    Only allows: letters (a-z, A-Z), digits (0-9), period, hash, underscore, and hyphen.
    Any other character (including accented ones) is replaced with a hyphen.
    """
    allowed = set(string.ascii_letters + string.digits + ".#_-")  # period is allowed!
    return ''.join(ch if ch in allowed else '-' for ch in name)

def get_unique_file_path(directory, file_name):
    """
    Ensures that a file name is unique within the specified directory.
    If a file exists with the given name, appends a counter to the base name until unique.
    """
    base, ext = os.path.splitext(file_name)
    sanitized_base = sanitize_filename(base)
    unique_file_name = sanitized_base + ext
    file_path = os.path.join(directory, unique_file_name)
    counter = 1

    while os.path.exists(file_path):
        unique_file_name = f"{sanitized_base}_{counter}{ext}"
        file_path = os.path.join(directory, unique_file_name)
        counter += 1

    return file_path

def process_directory(src_dir, dest_dir):
    """
    Processes a single directory by:
      - Reproducing the directory structure in dest_dir with sanitized names.
      - Processing .gig files and extracting their samples.
      - Copying other files while ensuring safe file names.
    """
    os.makedirs(dest_dir, exist_ok=True)
    try:
        items = os.scandir(src_dir)
    except Exception as e:
        log_error(f"Error reading directory {src_dir}: {e}")
        return

    for item in items:
        src_path = os.path.join(src_dir, item.name)
        sanitized_item_name = sanitize_filename(item.name)
        dest_path = os.path.join(dest_dir, sanitized_item_name)

        if item.is_dir():
            process_directory(src_path, dest_path)
        elif item.is_file():
            # Check for .gig file (case-insensitive)
            if item.name.lower().endswith('.gig'):
                print(f"Processing .gig file: {src_path}")
                gig_base_name = os.path.splitext(item.name)[0]
                sanitized_gig_base_name = sanitize_filename(gig_base_name)
                gig_dest_folder = os.path.join(dest_dir, sanitized_gig_base_name)
                os.makedirs(gig_dest_folder, exist_ok=True)

                samples_dir = os.path.join(gig_dest_folder, 'samples')
                os.makedirs(samples_dir, exist_ok=True)

                # Run the external gigextract command
                try:
                    subprocess.run(["gigextract", src_path, samples_dir], check=True)
                except subprocess.CalledProcessError as err:
                    log_error(f"Error extracting samples from {src_path}: {err}")
                    continue

                # Process each sample file
                try:
                    for file in os.listdir(samples_dir):
                        new_name = remove_numeric_prefix(file)
                        sanitized_new_name = sanitize_filename(new_name)
                        if sanitized_new_name != file:
                            old_path = os.path.join(samples_dir, file)
                            new_path = get_unique_file_path(samples_dir, sanitized_new_name)
                            if old_path != new_path:
                                os.rename(old_path, new_path)
                                print(f"Renamed {file} -> {os.path.basename(new_path)}")
                except Exception as rename_err:
                    log_error(f"Error renaming sample files in {samples_dir}: {rename_err}")

            else:
                # For non-.gig files, copy them safely to the destination
                try:
                    dest_file_path = get_unique_file_path(dest_dir, sanitized_item_name)
                    shutil.copy2(src_path, dest_file_path)
                    print(f"Copied file: {src_path} -> {dest_file_path}")
                except Exception as copy_err:
                    log_error(f"Error copying file {src_path}: {copy_err}")

def main():
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: python extract_samples.py <source directory> <destination directory>\n")
        sys.exit(1)

    src_root = os.path.abspath(sys.argv[1])
    dest_root = os.path.abspath(sys.argv[2])

    if not os.path.exists(src_root):
        sys.stderr.write(f"Source directory does not exist: {src_root}\n")
        sys.exit(1)

    print(f"Starting processing:\n  Source: {src_root}\n  Destination: {dest_root}")

    process_directory(src_root, dest_root)

    print("Processing complete.")

if __name__ == '__main__':
    main()
