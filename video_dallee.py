
from datetime import datetime
from PIL import Image
import subprocess
import sys
import os

def create_video_segment(image_path, duration, output_path):
    """Create a video segment from an image for the specified duration."""
    command = [
        'ffmpeg',
        '-loop', '1',
        '-i', image_path,
        '-c:v', 'libx264',
        '-t', str(duration),
        '-pix_fmt', 'yuv420p',
        output_path
    ]
    subprocess.run(command)

def concatenate_videos(video_files, output_file):
    """Concatenate a list of video files into a single video."""
    with open('filelist.txt', 'w') as filelist:
        for video_file in video_files:
            filelist.write(f"file '{video_file}'\n")

    command = [
        'ffmpeg',
        '-f', 'concat',
        '-safe', '0',
        '-i', 'filelist.txt',
        '-c', 'copy',
        output_file
    ]
    subprocess.run(command)

def get_duration(start_time, end_time):
    """Calculate duration in seconds from two time strings."""
    time_format = "%H:%M:%S,%f"
    start = datetime.strptime(start_time, time_format)
    end = datetime.strptime(end_time, time_format)
    return (end - start).total_seconds()

def create_video_with_images_and_audio(source_directory, base_name):
    audio_file = os.path.join(source_directory, f"{base_name}.mp3")
    subtitle_file = os.path.join(source_directory, f"{base_name}_image_prompts.srt")
    final_subtitle_file = os.path.join(source_directory, f"{base_name}.srt")
    image_folder = os.path.join(source_directory, f"{base_name}_images")
    output_video_file = os.path.join(source_directory, f"{base_name}_with_subtitles_and_images.mp4")

    # Read the subtitle file and create video segments
    video_segments = []
    with open(subtitle_file, 'r') as file:
        lines = file.readlines()
        for i in range(0, len(lines), 4):
            if i + 1 < len(lines):
                segment_output = os.path.join(source_directory, f"segment_{i//4}.mp4")
                
                # Check if segment already exists
                if not os.path.exists(segment_output):
                    start_time, end_time = lines[i+1].strip().split(' --> ')
                    duration = get_duration(start_time, end_time)
                    image_path = os.path.join(image_folder, f"{i//4}.jpg")
                    create_video_segment(image_path, duration, segment_output)

                video_segments.append(segment_output)

    # Concatenate all video segments
    concatenated_video = os.path.join(source_directory, "concatenated.mp4")
    concatenate_videos(video_segments, concatenated_video)

    # Add audio and subtitles to the concatenated video
    command = [
        'ffmpeg',
        '-i', concatenated_video,
        '-i', audio_file,
        '-vf', f"subtitles={final_subtitle_file}",
        '-c:v', 'libx264',
        '-c:a', 'aac',
        '-strict', 'experimental',
        '-shortest',
        output_video_file
    ]
    subprocess.run(command)

    # # Clean up temporary files
    # for segment in video_segments:
    #     os.remove(segment)
    # os.remove(concatenated_video)

    print(f"Final video with images and audio created: {output_video_file}")

# Example usage
base_directory = "sources/"
base_name = "eric1"
create_video_with_images_and_audio(base_directory, base_name)
