import requests
import os
import shutil
from urllib.parse import urlparse # For parsing the URL to get a potential filename

def download_file(url, save_directory, overwrite=False, custom_filename=None):
    """
    Downloads a file from a given URL and saves it to a specified directory.

    Args:
        url (str): The URL of the file to download.
        save_directory (str): The directory where the file should be saved.
        custom_filename (str, optional): A custom name for the saved file.
                                         If None, tries to infer from URL or Content-Disposition.
    """
    print(f"Attempting to download from: {url}")
    print(f"Saving to directory: {save_directory}")

    # 1. Ensure the save directory exists
    try:
        os.makedirs(save_directory, exist_ok=True)
        print(f"Directory '{save_directory}' ensured.")
    except OSError as e:
        print(f"Error creating directory {save_directory}: {e}")
        return False

    # 2. Get the filename
    if custom_filename:
        filename = custom_filename
    else:
        try:
            # Try to get filename from Content-Disposition header first
            with requests.get(url, stream=True, timeout=10) as r_head: # Short timeout for headers
                r_head.raise_for_status() # Raise an exception for bad status codes
                content_disposition = r_head.headers.get('content-disposition')
                if content_disposition:
                    # Example: "attachment; filename="actual_filename.jpg""
                    # A more robust parser might be needed for complex cases
                    parts = content_disposition.split('filename=')
                    if len(parts) > 1:
                        filename = parts[1].strip('"\' ') # Remove quotes and spaces
                    else: # Fallback if 'filename=' not found but header exists
                        filename = os.path.basename(urlparse(url).path)
                else:
                    # Fallback to URL parsing if no Content-Disposition
                    filename = os.path.basename(urlparse(url).path)

            if not filename: # If URL ends with / or path is empty
                filename = "downloaded_file"
                print(f"Could not determine filename, using default: '{filename}'")

        except requests.exceptions.RequestException as e:
            print(f"Error fetching headers or initial connection: {e}")
            return False
        except Exception as e:
            print(f"An unexpected error occurred while trying to determine filename: {e}")
            return False

    save_path = os.path.join(save_directory, filename)
    print(f"Resolved save path: {save_path}")
    
    
      # Check if file already exists
    if not overwrite and os.path.exists(save_path):
        print(f"File '{save_path}' already exists and overwrite is set to False. Skipping download.")
        return save_path


    # 3. Download the file
    try:
        with requests.get(url, stream=True, timeout=30) as r: # Longer timeout for content
            r.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
            total_size = int(r.headers.get('content-length', 0))
            
            print(f"Downloading '{filename}' ({total_size / (1024*1024):.2f} MB)...")
            
            with open(save_path, 'wb') as f:
                downloaded_size = 0
                for chunk in r.iter_content(chunk_size=8192): # 8KB chunks
                    if chunk: # filter out keep-alive new chunks
                        f.write(chunk)
                        downloaded_size += len(chunk)
                        # Basic progress (can be made prettier with tqdm)
                        progress = int(50 * downloaded_size / total_size) if total_size else 0
                        print(f"\r[{'#' * progress}{'.' * (50 - progress)}] {downloaded_size/1024:.2f}KB / {total_size/1024:.2f}KB", end="")
            print("\nDownload complete!")
            print(f"File saved as: {save_path}")
            return save_path
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error occurred: {e.response.status_code} - {e.response.reason}")
    except requests.exceptions.ConnectionError as e:
        print(f"Connection Error: Could not connect to {url}. Details: {e}")
    except requests.exceptions.Timeout:
        print(f"Timeout Error: The request to {url} timed out.")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during download: {e}")
    except IOError as e:
        print(f"File I/O error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    # Clean up partially downloaded file if an error occurred
    if os.path.exists(save_path) and downloaded_size < total_size :
        try:
            os.remove(save_path)
            print(f"Partially downloaded file '{save_path}' removed.")
        except OSError as e_rem:
            print(f"Error removing partially downloaded file '{save_path}': {e_rem}")
            
    return False

if __name__ == "__main__":
    # --- Configuration ---
    # Example URL (publicly accessible image)
    file_url = "https://www.python.org/static/community_logos/python-logo-master-v3-TM.png"
    # file_url = "https://speed.hetzner.de/100MB.bin" # For testing larger files
    # file_url = "https://invalid.url.that.does.not.exist/file.zip" # For testing errors

    custom_dir = "downloads"  # Relative to where the script is run
    # Or an absolute path:
    # custom_dir = "/path/to/your/desired/downloads_folder"

    # Optional: specify a custom filename. If None, it will try to infer.
    new_filename = None
    # new_filename = "python_official_logo.png"

    # --- Execution ---
    print("--- File Downloader ---")
    if download_file(file_url, custom_dir, new_filename):
        print("--- Process finished successfully. ---")
    else:
        print("--- Process failed. ---")

    # Example with custom filename
    # print("\n--- Downloading with custom filename ---")
    # another_url = "https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png"
    # download_file(another_url, custom_dir, "google_logo_custom.png")
