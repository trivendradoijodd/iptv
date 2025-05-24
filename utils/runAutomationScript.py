import subprocess
import sys
import os

def run_automation_script():
    # Define the path to Firefox executable and the URL as separate strings
    firefox_exe_path = r"C:\Program Files\Mozilla Firefox\firefox.exe"
    # Using a raw string (r"...") is good practice for Windows paths to avoid issues with backslashes
    # The URL is treated as a single argument
    target_url = r"file:///C:\Users\rainbow\Desktop\scripts\iptv\ui.vision.html?direct=1&macro=iptv/freeiptv2023&savelog=iptvlogs.txt&closeBrowser=0"

    try:
        # Construct the command as a list of strings
        # The first element is the executable, subsequent elements are arguments
        command_list = [firefox_exe_path, target_url]

        print(f"Attempting to execute: {command_list}")

        # Run the command and wait for it to complete.
        # check=True will raise a CalledProcessError if the command returns a non-zero exit code.
        # capture_output=True and text=True are good for debugging but might not be necessary
        # for launching a browser where output is usually not captured by the script.
        # If Firefox launches and stays open, the Python script will wait until Firefox is closed
        # (or until the specific tab opened by the command is closed, depending on Firefox's behavior).
        # If closeBrowser=0 in your URL means Firefox should stay open, then your Python script
        # will wait indefinitely until that Firefox process closes.
        result = subprocess.run(
            command_list,
            check=True,
            capture_output=True, # Captures stdout and stderr
            text=True            # Decodes output as text (UTF-8 by default)
        )

        print(f"Command executed successfully. Return code: {result.returncode}")
        if result.stdout:
            print("STDOUT:\n", result.stdout)
        if result.stderr:
            print("STDERR:\n", result.stderr)

    except FileNotFoundError:
        print(f"Error: The executable '{firefox_exe_path}' was not found.")
        print("Please ensure Firefox is installed at the specified path.")
    except subprocess.CalledProcessError as e:
        print(f"Error: Command failed with exit code {e.returncode}")
        print(f"STDOUT:\n{e.stdout}")
        print(f"STDERR:\n{e.stderr}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    print("Python script finished execution after command.")

# This allows the file to be run directly for testing
if __name__ == "__main__":
    automation_result = run_automation_script()
    if automation_result:
        print(f"Automation result: {automation_result}")
    else:
        print("No automation result output")
