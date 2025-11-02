#!/usr/bin/env python3
"""
gig-2-sfz.py

A command-line Python tool to convert the output of the gigdump utility into
separate SFZ instrument files—one per instrument. Each SFZ file will reference
extracted WAV sample files (assumed to be in a “samples” folder by default).

Usage:
    python3 gig-2-sfz.py <input_gigdump.txt> <output_folder> [--sample-folder <sample_folder>]

Example:
    python3 gig-2-sfz.py mygigdump.txt output_folder --sample-folder extracted_samples

The tool uses a simple naming convention: each output file is named with the
instrument number and a sanitized instrument name.
"""

import argparse
import os
import re
import sys

def parse_gigdump(file_content):
    """
    Parse the gigdump text output and return a list of instrument dictionaries.
    
    Each instrument dict contains:
      - name: Instrument name.
      - midibank: MIDI bank number.
      - midiprogram: MIDI program number.
      - regions: List of region dictionaries.
    
    Each region dict may contain:
      - sample: A sample reference from the region line (if any).
      - key_range: Tuple (low_key, high_key).
      - vel_range: Tuple (low_vel, high_vel).
      - dimension_regions: List of dimension region dictionaries.
    
    Each dimension region dict contains (if parsed):
      - sample: Sample name.
      - unity_note: Root key for pitch.
      - finetune: Fine tuning in cents.
      - gain: Gain in dB.
      - offset: Sample start offset.
    """
    instruments = []
    current_instrument = None
    current_region = None

    # We want to parse the section starting with "Available Instruments:"
    in_instruments_section = False

    lines = file_content.splitlines()
    for line in lines:
        line_stripped = line.strip()
        # Check if we've reached the "Available Instruments:" section
        if line_stripped.startswith("Available Instruments:"):
            in_instruments_section = True
            continue

        # If not in instruments section, ignore the line.
        if not in_instruments_section:
            continue

        # Match instrument header lines
        # Example: Instrument 1) "BASIC INSTRUMENTS",  MIDIBank=0, MIDIProgram=0
        m_inst = re.match(r'^Instrument\s+\d+\)\s+"([^"]+)",\s+MIDIBank=(\d+),\s+MIDIProgram=(\d+)', line_stripped)
        if m_inst:
            if current_instrument is not None:
                instruments.append(current_instrument)
            current_instrument = {
                "name": m_inst.group(1),
                "midibank": int(m_inst.group(2)),
                "midiprogram": int(m_inst.group(3)),
                "regions": []
            }
            current_region = None
            continue

        # Match region lines
        # Example: Region 1) Sample: "Caxixi-low_ES", 44100Hz,  KeyRange=48-48, VelocityRange=0-127, Layers=1
        m_region = re.match(r'^Region\s+\d+\)\s+(.*)', line_stripped)
        if m_region:
            region_line = m_region.group(1)
            # Try to extract sample reference (it might be <NO_VALID_SAMPLE_REFERENCE>)
            sample_m = re.search(r'Sample:\s+"([^"]+)"', region_line)
            sample_ref = sample_m.group(1) if sample_m else None

            key_range_m = re.search(r'KeyRange=(\d+)-(\d+)', region_line)
            vel_range_m = re.search(r'VelocityRange=(\d+)-(\d+)', region_line)
            key_range = (int(key_range_m.group(1)), int(key_range_m.group(2))) if key_range_m else None
            vel_range = (int(vel_range_m.group(1)), int(vel_range_m.group(2))) if vel_range_m else None

            current_region = {
                "sample": sample_ref,
                "key_range": key_range,
                "vel_range": vel_range,
                "dimension_regions": []
            }
            current_instrument["regions"].append(current_region)
            continue

        # Match Dimension Region lines
        # Example:
        # Dimension Region 1) Sample: "Caxixi-low_ES", 44100Hz, UnityNote=48, FineTune=0, Gain=0dB, SampleStartOffset=0
        m_dim = re.match(r'^Dimension Region\s+\d+\)\s+(.*)', line_stripped)
        if m_dim:
            dim_line = m_dim.group(1)
            sample_m = re.search(r'Sample:\s+"([^"]+)"', dim_line)
            sample = sample_m.group(1) if sample_m else None

            unity_note_m = re.search(r'UnityNote=(\d+)', dim_line)
            unity_note = int(unity_note_m.group(1)) if unity_note_m else None

            finetune_m = re.search(r'FineTune=([\-\d\.]+)', dim_line)
            finetune = float(finetune_m.group(1)) if finetune_m else 0.0

            gain_m = re.search(r'Gain=([-\d\.]+)dB', dim_line)
            gain = float(gain_m.group(1)) if gain_m else 0.0

            offset_m = re.search(r'SampleStartOffset=(\d+)', dim_line)
            offset = int(offset_m.group(1)) if offset_m else 0

            dim_region = {
                "sample": sample,
                "unity_note": unity_note,
                "finetune": finetune,
                "gain": gain,
                "offset": offset
            }
            if current_region is not None:
                current_region["dimension_regions"].append(dim_region)
            continue

    if current_instrument is not None:
        instruments.append(current_instrument)
    return instruments

def generate_sfz(instrument, sample_path_mapper):
    """
    Generate an SFZ file string for one instrument.
    
    sample_path_mapper: a function that maps a sample name to the expected file path.
    """
    lines = []
    # Write a <global> section (can include common opcodes)
    lines.append("<global>")
    # Optionally, you could set a default_path here if you want relative sample paths.
    lines.append("default_path=")
    lines.append("")

    # Comment with instrument details
    lines.append("// Instrument: {} (MIDI Bank: {}, MIDI Program: {})".format(
        instrument["name"], instrument["midibank"], instrument["midiprogram"]))
    lines.append("")

    # Iterate over regions
    for region in instrument["regions"]:
        # If region has dimension regions, create a separate <region> for each
        if region["dimension_regions"]:
            for dregion in region["dimension_regions"]:
                # Skip if there's no valid sample reference.
                if not dregion["sample"]:
                    continue

                lines.append("<region>")
                sample_name = dregion["sample"]
                sfz_sample_path = sample_path_mapper(sample_name)
                if sfz_sample_path is None:
                    # Fallback: assume sample file is sample_name + ".wav"
                    sfz_sample_path = sample_name.replace(" ", "_") + ".wav"
                lines.append("sample={}".format(sfz_sample_path))
                if region["key_range"]:
                    lines.append("lokey={}".format(region["key_range"][0]))
                    lines.append("hikey={}".format(region["key_range"][1]))
                if region["vel_range"]:
                    lines.append("lovel={}".format(region["vel_range"][0]))
                    lines.append("hivel={}".format(region["vel_range"][1]))
                if dregion["unity_note"] is not None:
                    lines.append("pitch_keycenter={}".format(dregion["unity_note"]))
                if dregion["finetune"] != 0:
                    lines.append("tune={}".format(dregion["finetune"]))
                if dregion["gain"] != 0:
                    lines.append("volume={}".format(dregion["gain"]))
                if dregion["offset"] != 0:
                    lines.append("offset={}".format(dregion["offset"]))
                lines.append("")  # blank line for region separation
        else:
            # If there are no dimension regions, use the region's own sample reference.
            # Skip the region if sample reference is missing.
            if not region["sample"]:
                continue

            lines.append("<region>")
            sample_name = region["sample"]
            sfz_sample_path = sample_path_mapper(sample_name)
            if sfz_sample_path is None:
                sfz_sample_path = sample_name.replace(" ", "_") + ".wav"
            lines.append("sample={}".format(sfz_sample_path))
            if region["key_range"]:
                lines.append("lokey={}".format(region["key_range"][0]))
                lines.append("hikey={}".format(region["key_range"][1]))
            if region["vel_range"]:
                lines.append("lovel={}".format(region["vel_range"][0]))
                lines.append("hivel={}".format(region["vel_range"][1]))
            lines.append("")
    return "\n".join(lines)

def sample_path_mapper_factory(sample_folder):
    """
    Returns a function that maps a sample name to a file path in the sample folder.
    
    This assumes that the extracted samples are WAV files named as:
      <sample_name>.wav (spaces replaced with underscores)
    """
    def mapper(sample_name):
        if sample_name is None:
            return None
        # Create a safe filename by replacing non-alphanumeric characters
        filename = re.sub(r'\W+', '_', sample_name) + ".wav"
        full_path = os.path.join(sample_folder, filename)
        if os.path.exists(full_path):
            return full_path
        else:
            # If the file doesn't exist, return the filename only
            return filename
    return mapper

def main():
    parser = argparse.ArgumentParser(
        description="Convert gigdump output to SFZ instrument files.")
    parser.add_argument("input_file", help="Path to the gigdump output text file.")
    parser.add_argument("output_folder", help="Folder where SFZ files will be saved.")
    parser.add_argument("--sample-folder", help="Folder where extracted sample WAVs are located. "
                                                "Defaults to output_folder/samples",
                        default=None)
    args = parser.parse_args()

    # Read the input file
    try:
        with open(args.input_file, "r") as f:
            content = f.read()
    except Exception as e:
        sys.exit("Error reading input file: " + str(e))

    instruments = parse_gigdump(content)
    if not instruments:
        sys.exit("No instruments found in the gigdump output.")

    # Determine the folder where samples are located.
    sample_folder = args.sample_folder
    if sample_folder is None:
        sample_folder = os.path.join(args.output_folder, "samples")
    # Create sample folder if it does not exist (the user is expected to extract samples there)
    os.makedirs(sample_folder, exist_ok=True)

    mapper = sample_path_mapper_factory(sample_folder)
    # Create the output folder if needed
    os.makedirs(args.output_folder, exist_ok=True)

    # For each instrument, generate an SFZ file.
    for idx, inst in enumerate(instruments, start=1):
        # Sanitize instrument name to form a valid filename.
        safe_name = re.sub(r'\W+', '_', inst["name"])
        filename = f"{idx:02d}_{safe_name}.sfz"
        out_path = os.path.join(args.output_folder, filename)
        sfz_text = generate_sfz(inst, mapper)
        try:
            with open(out_path, "w") as outf:
                outf.write(sfz_text)
            print(f"Wrote instrument '{inst['name']}' to {out_path}")
        except Exception as e:
            print(f"Error writing {out_path}: {e}")

if __name__ == "__main__":
    main()
