# Download Deliver'd

This small project is designed for learning about blobs (large binary objects) in web development and practicing reverse-engineering skills by dissecting a website and using the debugger offered by Chrome.

![deliver'd](/docs/screenshot.jpg)
## Objectives:

- Blob Understanding: Gain practical knowledge of blobs and their role in web applications, why they are used.

- Reverse-Engineering Practice: Learn how to dissect and analyze websites to understand their structure and data handling.

- Hands-On Learning: Engage in practical exercises and code analysis.

- Data Security Awareness: Understand better data security principles in web applications, specifically when storing video files.

## In detail

### Preparation:

- blob URI, [link](https://www.youtube.com/watch?v=UgCCR-ZBP8w)
- deactivate breakpoints, [link](https://www.youtube.com/watch?v=_wGJpMfyfv4)
- inspect an element, [link](https://www.youtube.com/watch?v=oRKlKhFt2Rg)
- debug JavaScript events, [link](https://www.youtube.com/watch?v=AgIoWJcxsMQ)
- inspect network traffic, [link](https://www.youtube.com/watch?v=bQyXQDQFPag)
- how to download .m3u8 and .ts files, [link](https://www.youtube.com/watch?v=B8pW5cr2tIg)

### Run the script:
```bash
python3 download.py
```
### Code:

<details>
<summary>download.py</summary>

```Python
import os
import subprocess
```
These are standard Python libraries for working with the operating system and running subprocesses.
```Python
# Directory to save the downloaded files
download_dir = "./ts_files"
```
This sets the directory where downloaded .ts files will be stored.
```Python
# Define the Python script you want to execute
script_to_execute = "merge.py"
```
This specifies the name of the Python script you want to execute later.
```Python
# Define the directory containing the .ts files (relative path)
ts_directory_relative = download_dir
```
This sets the relative path for the directory containing the .ts files.

```Python
# Convert the relative path to an absolute path
ts_directory_absolute = os.path.abspath(ts_directory_relative)
```
This converts the relative path to an absolute path for later use.

```Python
# How many streams we should have in total
num_streams = 2902
```
This sets the number of expected streams.

```Python
# Check if the ts_files directory exists
if os.path.exists(download_dir) and os.path.isdir(download_dir):
    # .ts files are already downloaded
    ts_files = [file for file in os.listdir(
        download_dir) if file.endswith(".ts")]
    if len(ts_files) == num_streams:
        print(".ts files found. Proceeding to call the second script.")
```
This section checks if the download directory exists and if it contains the expected number of .ts files. If both conditions are met, it proceeds to call the second script.

```Python
else:
    # .ts files are not downloaded, download them
    import requests
    ...
```
If the download directory doesn't exist or doesn't contain the required number of .ts files, it enters the else block and proceeds to download the .ts files.

```Python
# Call the second script
...
```
This section calls the second script (merge.py) with the necessary arguments.

```Python
# Get the current working directory
current_directory = os.getcwd()
```
This gets the current working directory, which is the directory where this script is located.

```Python
# Define the current directory
output_dir = "./"
```
This sets the output directory for the second script (the current directory).

```Python

directory_absolute = os.path.abspath(output_dir)
```
This converts the relative output directory path to an absolute path.

```Python
# Get the directory where the calling script is located
calling_script_directory = os.path.dirname(os.path.abspath(__file__))
```
This gets the directory where the calling script (the script you provided) is located.

```Python
# Change the current working directory to the calling script's directory
os.chdir(calling_script_directory)
```
This changes the current working directory to the directory where the calling script is located.

```Python
# Run the other Python script with the directory argument
try:
    subprocess.run(["python", script_to_execute,
                   directory_absolute, ts_directory_absolute, download_dir], check=True)
    print("Other script executed successfully.")
except subprocess.CalledProcessError as e:
    print(f"Error executing the script: {e}")
```
This section runs the second script with the provided arguments, and it handles any potential errors that may occur during execution.

Overall, this script is designed to check if the required .ts files are already downloaded and then call another Python script (**merge.py**) with specific arguments. If the .ts files are not downloaded, it also handles the download process.
</details>

---
<details>
<summary>merge.py</summary>

```Python
import os
import sys
import datetime
import shutil
```
These are standard Python libraries for working with the operating system, handling command-line arguments, date and time operations, and file manipulation.

```Python
# Output directory for intermediate files
output_dir = sys.argv[1]
```
This line takes the first command-line argument as the output directory for intermediate files.

```Python
# Directory where the .ts files are located
ts_dir = sys.argv[2]
```
This takes the second command-line argument as the directory where the .ts files are located.

```Python
# Output file name
final_output_file = "final_output.mp4"
```
This sets the name of the final output file.

```Python
# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)
```
This creates the output directory if it doesn't already exist.

```Python
# Function to extract the numeric part from a filename
def extract_number(filename):
    return int("".join(filter(str.isdigit, filename)))
```
This is a function to extract numeric parts from filenames, which will be used to sort the .ts files.

```Python
# Get a list of all .ts files in the directory
ts_files = [file for file in os.listdir(ts_dir) if file.endswith(".ts")]
```
This retrieves a list of all .ts files in the specified directory.

```Python
# Sort the .ts files based on their numeric portions
sorted_ts_files = sorted(ts_files, key=extract_number)
```
This sorts the .ts files based on their numeric portions using the `extract_number` function.
```Python
# Create a temporary batch file
batch_file = os.path.join(output_dir, "batch_all.txt")
```
This sets the path for a temporary batch file.
```Python
# Write the file paths of all .ts files to the temporary batch file
with open(batch_file, "w") as f:
    for file in sorted_ts_files:
        file_path = os.path.join(ts_dir, file)
        f.write(f"file '{file_path}'\n")
```
This writes the file paths of all .ts files to the temporary batch file in a format suitable for FFmpeg concatenation.

```Python
# Concatenate all .ts files into a temporary output file using FFmpeg
temp_output_file = os.path.join(output_dir, "temp_output.mp4")
ffmpeg_concat_command = f"ffmpeg -f concat -safe 0 -i {batch_file} -c copy '{temp_output_file}'"
```
This constructs a command to use FFmpeg to concatenate all .ts files into a temporary output file.
```Python
# Check if the final output file already exists
if os.path.exists(os.path.join(output_dir, final_output_file)):
    # Generate a new filename with a unique timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    final_output_file = f"final_output_{timestamp}.mp4"
```
This section checks if the final output file already exists. If it does, a new filename with a unique timestamp is generated to avoid overwriting the existing file.
```Python
# Convert the temporary output file to .mp4 format
ffmpeg_convert_command = f"ffmpeg -i '{temp_output_file}' -c:v libx264 -crf 23 -c:a aac -strict experimental -b:a 192k '{os.path.join(output_dir, final_output_file)}'"
```
This constructs a command to use FFmpeg to convert the temporary output file into an .mp4 format file with specific encoding settings.
```Python
# Execute the FFmpeg concatenation command
os.system(ffmpeg_concat_command)
```
This runs the FFmpeg concatenation command to merge the .ts files into a temporary output file.
```Python
# Rename the temporary output file to the final output file
os.rename(temp_output_file, os.path.join(output_dir, final_output_file))
```
This renames the temporary output file to the final output file.
```Python
# Remove the temporary batch file
os.remove(batch_file)
```
This deletes the temporary batch file that was used for FFmpeg concatenation.
```Python
# Delete the ts_files folder
tmp = os.listdir(ts_dir)
if os.path.exists(ts_dir) and os.path.isdir(ts_dir):
    shutil.rmtree(ts_dir)
    print(f"Deleted {ts_dir}")
```
This deletes the ts_dir folder and its contents if it exists and is a directory.
```Python
print(f"Conversion and concatenation complete. Final output: {os.path.join(output_dir, final_output_file)}")
```
Finally, this prints a message indicating the completion of the conversion and concatenation process, along with the path to the final output file.
</details>

---

Source: [Binary large object](https://en.wikipedia.org/wiki/Binary_large_object)
