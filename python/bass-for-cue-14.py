from midiutil import MIDIFile
import random
import re

# Note names and their semitones
NOTE_NAMES = {
    'C': 0,
    'C#': 1, 'Db': 1,
    'D': 2,
    'D#': 3, 'Eb': 3,
    'E': 4,
    'F': 5,
    'F#': 6, 'Gb': 6,
    'G': 7,
    'G#': 8, 'Ab': 8,
    'A': 9,
    'A#': 10, 'Bb': 10,
    'B': 11, 'Cb': 11,
}

# D minor scale degrees
D_MINOR_SCALE = [2, 4, 5, 7, 9, 10, 0]  # D, E, F, G, A, Bb, C

# Chord formulas
CHORD_FORMULAS = {
    'maj': [0, 4, 7],
    'min': [0, 3, 7],
    '7': [0, 4, 7, 10],
    'maj7': [0, 4, 7, 11],
    'min7': [0, 3, 7, 10],
    'dim': [0, 3, 6],
    'aug': [0, 4, 8],
    'mmaj7': [0, 3, 7, 11],
    'dim7': [0, 3, 6, 9],
    'aug7': [0, 4, 8, 10],
}

def get_midi_note_number(note_name, octave):
    semitone = NOTE_NAMES[note_name]
    midi_number = (octave + 1) * 12 + semitone
    return midi_number

def parse_chord_name(chord_name):
    pattern = r'^([A-G][b#]?)(.*)$'
    match = re.match(pattern, chord_name)
    if match:
        root = match.group(1)
        chord_type = match.group(2)
        return root, chord_type
    else:
        return None, None

def get_chord_tones(root, chord_type):
    chord_type = chord_type.strip()
    intervals = []
    if chord_type == '':
        intervals = CHORD_FORMULAS['maj']
    elif chord_type.startswith('mmaj7'):
        intervals = CHORD_FORMULAS['mmaj7']
    elif chord_type.startswith('maj7'):
        intervals = CHORD_FORMULAS['maj7']
    elif chord_type.startswith('m7'):
        intervals = CHORD_FORMULAS['min7']
    elif chord_type.startswith('m'):
        intervals = CHORD_FORMULAS['min']
    elif chord_type.startswith('dim7'):
        intervals = CHORD_FORMULAS['dim7']
    elif chord_type.startswith('dim'):
        intervals = CHORD_FORMULAS['dim']
    elif chord_type.startswith('aug7'):
        intervals = CHORD_FORMULAS['aug7']
    elif chord_type.startswith('aug'):
        intervals = CHORD_FORMULAS['aug']
    elif chord_type.startswith('7'):
        intervals = CHORD_FORMULAS['7']
    else:
        intervals = CHORD_FORMULAS['maj']

    # Handle extensions
    if '(' in chord_type and ')' in chord_type:
        extensions = chord_type[chord_type.find('(')+1:chord_type.find(')')]
        for ext in extensions.split(','):
            ext = ext.strip()
            if ext == '9':
                intervals.append(14)
            elif ext == '13':
                intervals.append(21)
            elif ext == 'b9':
                intervals.append(13)
            elif ext == '#9':
                intervals.append(15)
            elif ext == '11':
                intervals.append(17)
            elif ext == '#11':
                intervals.append(18)

    root_semitone = NOTE_NAMES[root]
    chord_tones = [(root_semitone + interval) % 12 for interval in intervals]
    return chord_tones

# Chord progression
chord_progression = [
    'G',
    'Bb',
    'D',
    'C',
    'Fmaj7(13)',
    'D',
    'C',
    'Am',
    'D7',
    'A',
    'C',
    'Caug',
    'Bm7',
    'Bb7',
    'Bbaug7',
    'D',
    'Bdmmaj7(9)',
    'D',
    'D',
    'D',
    'A7',
    'Bbdim',
    'Cadd9',
    'D',
    'Fmaj7(13)',
    'Dmmaj7(9)',
    'Fmaj7(13)',
    'G7',
    'G7',
    'Fmaj7(13)',
    'G7',
    'Dmmaj7(9)',
    'Fmaj7(13)',
]

# Break measures
break_bars = [8, 16, 24, 32]
break_measures = set(break_bars)

# Initialize MIDI file
tempo = 128.7
midi = MIDIFile(1)
midi.addTempo(0, 0, tempo)
midi.addProgramChange(0, 0, 0, 33)  # Acoustic Bass

# Base unit is a sixteenth note (0.25 beats)
BASE_UNIT = 0.25

# Note durations in units (multiples of BASE_UNIT)
NOTE_DURATIONS = {
    'sixteenth': 1,      # 0.25 beats
    'eighth': 2,         # 0.5 beats
    'quarter': 4,        # 1.0 beat
    'half': 8,           # 2.0 beats
    'whole': 16,         # 4.0 beats
}

# Define rhythm patterns in units (summing to 16 units per measure)
rhythm_patterns = [
    [4, 4, 4, 4],            # Four quarter notes
    [2, 2, 4, 8],            # Two eighths, quarter, half note
    [2, 2, 2, 2, 8],         # Four eighths, half note
    [4, 2, 2, 8],            # Quarter, two eighths, half note
    [2, 4, 2, 8],            # Eighth, quarter, eighth, half note
    [2, 2, 2, 2, 2, 2, 2, 2],# Eight eighth notes
    [1, 1, 1, 1, 4, 8],      # Four sixteenths, quarter, half note
]

current_time_units = 0  # Start time in units

for i, chord_name in enumerate(chord_progression):
    measure_number = i + 1  # Measures start at 1
    if measure_number in break_measures:
        # Skip this measure, as it will be replaced by a break
        current_time_units += 16  # Advance time by one measure (16 units)
        continue

    root, chord_type = parse_chord_name(chord_name)
    if root is None:
        current_time_units += 16  # Advance time even if chord parsing fails
        continue
    chord_tones = get_chord_tones(root, chord_type)
    octave = 2  # Bass octave

    # Generate rhythm pattern
    rhythm = random.choice(rhythm_patterns)
    total_units = sum(rhythm)
    # Adjust the last note duration to fit exactly 16 units (4 beats)
    rhythm[-1] += 16 - total_units

    notes = []
    # First note is the root note
    root_midi = get_midi_note_number(root, octave)
    notes.append(root_midi)

    # For the remaining beats, choose chord tones or D minor scale notes
    available_notes = chord_tones.copy()
    if len(available_notes) < 3:
        # If not enough chord tones, use D minor scale notes
        available_notes.extend(D_MINOR_SCALE)
    # Remove duplicates and sort
    available_notes = sorted(list(set(available_notes)))

    while len(notes) < len(rhythm):
        note_options = [n for n in available_notes if n != (notes[-1] % 12)]
        if not note_options:
            note_options = [n for n in D_MINOR_SCALE if n != (notes[-1] % 12)]
        if not note_options:
            # As a last resort, allow repeated notes
            note_options = available_notes
        next_note = random.choice(note_options)
        note_midi = (octave * 12) + next_note
        # Avoid repeated notes
        if note_midi != notes[-1]:
            notes.append(note_midi)
        else:
            # Try again if the note is the same as the previous one
            continue

    # Add notes to MIDI track with the generated rhythm
    current_time = current_time_units * BASE_UNIT  # Convert units to beats
    for j, note in enumerate(notes):
        duration_units = rhythm[j]
        duration_beats = duration_units * BASE_UNIT
        midi.addNote(0, 0, note, current_time, duration_beats, 100)
        current_time += duration_beats

    current_time_units += 16  # Move to the next measure (16 units)

# Break patterns
def generate_break(time_units, intense=False):
    current_time = time_units * BASE_UNIT
    if intense:
        # Use sixteenth notes for intensity
        durations = [1] * 16  # 16 sixteenth notes (1 unit each)
        start_note = get_midi_note_number('D', 3)
        for i, duration_units in enumerate(durations):
            duration_beats = duration_units * BASE_UNIT
            note = start_note + i  # Ascending chromatic scale
            midi.addNote(0, 0, note, current_time, duration_beats, 100)
            current_time += duration_beats
    else:
        # Use eighth notes
        durations = [2] * 8  # 8 eighth notes (2 units each)
        start_note = get_midi_note_number('A', 2)
        for i, duration_units in enumerate(durations):
            duration_beats = duration_units * BASE_UNIT
            note = start_note - i  # Descending chromatic
            midi.addNote(0, 0, note, current_time, duration_beats, 100)
            current_time += duration_beats

break_bars = [8, 16, 24, 32]
for bar in break_bars:
    break_time_units = (bar - 1) * 16  # Each measure is 16 units
    intense = bar in [16, 32]
    generate_break(break_time_units, intense)

# Write MIDI file
with open("walking_bass.mid", "wb") as output_file:
    midi.writeFile(output_file)