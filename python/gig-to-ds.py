#!/usr/bin/env python3
"""
gig_to_ds.py

A command-line tool that runs "gigdump" against a .gig file passed in as an argument,
parses its output to extract sample (zone) data, converts scientific notation to decimal,
translates MIDI note numbers into note names (using sharps only), and then outputs
DecentSampler-compatible XML (one <sample> element per zone).

Usage:
    python3 gig_to_ds.py instrument.gig

Requirements:
    - gigdump must be installed and in your PATH.
    - The .gig file must be readable by gigdump.
"""

import sys, subprocess, re
from math import floor

def midi_note_to_name(midi_num):
    """Convert a MIDI note number (0-127) to a note name with octave (all sharps)."""
    notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    octave = (midi_num // 12) - 1  # MIDI note 0 is C-1
    return notes[midi_num % 12] + str(octave)

def parse_samples_section(lines):
    """
    Parses the "ALL Available Samples" section to get loop information.
    Assumes that each sample entry begins with "Sample <num>)" and may include
    loop start/end info in the line (if available).
    Returns a dict mapping sample name to (loopStart, loopEnd) or None.
    """
    samples = {}
    in_samples = False
    for line in lines:
        if "ALL Available Samples" in line:
            in_samples = True
            continue
        if in_samples and ("Available Real-Time Instrument Scripts" in line or "Available Instruments:" in line):
            break
        if in_samples:
            m = re.match(r'\s*Sample\s+\d+\)\s+"([^"]+)"', line)
            if m:
                sample_name = m.group(1)
                # Try to extract loop start and end if present (example: Start=12345, End=34456)
                m_loop = re.search(r'Start=(\d+),\s*End=(\d+)', line)
                if m_loop:
                    loop_start = int(m_loop.group(1))
                    loop_end = int(m_loop.group(2))
                    samples[sample_name] = (loop_start, loop_end)
                else:
                    samples[sample_name] = None
    return samples

def parse_instruments_section(lines):
    """
    Parses the "Available Instruments:" section to extract instrument regions.
    Each region (and its associated "Dimension Region" block) is parsed for:
      - sample reference (skips <NO_VALID_SAMPLE_REFERENCE>)
      - key range and velocity range
      - (in Dimension Region) UnityNote, Gain, and envelope (EG1) parameters.
    Returns a list of region dictionaries.
    """
    regions = []
    in_instruments = False
    i = 0
    while i < len(lines):
        line = lines[i]
        if "Available Instruments:" in line:
            in_instruments = True
            i += 1
            continue
        if in_instruments:
            # Look for a region header line that contains a Sample reference
            if "Region" in line and "Sample:" in line:
                # Extract the sample reference; if it's "<NO_VALID_SAMPLE_REFERENCE>", skip it.
                m_sample = re.search(r'Sample:\s*("([^"]+)"|<NO_VALID_SAMPLE_REFERENCE>)', line)
                if m_sample:
                    sample_ref = m_sample.group(2) if m_sample.group(2) else m_sample.group(1)
                    if "<NO_VALID_SAMPLE_REFERENCE>" in sample_ref:
                        i += 1
                        continue
                    # Create a region dict with defaults
                    region = {
                        "sample": sample_ref,
                        "loNote": 0, "hiNote": 127,
                        "loVel": 0, "hiVel": 127,
                        "root": None,
                        "volume": None,
                        "attack": None, "decay": None, "sustain": None, "release": None,
                        "hasLoop": False
                    }
                    # KeyRange and VelocityRange may be on this same line.
                    m_key = re.search(r'KeyRange=(\d+)-(\d+)', line)
                    if m_key:
                        region["loNote"] = int(m_key.group(1))
                        region["hiNote"] = int(m_key.group(2))
                    m_vel = re.search(r'VelocityRange=(\d+)-(\d+)', line)
                    if m_vel:
                        region["loVel"] = int(m_vel.group(1))
                        region["hiVel"] = int(m_vel.group(2))
                    m_loops = re.search(r'Loops=(\d+)', line)
                    if m_loops:
                        region["hasLoop"] = int(m_loops.group(1)) > 0

                    # Now look ahead for the Dimension Region block that holds envelope and tuning info.
                    # We look at the next few lines.
                    j = i + 1
                    block = ""
                    while j < len(lines) and not lines[j].strip().startswith("Region"):
                        block += " " + lines[j].strip()
                        # Break early if we think we have enough info
                        if "EG1Attack=" in block:
                            break
                        j += 1

                    # UnityNote (the sample's root note)
                    m_unity = re.search(r'UnityNote=(\d+)', block)
                    if m_unity:
                        region["root"] = int(m_unity.group(1))
                    else:
                        # Fallback: use the low key
                        region["root"] = region["loNote"]

                    # Gain (volume) in dB – omit if 0.
                    m_gain = re.search(r'Gain=([-+0-9.]+)dB', block)
                    if m_gain:
                        gain_val = float(m_gain.group(1))
                        if abs(gain_val) > 1e-6:
                            region["volume"] = gain_val

                    # Envelope settings (EG1)
                    m_env = re.search(r'EG1Attack=([\d.eE+-]+)s,\s*EG1Decay1=([\d.eE+-]+)s,\s*EG1Sustain=(\d+)permille,\s*EG1Release=([\d.eE+-]+)s', block)
                    if m_env:
                        att = round(float(m_env.group(1)), 3)
                        dec = round(float(m_env.group(2)), 3)
                        sus = round(int(m_env.group(3)) / 1000.0, 3)
                        rel = round(float(m_env.group(4)), 3)
                        # Only set if non-default (defaults: attack=0, sustain=1.0, etc.)
                        if att > 0:
                            region["attack"] = att
                        if dec > 0 and sus < 1.0:
                            region["decay"] = dec
                        if sus < 1.0:
                            region["sustain"] = sus
                        if rel > 0:
                            region["release"] = rel

                    regions.append(region)
                    i = j  # jump ahead
                    continue
        i += 1
    return regions

def generate_sample_xml(region, sample_loops):
    """
    Given a region dict and a sample_loops dict (from parse_samples_section),
    build the XML string for a DecentSampler <sample> entry.
    The attribute order is:
      - Pitch/volume: path, rootNote, loNote/hiNote, loVel/hiVel, volume
      - Envelope: attack, decay, sustain, release
      - Loop info (if present): loopStart, loopEnd, loopEnabled
    Only include attributes that are non-default.
    """
    # Use the sample name as the filename (assume a .wav file in a samples/ folder)
    attrs = []
    sample_name = region["sample"]
    attrs.append(f'path="samples/{sample_name}.wav"')
    # rootNote is required
    root = region.get("root", region["loNote"])
    attrs.append(f'rootNote="{root}"')
    # Only include key range if not the full range
    if region["loNote"] != 0 or region["hiNote"] != 127:
        attrs.append(f'loNote="{region["loNote"]}"')
        attrs.append(f'hiNote="{region["hiNote"]}"')
    # Only include velocity range if not full
    if region["loVel"] != 0 or region["hiVel"] != 127:
        attrs.append(f'loVel="{region["loVel"]}"')
        attrs.append(f'hiVel="{region["hiVel"]}"')
    # Volume (if provided and nonzero)
    if region.get("volume") is not None:
        # Format to one decimal place (or as integer if it divides evenly)
        vol = region["volume"]
        if vol % 1:
            attrs.append(f'volume="{vol:.1f}dB"')
        else:
            attrs.append(f'volume="{int(vol)}dB"')
    # Envelope attributes (only if non-default)
    if region.get("attack") is not None:
        attrs.append(f'attack="{region["attack"]:.3f}"')
    if region.get("decay") is not None:
        attrs.append(f'decay="{region["decay"]:.3f}"')
    if region.get("sustain") is not None:
        attrs.append(f'sustain="{region["sustain"]:.3f}"')
    if region.get("release") is not None:
        attrs.append(f'release="{region["release"]:.3f}"')
    # Loop info – if the region has loops and sample_loops contains loop data, include it.
    if region.get("hasLoop") and sample_loops.get(sample_name):
        loopStart, loopEnd = sample_loops[sample_name]
        attrs.append(f'loopStart="{loopStart}"')
        attrs.append(f'loopEnd="{loopEnd}"')
        attrs.append('loopEnabled="true"')

    # Build attribute string. We'll try to keep it to a single line if it fits.
    attr_str = " ".join(attrs)
    # If the string is long, break it into groups (up to 3 lines) for readability.
    if len(attr_str) > 100:
        # Group 1: path, rootNote, key and velocity ranges, volume
        group1 = " ".join([a for a in attrs if a.startswith("path") or a.startswith("rootNote") or a.startswith("loNote") or a.startswith("hiNote") or a.startswith("loVel") or a.startswith("hiVel") or a.startswith("volume")])
        # Group 2: envelope attributes
        group2 = " ".join([a for a in attrs if a.startswith("attack") or a.startswith("decay") or a.startswith("sustain") or a.startswith("release")])
        # Group 3: loop info
        group3 = " ".join([a for a in attrs if a.startswith("loop")])
        xml_lines = []
        xml_lines.append(f'<sample {group1}')
        if group2:
            xml_lines.append(f'        {group2}')
        if group3:
            xml_lines.append(f'        {group3} />')
        else:
            xml_lines[-1] += " />"
        return "\n".join(xml_lines)
    else:
        # Single-line output
        return f'<sample {attr_str} />'

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 gig_to_ds.py <instrument.gig>", file=sys.stderr)
        sys.exit(1)
    gig_file = sys.argv[1]
    try:
        proc = subprocess.run(["gigdump", gig_file],
                              check=True,
                              capture_output=True,
                              text=True)
    except FileNotFoundError:
        print("Error: 'gigdump' not found. Please install gigdump (libgig/gigtools) to use this script.", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError:
        print(f"Error: gigdump failed to process '{gig_file}'.", file=sys.stderr)
        sys.exit(1)

    output = proc.stdout
    if not output.strip():
        print(f"Error: No output from gigdump for '{gig_file}'. The file may be invalid.", file=sys.stderr)
        sys.exit(1)

    lines = output.splitlines()
    sample_loops = parse_samples_section(lines)
    regions = parse_instruments_section(lines)

    # Filter out any regions without a valid sample reference
    regions = [r for r in regions if r.get("sample")]

    # Sort the regions by: sample name, then by MIDI note (root), then velocity low, then volume.
    regions.sort(key=lambda r: (r["sample"].lower(),
                                r.get("root", r["loNote"]),
                                r["loVel"],
                                r.get("volume", 0)))

    # Output XML for each unique region.
    printed_xmls = set()
    for region in regions:
        xml = generate_sample_xml(region, sample_loops)
        if xml not in printed_xmls:
            print(xml)
            printed_xmls.add(xml)

if __name__ == '__main__':
    main()
