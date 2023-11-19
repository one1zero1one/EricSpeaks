import logging
from openai import OpenAI
import sys
import os
import glob

# Base directory and input base name
base_directory = sys.argv[1]
base_name = os.path.basename(base_directory)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = OpenAI()

system_prompt = "You are a helpful assistant for my family. Your task is to correct any spelling discrepancies in the transcribed text, in Romanian language. The text is from a recording of a 3-year-old speaking."

def generate_corrected_transcript(temperature, system_prompt, text_file):
    with open(text_file, "r") as file:
        user_input = file.read()

    response = client.chat.completions.create(
        model="gpt-4",
        temperature=temperature,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
    )

    # Assuming 'text' is the correct key for transcript text
    return response.choices[0].message['content']

def process_files(base_name, base_directory):
    # Find all text files for the given base name
    text_files_pattern = os.path.join(base_directory, f"{base_name}_*.txt")
    for text_file in glob.glob(text_files_pattern):
        logger.info(f"Processing file: {text_file}")
        corrected_text = generate_corrected_transcript(0, system_prompt, text_file)

        # Save the corrected text to a new file
        output_file_path = os.path.splitext(text_file)[0] + "_corrected.txt"
        with open(output_file_path, "w") as corrected_file:
            corrected_file.write(corrected_text)
        logger.info(f"Corrected text written to {output_file_path}")

# Process files
process_files(base_name, base_directory)
