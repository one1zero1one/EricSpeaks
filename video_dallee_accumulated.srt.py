import os
from datetime import datetime, timedelta

def parse_timecode(timecode):
    return datetime.strptime(timecode, '%H:%M:%S,%f')

def format_timecode(timecode):
    return datetime.strftime(timecode, '%H:%M:%S,%f')[:-3]

def process_subtitles_for_accumulation(input_file_path, output_file_path, interval=timedelta(minutes=1)):
    with open(input_file_path, 'r') as infile:
        lines = infile.readlines()

    accumulated_text = ''
    last_timecode = None
    subtitle_index = 1
    accumulated_subtitles = []

    for i in range(0, len(lines), 4):
        if i + 1 < len(lines) and ' --> ' in lines[i+1]:
            start_time, _ = lines[i+1].strip().split(' --> ')
            current_time = parse_timecode(start_time)

            if last_timecode is None:
                last_timecode = current_time  # Initialize last_timecode at the start of the first block

            if current_time - last_timecode < interval:
                accumulated_text += lines[i+2].strip() + ' '
            else:
                # Append the accumulated text to the list
                start = format_timecode(last_timecode)
                end = format_timecode(current_time)  # Use current_time as the end of the interval
                accumulated_subtitles.append(f"{subtitle_index}\n{start} --> {end}\n{accumulated_text}\n\n")
                subtitle_index += 1
                accumulated_text = lines[i+2].strip() + ' '
                last_timecode = current_time

    # Add the final accumulation
    if accumulated_text:
        start = format_timecode(last_timecode)
        end = format_timecode(last_timecode + interval)
        accumulated_subtitles.append(f"{subtitle_index}\n{start} --> {end}\n{accumulated_text}\n\n")

    # Write the accumulated subtitles to the output file
    with open(output_file_path, 'w') as outfile:
        outfile.writelines(accumulated_subtitles)

    print(f"Processed subtitles written to {output_file_path}")

# Example usage
input_file_path = "sources/eric1.srt"
output_file_path = "sources/eric1_accumulated.srt"
process_subtitles_for_accumulation(input_file_path, output_file_path)
