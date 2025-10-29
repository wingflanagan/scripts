from pydub import AudioSegment

def concatenate_mp3(files_list, output_file):
    """
    Concatenate a list of MP3 files into a single file after optionally trimming them.

    Args:
    files_list (list of tuples): List of tuples, each containing the file path 
                                 to an MP3 file and a tuple of two integers representing 
                                 the start and end trim times in milliseconds.
    output_file (str): The path to the output MP3 file.
    """

    # Initialize an empty AudioSegment object for concatenation
    combined = AudioSegment.silent(duration=0)

    # Loop through each file and its specified start and end trim times
    for file_path, (start_trim, end_trim) in files_list:
        # Tell us what's doin'
        print(f"Processing {file_path}...")

        # Load the MP3 file
        track = AudioSegment.from_file(file_path, format="mp3")

        # Check if trimming is needed
        if start_trim != 0 or end_trim != 0:
            # Trim the audio from start_trim to end_trim
            track = track[start_trim:end_trim]

        # Concatenate to the combined file
        combined += track

    # Export the combined file
    print(f"Exporting {output_file} (this may take a while)...")
    combined.export(output_file, format="mp3")

# Example usage
files_to_combine = [
    # ("file1.mp3", (1000, 3000)),  # Trims from 1 to 3 seconds
    # ("file2.mp3", (2000, 5000)),  # Trims from 2 to 5 seconds
    # ("file3.mp3", (0, 4000)),     # Trims from start to 4 seconds
    # ("file4.mp3", (0, 0))         # No trimming, includes the entire file
    ("/home/wingf/temp/gunslinger_001.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_002.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_003.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_004.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_005.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_006.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_007.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_008.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_009.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_010.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_011.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_012.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_013.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_014.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_015.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_016.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_017.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_018.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_019.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_020.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_021.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_022.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_023.mp3", (0, 314000)),
    ("/home/wingf/temp/gunslinger_024.mp3", (4500, 168960)),
    ("/home/wingf/temp/gunslinger_025.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_026.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_027.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_028.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_029.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_030.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_031.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_032.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_033.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_034.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_035.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_036.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_037.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_038.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_039.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_040.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_041.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_042.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_043.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_044.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_045.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_046.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_047.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_048.mp3", (0, 324000)),
    ("/home/wingf/temp/gunslinger_049.mp3", (4000, 233822)),
    ("/home/wingf/temp/gunslinger_050.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_051.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_052.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_053.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_054.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_055.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_056.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_057.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_058.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_059.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_060.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_061.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_062.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_063.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_064.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_065.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_066.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_067.mp3", (0, 172000)),
    ("/home/wingf/temp/gunslinger_068.mp3", (4000, 240562)),
    ("/home/wingf/temp/gunslinger_069.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_070.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_071.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_072.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_073.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_074.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_075.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_076.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_077.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_078.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_079.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_080.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_081.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_082.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_083.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_084.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_085.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_086.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_087.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_088.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_089.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_090.mp3", (0, 223000)),
    ("/home/wingf/temp/gunslinger_091.mp3", (5000, 222642)),
    ("/home/wingf/temp/gunslinger_092.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_093.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_094.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_095.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_096.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_097.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_098.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_099.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_100.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_101.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_102.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_103.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_104.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_105.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_106.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_107.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_108.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_109.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_110.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_111.mp3", (0, 200000)),
    ("/home/wingf/temp/gunslinger_112.mp3", (4000, 158955)),
    ("/home/wingf/temp/gunslinger_113.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_114.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_115.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_116.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_117.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_118.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_119.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_120.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_121.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_122.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_123.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_124.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_125.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_126.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_127.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_128.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_129.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_130.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_131.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_132.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_133.mp3", (0, 0)),
    ("/home/wingf/temp/gunslinger_134.mp3", (0, 0))
]

output_file_name = "/home/wingf/temp/02_the-gunslinger.mp3"
concatenate_mp3(files_to_combine, output_file_name)
print("Done!")