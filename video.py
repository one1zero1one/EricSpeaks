from PIL import Image
import subprocess
import sys
import os

def create_blank_image(image_path, size=(1920, 1080), color=(255, 255, 255)):
    """Create a blank image with the specified size and color."""
    img = Image.new('RGB', size, color)
    img.save(image_path)

def create_video_with_subtitles(source_directory, base_name):
    audio_file = os.path.join(source_directory, f"{base_name}.mp3")
    subtitle_file = os.path.join(source_directory, f"{base_name}.srt")
    output_video_file = os.path.join(source_directory, f"{base_name}_with_subtitles.mp4")
    blank_image_path = os.path.join(source_directory, "blank_image.jpg")

    # Create a blank image
    create_blank_image(blank_image_path)

    # Command to create a video with subtitles
    command = [
        'ffmpeg',
        '-loop', '1',  # Loop over the blank image
        '-i', blank_image_path,  # Use the generated blank image
        '-i', audio_file,
        '-vf', f"subtitles={subtitle_file}",
        '-c:v', 'libx264',
        '-c:a', 'aac',
        '-strict', 'experimental',
        '-b:a', '192k',
        '-shortest',
        output_video_file
    ]

    # Execute the command
    subprocess.run(command)

    print(f"Video created: {output_video_file}")

# Example usage
base_directory = "sources/"
base_name = "eric1"
create_video_with_subtitles(base_directory, base_name)
