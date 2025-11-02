#!/usr/bin/env python3
import os
import sys
import struct

def read_4cc(f):
    """Read 4 bytes and return them as an ASCII string."""
    return f.read(4).decode('ascii', errors='replace')

def write_4cc(f, fourcc):
    """Write a 4-character ASCII string."""
    f.write(fourcc.encode('ascii'))

def parse_fmt_chunk(data):
    """
    Parse the 'fmt ' chunk data (PCM or float).
    Returns a dict with keys:
      audioFormat, numChannels, sampleRate, byteRate, blockAlign, bitsPerSample
    """
    # Minimum is 16 bytes for PCM; might be more if 'fmt ' is extended
    audioFormat, numChannels, sampleRate, byteRate, blockAlign, bitsPerSample = struct.unpack('<HHIIHH', data[:16])
    return {
        'audioFormat': audioFormat,      # 1=PCM, 3=IEEE float, etc.
        'numChannels': numChannels,
        'sampleRate': sampleRate,
        'byteRate': byteRate,
        'blockAlign': blockAlign,
        'bitsPerSample': bitsPerSample
    }

def parse_smpl_chunk(data):
    """
    Parse the 'smpl' chunk, return the first loop as (startFrame, endFrame), or None if no loops.
    smpl layout (basic):
      Manufacturer   4 bytes
      Product        4 bytes
      SamplePeriod   4 bytes
      MidiUnityNote  4 bytes
      PitchFraction  4 bytes
      SmpteFormat    4 bytes
      SmpteOffset    4 bytes
      NumSampleLoops 4 bytes
      SamplerData    4 bytes
      Then for each loop (24 bytes):
        CuePointID   4
        Type         4
        Start        4
        End          4
        Fraction     4
        PlayCount    4
    """
    if len(data) < 36:
        return None

    # Unpack the first 7 * 4-byte fields
    # We only really need NumSampleLoops (the 8th 4-byte field)
    manufacturer, product, samplePeriod, midiUnity, pitchFraction, smpteFormat, smpteOffset, numLoops, samplerData \
        = struct.unpack('<9I', data[:36])

    if numLoops < 1:
        return None

    # For simplicity, just read the FIRST loop data
    loopOffset = 36
    loopData = data[loopOffset:loopOffset+24]
    if len(loopData) < 24:
        return None

    cuePointID, loopType, startFrame, endFrame, fraction, playCount = struct.unpack('<6I', loopData)
    return (startFrame, endFrame)

def extract_release_from_wav(filename):
    """
    Parses a WAV file’s RIFF chunks, looks for 'smpl' loop data,
    slices audio after loopEnd+1 frames, and writes a new release WAV.
    """
    with open(filename, 'rb') as f:
        # Read main RIFF header
        mainChunkId = read_4cc(f)  # should be "RIFF"
        if mainChunkId != 'RIFF':
            print(f"[SKIP] Not a RIFF file: {filename}")
            return
        riffSizeBytes = struct.unpack('<I', f.read(4))[0]
        waveId = read_4cc(f)       # should be "WAVE"
        if waveId != 'WAVE':
            print(f"[SKIP] Not a WAVE file: {filename}")
            return

        fmtInfo = None
        smplLoop = None
        dataPos = None
        dataSize = 0

        # We'll gather subchunks until we reach the end of file
        fileSize = os.fstat(f.fileno()).st_size

        while f.tell() < fileSize:
            subchunkId = read_4cc(f)
            subchunkSizeBytes = struct.unpack('<I', f.read(4))[0]
            nextPos = f.tell() + subchunkSizeBytes

            if subchunkId == 'fmt ':
                # Parse the fmt chunk
                fmtData = f.read(subchunkSizeBytes)
                fmtInfo = parse_fmt_chunk(fmtData)

            elif subchunkId == 'smpl':
                # Parse the smpl chunk
                smplData = f.read(subchunkSizeBytes)
                smplLoop = parse_smpl_chunk(smplData)

            elif subchunkId == 'data':
                # We'll record where the actual sample data is
                dataPos = f.tell()
                dataSize = subchunkSizeBytes
                # Skip ahead, but let's not read it into memory yet
                f.seek(subchunkSizeBytes, 1)

            else:
                # Skip unknown chunk
                f.seek(subchunkSizeBytes, 1)

            # Move file pointer to the next chunk
            f.seek(nextPos)

        # If no loop data, skip
        if not smplLoop:
            print(f"[SKIP] No loop data: {filename}")
            return

        if not fmtInfo:
            print(f"[SKIP] No fmt chunk found: {filename}")
            return

        if dataPos is None:
            print(f"[SKIP] No data chunk found: {filename}")
            return

    # Now we reopen to read the actual audio
    startFrame, endFrame = smplLoop
    # We'll read from endFrame+1 until the end of the file
    audioFormat = fmtInfo['audioFormat']   # 1=PCM int, 3=float
    numChannels = fmtInfo['numChannels']
    bitsPerSample = fmtInfo['bitsPerSample']  # 32
    sampleRate = fmtInfo['sampleRate']

    bytesPerSample = bitsPerSample // 8
    totalFrames = dataSize // (bytesPerSample * numChannels)

    # Debug prints
    print(f"\nFile: {filename}")
    print(f"  Loop Start (frames): {startFrame}")
    print(f"  Loop End   (frames): {endFrame}")
    print(f"  Total Frames:       {totalFrames}")

    releaseStartFrame = endFrame + 1
    if releaseStartFrame >= totalFrames:
        print(f"[SKIP] Loop end is at/beyond file length: {filename}")
        return

    leftoverFrames = totalFrames - releaseStartFrame
    print(f"  Release frames:     {leftoverFrames}")

    if leftoverFrames <= 0:
        print(f"[SKIP] No leftover release frames: {filename}")
        return

    # Read the relevant portion of the data chunk
    with open(filename, 'rb') as f:
        # move to start of data
        f.seek(dataPos)
        # skip frames up to releaseStartFrame
        skipBytes = releaseStartFrame * numChannels * bytesPerSample
        f.seek(skipBytes, 1)

        # now read leftover
        releaseData = f.read(leftoverFrames * numChannels * bytesPerSample)

    if not releaseData:
        print(f"[SKIP] No samples after loop end: {filename}")
        return

    # Build a brand-new WAV in memory (without smpl)
    # We'll have:
    #   RIFF
    #   WAVE
    #   'fmt ' subchunk
    #   'data' subchunk

    # 1) Construct fmt chunk (16 bytes for PCM/float standard)
    #    Some WAVs have extended fmt, but we’ll assume standard PCM chunk for 32-bit
    byteRate = sampleRate * numChannels * bytesPerSample
    blockAlign = numChannels * bytesPerSample

    # pack the standard 16-byte PCM/float 'fmt '
    # <HHIIHH = 2 + 2 + 4 + 4 + 2 + 2 = 16 bytes
    fmtChunkData = struct.pack('<HHIIHH',
                               audioFormat,
                               numChannels,
                               sampleRate,
                               byteRate,
                               blockAlign,
                               bitsPerSample)

    # 2) data chunk is just leftover audio
    dataChunkSize = len(releaseData)

    # 3) Calculate overall size for RIFF
    #    total = "WAVE" (4 bytes) + "fmt " chunk header(8) + 16 + "data" chunk header(8) + data
    #    We do fileSize - 8 in the RIFF header
    riffTotal = 4 + (8 + len(fmtChunkData)) + (8 + dataChunkSize)
    #   4 bytes: "WAVE"
    #   + 8 + len(fmtChunkData) = subchunk header + chunk data
    #   + 8 + dataChunkSize = subchunk header + chunk data

    # 4) Write out the new file
    base, ext = os.path.splitext(filename)
    outName = base + "_release.wav"

    with open(outName, 'wb') as out:
        # RIFF header
        write_4cc(out, "RIFF")
        out.write(struct.pack('<I', riffTotal))   # file size minus 8
        write_4cc(out, "WAVE")

        # fmt chunk
        write_4cc(out, "fmt ")
        out.write(struct.pack('<I', len(fmtChunkData)))  # chunk size
        out.write(fmtChunkData)

        # data chunk
        write_4cc(out, "data")
        out.write(struct.pack('<I', dataChunkSize))
        out.write(releaseData)

    print(f"[OK] Wrote: {outName}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python extract_release_samples.py <folderPath>")
        sys.exit(1)

    folderPath = sys.argv[1]
    if not os.path.isdir(folderPath):
        print(f"Error: Not a valid folder: {folderPath}")
        sys.exit(1)

    files = [f for f in os.listdir(folderPath) if f.lower().endswith('.wav')]
    if not files:
        print(f"No .wav files found in: {folderPath}")
        return

    for fn in files:
        fullPath = os.path.join(folderPath, fn)
        extract_release_from_wav(fullPath)

if __name__ == "__main__":
    main()