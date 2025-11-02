import mido
from mido import MidiFile, MidiTrack, Message

# Helper function to add notes to the track
def add_note(track, note, velocity, time, duration, channel=0):
    track.append(Message('note_on', note=note, velocity=velocity, time=time, channel=channel))
    track.append(Message('note_off', note=note, velocity=velocity, time=duration, channel=channel))

# Create a new MIDI file and track
mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)

# Set tempo (optional, use your 93.2 BPM)
tempo = 643777  # microseconds per quarter note for 93.2 BPM
track.append(Message('program_change', program=33, time=0))  # Program 33: Acoustic Bass

# Define chord progression and their corresponding bassline (fifth + approach notes)
chords = [
    ('G', [50, 57]),      # Fifth (D), approach (A)
    ('Bb', [53, 58]),     # Fifth (F), approach (C)
    ('D', [45, 54]),      # Fifth (A), approach (B)
    ('C', [43, 55]),      # Fifth (G), approach (E)
    ('Fmaj7(13)', [48, 50]), # Sixth (D), approach (E)
    ('D', [45, 54]),      # Fifth (A), approach (B)
    ('C', [43, 55]),      # Fifth (G), approach (B)
    ('Am', [40, 47]),     # Fifth (E), approach (G)
    ('D7', [45, 56]),     # Seventh (C), approach (G#)
    ('A', [40, 52]),      # Fifth (E), approach (B)
    ('C', [43, 55]),      # Fifth (G), approach (B)
    ('Caug', [43, 56]),   # Augmented Fifth (G#), approach (A)
    ('Bm7', [42, 47]),    # Seventh (A), approach (C)
    ('Bb7', [53, 58]),    # Seventh (Ab), approach (A)
    ('Bbaug7', [53, 56]), # Augmented Fifth (D), approach (C)
    ('D', [45, 54]),      # Fifth (A), approach (C#)
    ('Bdmmaj7(9)', [46, 54]),  # Maj7 (A#), approach (C#)
    ('D', [45, 54]),      # Fifth (A), approach (C#)
    ('D', [45, 54]),      # Fifth (A), approach (C#)
    ('D', [45, 54]),      # Fifth (A), approach (C#)
    ('A7', [40, 46]),     # Seventh (G), approach (B)
    ('Bbdim', [46, 55]),  # Diminished fifth (E), approach (C)
    ('Cadd9', [43, 50]),  # Ninth (D), approach (B)
    ('D', [45, 54]),      # Fifth (A), approach (C#)
    ('Fmaj7(13)', [48, 50]),  # Sixth (D), approach (E)
    ('Dmmaj7(9)', [45, 54]),  # Maj7 (C#), approach (E)
    ('Fmaj7(13)', [48, 50]),  # Sixth (D), approach (E)
    ('G7', [50, 57]),     # Seventh (F), approach (F#)
    ('G7', [50, 57]),     # Seventh (F), approach (F#)
    ('Fmaj7(13)', [48, 50]),  # Sixth (D), approach (E)
    ('G7', [50, 57]),     # Seventh (F), approach (F#)
    ('Dmmaj7(9)', [45, 54]),  # Maj7 (C#), approach (E)
    ('Fmaj7(13)', [48, 50]),  # Sixth (D), approach (E)
]

# Time variables (assuming 3/4 time signature)
quarter_note_time = 480  # Standard quarter note duration for MIDI
eighth_note_time = quarter_note_time // 2
triplet_note_time = quarter_note_time * 2 // 3  # Quarter-note triplet duration
measure_time = 3 * quarter_note_time  # each measure is 3 quarter notes long

# Add notes for each chord, skipping beat 1, and adding triplet variation every 8 bars
for i, chord in enumerate(chords):
    if (i + 1) % 8 == 0:  # Triplet variation every 8th measure
        # Quarter-note triplet starting on beat 2
        add_note(track, chord[1][0], 64, quarter_note_time, triplet_note_time)  # First triplet note
        add_note(track, chord[1][1], 64, 0, triplet_note_time)  # Second triplet note
        add_note(track, chord[1][0], 64, 0, triplet_note_time)  # Third triplet note
    else:
        # Standard pattern: rest on beat 1, notes on beats 2 and 3
        add_note(track, chord[1][0], 64, quarter_note_time, quarter_note_time)  # Fifth on beat 2
        add_note(track, chord[1][1], 64, quarter_note_time, quarter_note_time)  # Approach on beat 3

# Save the generated MIDI file
mid.save('jazz_bass_pattern_triplet_variation.mid')
