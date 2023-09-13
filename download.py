import os
import subprocess

# Directory to save the downloaded files
download_dir = "./ts_files"

# Define the Python script you want to execute
script_to_execute = "merge.py"

# Define the directory containing the .ts files (relative path)
ts_directory_relative = download_dir

# Convert the relative path to an absolute path
ts_directory_absolute = os.path.abspath(ts_directory_relative)

# How many streams we should have in total
num_streams = 2902

# Check if the ts_files directory exists
if os.path.exists(download_dir) and os.path.isdir(download_dir):
    # .ts files are already downloaded
    ts_files = [file for file in os.listdir(
        download_dir) if file.endswith(".ts")]
    if len(ts_files) == num_streams:
        print(".ts files found. Proceeding to call the second script.")
else:
    # .ts files are not downloaded, download them
    import requests

    # URL of the .ts files
    base_url = "https://astream-9-1.voxzer.org/stream/5ef5c9a6dfe45b2548cac0bf/1080/index"

    # Create the download directory if it doesn't exist
    os.makedirs(download_dir, exist_ok=True)

    # Number of .ts files to download
    num_files = num_streams

    # Download the .ts files
    for i in range(1, num_files + 1):
        ts_url = f"{base_url}{i}.ts"
        file_name = os.path.join(download_dir, f"{i}.ts")
        try:
            response = requests.get(ts_url, stream=True)
            response.raise_for_status()
            with open(file_name, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
            print(f"Downloaded {i}/{num_files} files")
        except requests.exceptions.RequestException as e:
            print(f"Error downloading {ts_url}: {e}")

    print("Download completed.")

# Call the second script

# Get the current working directory
current_directory = os.getcwd()

# Define the current directory
output_dir = "./"

directory_absolute = os.path.abspath(output_dir)

# Get the directory where the calling script is located
calling_script_directory = os.path.dirname(os.path.abspath(__file__))

# Change the current working directory to the calling script's directory
os.chdir(calling_script_directory)

# Run the other Python script with the directory argument
try:
    subprocess.run(["python", script_to_execute,
                   directory_absolute, ts_directory_absolute, download_dir], check=True)
    print("Other script executed successfully.")
except subprocess.CalledProcessError as e:
    print(f"Error executing the script: {e}")
