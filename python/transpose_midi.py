import mido
from mido import MidiFile, MidiTrack, Message
import sys
import re

# Define note names and their corresponding pitch classes
NOTE_NAMES_SHARP = ['C', 'C#', 'D', 'D#', 'E', 'F',
                    'F#', 'G', 'G#', 'A', 'A#', 'B']
NOTE_NAMES_FLAT = ['C', 'Db', 'D', 'Eb', 'E', 'F',
                   'Gb', 'G', 'Ab', 'A', 'Bb', 'B']

# Map note names to pitch classes
NOTE_NAME_TO_PITCH_CLASS = {}
for i in range(12):
    NOTE_NAME_TO_PITCH_CLASS[NOTE_NAMES_SHARP[i]] = i
    NOTE_NAME_TO_PITCH_CLASS[NOTE_NAMES_FLAT[i]] = i

# Define interval patterns for each mode
MODES = {
    'ionian':         [2, 2, 1, 2, 2, 2, 1],  # Major scale
    'major':          [2, 2, 1, 2, 2, 2, 1],  # Synonym for Ionian
    'dorian':         [2, 1, 2, 2, 2, 1, 2],
    'phrygian':       [1, 2, 2, 2, 1, 2, 2],
    'lydian':         [2, 2, 2, 1, 2, 2, 1],
    'mixolydian':     [2, 2, 1, 2, 2, 1, 2],
    'aeolian':        [2, 1, 2, 2, 1, 2, 2],  # Natural minor scale
    'minor':          [2, 1, 2, 2, 1, 2, 2],  # Synonym for Aeolian
    'locrian':        [1, 2, 2, 1, 2, 2, 2],
    'whole-tone':     [2, 2, 2, 2, 2, 2],     # Whole-tone scale
    'pentatonic-major': [2, 2, 3, 2, 3],      # Major pentatonic scale
    'pentatonic-minor': [3, 2, 2, 3, 2],      # Minor pentatonic scale
}

# Function to generate a scale given a tonic and mode
def generate_scale(tonic_pc, mode_intervals):
    scale = [tonic_pc]
    for interval in mode_intervals:
        scale.append((scale[-1] + interval) % 12)
    return scale[:-1]  # Exclude the octave duplication

# Function to parse key string (e.g., 'D Major' or 'E minor')
def parse_key(key_str):
    key_str = key_str.strip()
    # Regular expression to match the key pattern
    match = re.match(r'^([A-G][b#]?)(\s+([a-zA-Z\-]+))?$', key_str, re.IGNORECASE)
    if not match:
        raise ValueError(f"Invalid key format: '{key_str}'")
    tonic_name = match.group(1).capitalize()
    mode_name = match.group(3).lower() if match.group(3) else 'ionian'  # Default to Ionian mode

    if tonic_name not in NOTE_NAME_TO_PITCH_CLASS:
        raise ValueError(f"Invalid tonic: '{tonic_name}'")
    if mode_name not in MODES:
        raise ValueError(f"Invalid mode: '{mode_name}'")

    tonic_pc = NOTE_NAME_TO_PITCH_CLASS[tonic_name]
    mode_intervals = MODES[mode_name]
    scale = generate_scale(tonic_pc, mode_intervals)
    return scale, tonic_pc

# Main function to transpose MIDI file
def transpose_midi(input_file, output_file, source_key_str, dest_key_str):
    # Parse source and destination keys
    source_scale, source_tonic_pc = parse_key(source_key_str)
    dest_scale, dest_tonic_pc = parse_key(dest_key_str)

    # Create mapping from source scale degrees to destination scale degrees
    scale_degree_mapping = {}
    N = len(source_scale)
    M = len(dest_scale)
    for idx, src_pc in enumerate(source_scale):
        if N > 1:
            mapped_idx = round(idx * (M - 1) / (N - 1))
        else:
            mapped_idx = 0
        dest_pc = dest_scale[mapped_idx]
        scale_degree_mapping[src_pc] = dest_pc

    # Load MIDI file
    mid = MidiFile(input_file)
    
    # IMPORTANT: copy the type and ticks_per_beat to preserve timing
    new_mid = MidiFile(type=mid.type, ticks_per_beat=mid.ticks_per_beat)

    for track in mid.tracks:
        new_track = MidiTrack()
        new_track.name = track.name  # optional: preserve track name if desired
        for msg in track:
            if msg.type in ('note_on', 'note_off'):
                # Transpose note if it's in the source scale
                note = msg.note
                pc = note % 12
                if pc in source_scale:
                    dest_pc = scale_degree_mapping[pc]
                    new_note = (note - pc) + dest_pc
                    msg.note = new_note

            new_track.append(msg)  # append the (possibly modified) message

        new_mid.tracks.append(new_track)

    # Save the transposed MIDI file
    new_mid.save(output_file)
    print(f"Transposed MIDI file saved as '{output_file}'")

# Example usage
if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python transpose_midi.py input.mid output.mid 'SourceKey' 'DestinationKey'")
        print("Example: python transpose_midi.py input.mid output.mid 'C major' 'C pentatonic-minor'")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    source_key_str = sys.argv[3]
    dest_key_str = sys.argv[4]

    transpose_midi(input_file, output_file, source_key_str, dest_key_str)