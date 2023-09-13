import os
import sys
import datetime
import shutil

# Output directory for intermediate files
output_dir = sys.argv[1]

# Directory where the .ts files are located
ts_dir = sys.argv[2]


# Output file name
final_output_file = "final_output.mp4"

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Function to extract the numeric part from a filename


def extract_number(filename):
    return int("".join(filter(str.isdigit, filename)))


# Get a list of all .ts files in the directory
ts_files = [file for file in os.listdir(ts_dir) if file.endswith(".ts")]

# Sort the .ts files based on their numeric portions
sorted_ts_files = sorted(ts_files, key=extract_number)

# Create a temporary batch file
batch_file = os.path.join(output_dir, "batch_all.txt")

# Write the file paths of all .ts files to the temporary batch file
with open(batch_file, "w") as f:
    for file in sorted_ts_files:
        file_path = os.path.join(ts_dir, file)
        f.write(f"file '{file_path}'\n")

# Concatenate all .ts files into a temporary output file using FFmpeg
temp_output_file = os.path.join(output_dir, "temp_output.mp4")
ffmpeg_concat_command = f"ffmpeg -f concat -safe 0 -i {batch_file} -c copy '{temp_output_file}'"

# Check if the final output file already exists
if os.path.exists(os.path.join(output_dir, final_output_file)):
    # Generate a new filename with a unique timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    final_output_file = f"final_output_{timestamp}.mp4"

# Convert the temporary output file to .mp4 format
ffmpeg_convert_command = f"ffmpeg -i '{temp_output_file}' -c:v libx264 -crf 23 -c:a aac -strict experimental -b:a 192k '{os.path.join(output_dir, final_output_file)}'"

# Execute the FFmpeg concatenation command
os.system(ffmpeg_concat_command)

# Rename the temporary output file to the final output file
os.rename(temp_output_file, os.path.join(output_dir, final_output_file))

# Remove the temporary batch file
os.remove(batch_file)
# Delete the ts_files folder
tmp = os.listdir(ts_dir)
if os.path.exists(ts_dir) and os.path.isdir(ts_dir):
    shutil.rmtree(ts_dir)
    print(f"Deleted {ts_dir}")

print(
    f"Conversion and concatenation complete. Final output: {os.path.join(output_dir, final_output_file)}")
