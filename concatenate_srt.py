import glob
import os
from datetime import datetime, timedelta

# Function to parse a timecode string into a datetime object
def parse_timecode(timecode):
    return datetime.strptime(timecode, '%H:%M:%S,%f')

# Function to format a datetime object back into a timecode string
def format_timecode(timecode):
    return datetime.strftime(timecode, '%H:%M:%S,%f')[:-3]

# Function to adjust a timecode by a given timedelta
def adjust_timecode(timecode, delta):
    return format_timecode(parse_timecode(timecode) + delta)

# Function to find the last line containing a timecode in a list of subtitle lines
def find_last_timecode_line(lines):
    for i in range(len(lines) - 1, -1, -1):
        if ' --> ' in lines[i]:
            return lines[i]
    return None

# Function to process each individual subtitle file
def process_subtitle_file(file_path, total_duration, subtitle_index):
    with open(file_path, 'r') as infile:
        lines = infile.readlines()

    adjusted_lines = []
    i = 0
    while i < len(lines):
        # Check if the line is a number (indicating a new subtitle block)
        if lines[i].strip().isdigit():
            # Adjust the subtitle index
            adjusted_lines.append(f"{subtitle_index}\n")
            subtitle_index += 1

            # Extract and adjust timecodes
            if i + 1 < len(lines) and ' --> ' in lines[i+1]:
                start_time, end_time = lines[i+1].strip().split(' --> ')
                adjusted_start_time = adjust_timecode(start_time, total_duration)
                adjusted_end_time = adjust_timecode(end_time, total_duration)
                adjusted_lines.append(f"{adjusted_start_time} --> {adjusted_end_time}\n")
            else:
                # Break processing if the format is unexpected
                print(f"Unexpected format in file: {file_path}, line: {i+1}")
                break

            # Move to the subtitle text and add it to the adjusted lines
            i += 2
            while i < len(lines) and lines[i].strip() != "":
                adjusted_lines.append(lines[i])
                i += 1
            # Add a blank line after each subtitle block
            adjusted_lines.append("\n")
        else:
            # Skip unexpected lines
            i += 1

    return adjusted_lines, subtitle_index

# Main function to concatenate all subtitle files into one
def concatenate_subtitles(base_name, source_directory):
    file_pattern = os.path.join(source_directory, f"{base_name}_*.srt")
    subtitle_files = sorted(glob.glob(file_pattern))

    output_file_path = os.path.join(source_directory, f"{base_name}.srt")

    # Initialize total duration and subtitle index
    total_duration = timedelta(0)
    subtitle_index = 1

    with open(output_file_path, 'w') as outfile:
        for file_path in subtitle_files:
            print(f"Processing file: {file_path}")
            adjusted_lines, subtitle_index = process_subtitle_file(file_path, total_duration, subtitle_index)
            outfile.writelines(adjusted_lines)

            # Update total duration based on the first and last timecode of the current file
            if adjusted_lines:
                last_timecode_line = find_last_timecode_line(adjusted_lines)
                if last_timecode_line:
                    first_start_time = parse_timecode(adjusted_lines[1].strip().split(' --> ')[0])
                    last_end_time = parse_timecode(last_timecode_line.strip().split(' --> ')[1])
                    total_duration += last_end_time - first_start_time
                else:
                    print(f"No valid last timecode line found in file: {file_path}")

    print(f"All subtitles for '{base_name}' concatenated into {output_file_path}")

# Example usage
base_directory = "sources/"
base_name = "eric1"
concatenate_subtitles(base_name, base_directory)
