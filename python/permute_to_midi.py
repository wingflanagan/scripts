#!/usr/bin/env python3
import argparse
import itertools
import math
import random
from typing import List, Iterable, Tuple, Set, Union

try:
    import mido
except ImportError:
    raise SystemExit("Missing dependency: install with `pip install mido`")

NOTE_BASES = {
    'C': 0,  'C#': 1, 'Db': 1,
    'D': 2,  'D#': 3, 'Eb': 3,
    'E': 4,  'Fb': 4, 'E#': 5,  # enharmonics for the pedants
    'F': 5,  'F#': 6, 'Gb': 6,
    'G': 7,  'G#': 8, 'Ab': 8,
    'A': 9,  'A#': 10, 'Bb': 10,
    'B': 11, 'Cb': 11, 'B#': 0
}

def parse_note(token: str) -> int:
    """Parse a note name like C4, D#3, Gb5 or a MIDI number string."""
    token = token.strip()
    # MIDI number path
    if token.isdigit() or (token.startswith('-') and token[1:].isdigit()):
        n = int(token)
        if not (0 <= n <= 127):
            raise ValueError(f"MIDI note out of range 0–127: {n}")
        return n
    # Name path
    # Split pitch class vs octave (last chars are digits, possibly negative)
    i = len(token) - 1
    while i >= 0 and token[i].isdigit():
        i -= 1
    if i < 0:
        raise ValueError(f"Bad note token: {token}")
    pitch = token[:i+1].replace('♯', '#').replace('♭', 'b').upper()
    octave_str = token[i+1:]
    if octave_str == '':
        raise ValueError(f"Missing octave in note: {token}")
    if pitch not in NOTE_BASES:
        raise ValueError(f"Unrecognized pitch class: {pitch}")
    octave = int(octave_str)
    midi = 12 * (octave + 1) + NOTE_BASES[pitch]
    if not (0 <= midi <= 127):
        raise ValueError(f"Computed MIDI note out of range for {token}: {midi}")
    return midi

def parse_notes(tokens: List[str]) -> List[int]:
    notes = [parse_note(t) for t in tokens]
    if len(set(notes)) != len(notes):
        # permutations of duplicates collapse; warn to avoid surprises
        print("Warning: duplicate notes provided; total unique permutations will be reduced.")
    return notes

def bpm_to_tempo(bpm: float) -> int:
    return mido.bpm2tempo(bpm)

def quarter_note_ticks(ticks_per_beat: int) -> int:
    return ticks_per_beat

def gap_ticks(ticks_per_beat: int, gap_beats: float) -> int:
    return int(round(ticks_per_beat * gap_beats))

def iter_first_permutations(notes: List[int], limit: int) -> Iterable[Tuple[int, ...]]:
    count = math.factorial(len(set(notes))) if len(notes) <= 10 else limit
    # itertools.permutations respects duplicates by position; we want unique tuples
    seen: Set[Tuple[int, ...]] = set()
    for p in itertools.permutations(notes):
        if p in seen:
            continue
        seen.add(p)
        yield p
        if limit and len(seen) >= limit:
            break

def iter_all_permutations(notes: List[int]) -> Iterable[Tuple[int, ...]]:
    seen: Set[Tuple[int, ...]] = set()
    for p in itertools.permutations(notes):
        if p in seen:
            continue
        seen.add(p)
        yield p

def iter_random_unique_permutations(notes: List[int], limit: int, seed: Union[int, None]) -> Iterable[Tuple[int, ...]]:
    rng = random.Random(seed)
    # To avoid generating all n! upfront, sample by shuffling until unique set reaches limit
    # For n≤10 and modest limits this is fine.
    seen: Set[Tuple[int, ...]] = set()
    base = notes[:]
    while len(seen) < limit:
        rng.shuffle(base)
        t = tuple(base)
        if t not in seen:
            seen.add(t)
            yield t

def write_permutations_to_midi(perms: Iterable[Tuple[int, ...]],
                               out_path: str,
                               bpm: float = 120.0,
                               velocity: int = 96,
                               gap_beats: float = 0.0,
                               ticks_per_beat: int = 480) -> None:
    mid = mido.MidiFile(ticks_per_beat=ticks_per_beat)
    track = mido.MidiTrack()
    mid.tracks.append(track)

    track.append(mido.MetaMessage('set_tempo', tempo=bpm_to_tempo(bpm), time=0))
    q_ticks = quarter_note_ticks(ticks_per_beat)
    g_ticks = gap_ticks(ticks_per_beat, gap_beats)

    for perm in perms:
        # each note: quarter note
        for idx, n in enumerate(perm):
            # note on
            track.append(mido.Message('note_on', note=n, velocity=velocity, time=0))
            # note off after a quarter note
            track.append(mido.Message('note_off', note=n, velocity=0, time=q_ticks))
        # add gap between permutations (as rest)
        if g_ticks > 0:
            # easiest rest is a zero-velocity note on of a dummy pitch followed by time,
            # but better is simply a delta time with no events. Mido requires time on a message.
            # We'll add a zero-length meta message to carry the rest time.
            track.append(mido.MetaMessage('marker', text='perm_sep', time=g_ticks))

    mid.save(out_path)

def main():
    ap = argparse.ArgumentParser(
        description="Generate a MIDI file containing permutations of input notes as quarter notes."
    )
    ap.add_argument('notes', nargs='+',
                    help="Note names like C4, D#4, Gb3 or MIDI numbers 0–127. Up to ~10 unique notes.")
    ap.add_argument('-o', '--out', default='permutations.mid', help="Output MIDI file path.")
    ap.add_argument('--bpm', type=float, default=120.0, help="Tempo in BPM (default 120).")
    ap.add_argument('--velocity', type=int, default=96, help="Note velocity 1–127 (default 96).")
    ap.add_argument('--gap-beats', type=float, default=0.0, help="Rest between permutations in beats (e.g., 0.25).")
    ap.add_argument('--ticks-per-beat', type=int, default=480, help="PPQ (default 480).")
    ap.add_argument('--mode', choices=['first', 'all', 'random'], default='first',
                    help="Which permutations to generate: first (lexicographic), all, random.")
    ap.add_argument('--limit', type=int, default=10000,
                    help="Max permutations to write (ignored for mode=all). Default 10000.")
    ap.add_argument('--seed', type=int, default=None, help="Random seed for mode=random.")
    ap.add_argument('--chunk-size', type=int, default=0,
                    help="If >0, split output into multiple files with this many permutations each.")
    ap.add_argument('--basename', default='permutations',
                    help="Base filename when chunking (e.g., permutations_0001.mid).")

    args = ap.parse_args()

    notes = parse_notes(args.notes)
    uniq = len(set(notes))
    if uniq == 0:
        raise SystemExit("No notes parsed. Try again with something that makes sound.")

    if uniq > 10:
        print("Warning: more than 10 unique notes will create a ridiculous number of permutations. Proceeding anyway.")

    def perm_iter() -> Iterable[Tuple[int, ...]]:
        if args.mode == 'all':
            return iter_all_permutations(notes)
        elif args.mode == 'random':
            if args.limit <= 0:
                raise SystemExit("--limit must be > 0 for mode=random")
            return iter_random_unique_permutations(notes, args.limit, args.seed)
        else:
            # first
            limit = max(args.limit, 1) if args.limit is not None else 10000
            return iter_first_permutations(notes, limit)

    # Handle chunking without buffering everything in RAM
    if args.chunk_size and args.chunk_size > 0:
        gen = perm_iter()
        chunk_idx = 1
        done = 0
        while True:
            batch = list(itertools.islice(gen, args.chunk_size))
            if not batch:
                break
            fname = f"{args.basename}_{chunk_idx:04d}.mid"
            write_permutations_to_midi(
                batch,
                out_path=fname,
                bpm=args.bpm,
                velocity=args.velocity,
                gap_beats=args.gap_beats,
                ticks_per_beat=args.ticks_per_beat
            )
            print(f"Wrote {len(batch)} permutations to {fname}")
            done += len(batch)
            chunk_idx += 1
        if done == 0:
            print("No permutations written. Check your inputs.")
    else:
        # Single file path
        perms = list(perm_iter()) if args.mode != 'all' else perm_iter()
        out_path = args.out
        write_permutations_to_midi(
            perms,
            out_path=out_path,
            bpm=args.bpm,
            velocity=args.velocity,
            gap_beats=args.gap_beats,
            ticks_per_beat=args.ticks_per_beat
        )
        print(f"Wrote permutations to {out_path}")

if __name__ == '__main__':
    main()