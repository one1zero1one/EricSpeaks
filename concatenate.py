import glob
import os

# Directory containing the files
source_directory = "sources/"

# Pattern to match all files with the format 'NAME_number.txt'
file_pattern = os.path.join(source_directory, "*_[0-9]*.txt")

# Find all files that match the pattern
matching_files = glob.glob(file_pattern)

# Extract unique names from the files (assuming the name is before the first underscore)
unique_names = set(os.path.basename(f).split('_')[0] for f in matching_files)

# Concatenate files for each unique name
for name in unique_names:
    # Pattern for current name
    current_pattern = os.path.join(source_directory, f"{name}_*.txt")

    # Output file for the current name
    output_file_path = os.path.join(source_directory, f"{name}.txt")

    with open(output_file_path, 'w') as outfile:
        for file_path in sorted(glob.glob(current_pattern)):
            with open(file_path, 'r') as infile:
                outfile.write(infile.read())
                outfile.write("\n")  # Newline for separation

    print(f"All files for '{name}' concatenated into {output_file_path}")
