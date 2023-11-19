from pydub import AudioSegment
import os
import sys

input_file = sys.argv[1]
song = AudioSegment.from_mp3(input_file)

# PyDub handles time in milliseconds
ten_minutes = 10 * 60 * 1000
total_duration = len(song)

print(f"Total duration: {total_duration/1000/60}m")
print(f"Total chunks: {total_duration // ten_minutes + 1}")
print(f"Chunk duration: {ten_minutes/1000}s")

for i in range(0, total_duration, ten_minutes):
    chunk_filename = f"sources/eric1_{i//ten_minutes}.mp3"
    if os.path.exists(chunk_filename):
        print(f"Chunk {chunk_filename} already exists. Exiting.")
        sys.exit(1)
    print(f"Exporting chunk {i//ten_minutes}")
    chunk = song[i:i+ten_minutes]
    chunk.export(chunk_filename, format="mp3")
