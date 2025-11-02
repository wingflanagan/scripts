import sys
import struct

def read_chunks(file):
    """Yield (chunk_id, chunk_size, chunk_data) from the file."""
    while True:
        header = file.read(8)
        if len(header) < 8:
            break
        chunk_id, chunk_size = struct.unpack('<4sI', header)
        chunk_data = file.read(chunk_size)
        # If chunk_size is odd, there is an extra pad byte
        if chunk_size % 2 == 1:
            file.read(1)
        yield chunk_id, chunk_size, chunk_data

def main(wav_file):
    with open(wav_file, 'rb') as f:
        # Check the RIFF header
        riff = f.read(12)
        if len(riff) < 12 or riff[0:4] != b'RIFF' or riff[8:12] != b'WAVE':
            print("Not a valid WAVE file")
            return

        found_smpl = False
        for chunk_id, chunk_size, chunk_data in read_chunks(f):
            if chunk_id == b'smpl':
                found_smpl = True
                # The smpl chunk header is 9 unsigned ints (36 bytes)
                if len(chunk_data) < 36:
                    print("Invalid smpl chunk")
                    return

                header = struct.unpack('<9I', chunk_data[:36])
                num_sample_loops = header[7]
                if num_sample_loops == 0:
                    print("no loops")
                    return

                offset = 36
                for i in range(num_sample_loops):
                    if offset + 24 > len(chunk_data):
                        break
                    # Each loop is 6 unsigned ints: cuePointId, type, start, end, fraction, playCount
                    cue_point_id, loop_type, start, end, fraction, play_count = struct.unpack('<6I', chunk_data[offset:offset+24])
                    print(f"Loop {i}: start frame {start}, end frame {end}")
                    offset += 24
                break  # We're done once we find the smpl chunk

        if not found_smpl:
            print("no loops")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py file.wav")
    else:
        main(sys.argv[1])
