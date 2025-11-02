import argparse
from music21 import converter, instrument, note, chord, stream, key, meter, tempo, duration

def parse_arguments():
    parser = argparse.ArgumentParser(description="Harmonize a monophonic MIDI file for piano with 'oom-pah' accompaniment.")
    parser.add_argument("input_file", help="Path to the input MIDI file containing a single melodic line.")
    parser.add_argument("output_file", help="Path to the output harmonized MIDI file.")
    parser.add_argument("key", help="Diatonic key (e.g., 'C major', 'A minor').")
    parser.add_argument("--tremolo", action="store_true", help="Include octave tremolos for longer held notes at phrase ends.")
    return parser.parse_args()

def get_diatonic_chords(k):
    """Return a list of diatonic triads based on the key."""
    diatonic = k.getPitches()
    scale_degree = ['I', 'ii', 'iii', 'IV', 'V', 'vi', 'vii°']
    chords = []
    for i in range(7):
        triad = chord.Chord([diatonic[i], diatonic[(i+2)%7], diatonic[(i+4)%7]])
        triad.closedPosition(forceOctave=4, inPlace=True)
        triad.commonName = scale_degree[i]
        chords.append(triad)
    return chords

def assign_chords(melody_part, k, ts):
    """Assign a chord to each measure based on the melody note on the strong beat."""
    chords_assigned = []
    for measure in melody_part.getElementsByClass(stream.Measure):
        if ts.beatCount == 3:
            # In 3/4, beat 1 is strong
            strong_beats = [1]
        elif ts.beatCount == 4:
            # In 4/4, beats 1 and 3 are strong
            strong_beats = [1, 3]
        else:
            # Default to first beat
            strong_beats = [1]

        # Find melody notes on strong beats
        strong_notes = []
        for n in measure.notes:
            if n.beat in strong_beats:
                strong_notes.append(n)

        # Determine the chord based on strong notes
        if strong_notes:
            # Take the pitch of the first strong note
            melody_note = strong_notes[0].pitch
            # Find the chord that contains this note
            possible_chords = []
            for c in get_diatonic_chords(k):
                if melody_note.name in [p.name for p in c.pitches]:
                    possible_chords.append(c)
            if possible_chords:
                # Prefer I, IV, V
                preferred = ['I', 'IV', 'V']
                selected = None
                for name in preferred:
                    for c in possible_chords:
                        if c.commonName == name:
                            selected = c
                            break
                    if selected:
                        break
                if not selected:
                    selected = possible_chords[0]
                chords_assigned.append(selected)
            else:
                # Default to I if no chord contains the melody note
                chords_assigned.append(get_diatonic_chords(k)[0])
        else:
            # Default to I if no strong notes
            chords_assigned.append(get_diatonic_chords(k)[0])
    return chords_assigned

def create_accompaniment(chords_assigned, ts, tremolo_flag, melody_part):
    """Create accompaniment stream with bass and chords based on the assigned chords."""
    accompaniment = stream.Part()
    accompaniment.insert(0, instrument.Piano())

    # Create Bass and Chord streams
    bass_stream = stream.Part()
    bass_stream.insert(0, instrument.Piano())
    chord_stream = stream.Part()
    chord_stream.insert(0, instrument.Piano())

    measure_number = 0
    for measure in melody_part.getElementsByClass(stream.Measure):
        current_chord = chords_assigned[measure_number]
        measure_duration = measure.duration.quarterLength
        beats = ts.beatCount

        if beats == 4:
            # "oom-pah-pah" rhythm
            rhythm = [("bass", 1), ("chord", 1), ("chord", 1)]
        elif beats == 3:
            # "oom-pah-pah" rhythm for 3/4
            rhythm = [("bass", 1), ("chord", 1), ("chord", 1)]
        else:
            # Default to "oom-pah"
            rhythm = [("bass", 1), ("chord", 1)]

        beat_length = measure_duration / beats
        offset = measure.offset

        for r in rhythm:
            part, dur = r
            n = None
            if part == "bass":
                # Bass note is the root of the chord
                n = note.Note(current_chord.root().name)
                n.octave = 2  # Lower octave for bass
            elif part == "chord":
                # Add full chord
                c = chord.Chord(current_chord)
                c.octave = 4
                n = c
            if n:
                n.duration = duration.Duration(dur * beat_length)
                n.offset = offset
                if tremolo_flag and part == "chord":
                    # Check if this is the last chord in the measure and held
                    if is_phrase_end(measure):
                        apply_tremolo(n)
                if part == "bass":
                    bass_stream.insert(offset, n)
                else:
                    chord_stream.insert(offset, n)
            offset += dur * beat_length
        measure_number += 1

    accompaniment.insert(0, bass_stream)
    accompaniment.insert(0, chord_stream)
    return accompaniment

def is_phrase_end(measure):
    """Determine if a measure is at the end of a phrase based on held notes."""
    # Simple heuristic: if the last note is held longer than or equal to 2 beats
    last_note = measure.notes[-1]
    return last_note.duration.quarterLength >= 2  # Example threshold

def apply_tremolo(n):
    """Convert a note or chord into an octave tremolo."""
    if isinstance(n, chord.Chord):
        pitches = []
        for p in n.pitches:
            pitches.append(p)
            p_octave_up = p.transpose(12)  # Up an octave
            pitches.append(p_octave_up)
        tremolo_chord = chord.Chord(pitches)
        tremolo_chord.duration = n.duration
        n.activeSite.replace(n, tremolo_chord)
    elif isinstance(n, note.Note):
        p = n.pitch
        p_octave_up = p.transpose(12)
        tremolo_chord = chord.Chord([p, p_octave_up])
        tremolo_chord.duration = n.duration
        n.activeSite.replace(n, tremolo_chord)

def main():
    args = parse_arguments()

    # Split the key into tonic and mode
    key_parts = args.key.strip().split()
    if len(key_parts) == 1:
        tonic = key_parts[0]
        mode = 'major'  # Default to major if mode not specified
    elif len(key_parts) == 2:
        tonic, mode = key_parts
    else:
        raise ValueError("Key must be in the format 'D major' or 'A minor'.")

    # Validate mode
    mode = mode.lower()
    if mode not in ['major', 'minor']:
        raise ValueError("Mode must be 'major' or 'minor'.")

    # Create the key object
    user_key = key.Key(tonic, mode)

    # Load the melody
    melody = converter.parse(args.input_file)
    melody_part = melody.parts[0]

    melody_part.insert(0, user_key)

    # Determine time signature
    ts = melody_part.getTimeSignatures()[0] if melody_part.getTimeSignatures() else meter.TimeSignature('4/4')

    # Assign chords
    chords_assigned = assign_chords(melody_part, user_key, ts)

    # Create accompaniment
    accompaniment = create_accompaniment(chords_assigned, ts, args.tremolo, melody_part)

    # Combine melody and accompaniment
    piano = stream.Stream()
    piano.append(melody_part)
    piano.append(accompaniment)

    # Set instrument to Piano
    piano.insert(0, instrument.Piano())

    # Write to MIDI
    piano.write('midi', fp=args.output_file)
    print(f"Harmonized MIDI file saved as {args.output_file}")

if __name__ == "__main__":
    main()