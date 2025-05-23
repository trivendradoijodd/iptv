import re
import os
import glob

from utils.deleteOlderFiles import delete_older_files

def extract_m3u_link_from_latest_logs(delete_older=True):
    """
    Gets the latest logs*.txt file from Downloads folder,
    extracts the m3u link, and optionally deletes older files.
    
    Args:
        delete_older (bool): Whether to delete older logs files
        
    Returns:
        str or None: The extracted m3u link or None if not found
    """
    downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
    pattern = os.path.join(downloads_folder, "iptvlogs*.txt")

    files = glob.glob(pattern)
    if not files:
        return None

    # Sort files by modification time (newest first)
    sorted_files = sorted(files, key=os.path.getmtime, reverse=True)
    latest_file = sorted_files[0]

    if delete_older:
        delete_older_files(pattern, keep=1)

    try:
        with open(latest_file, 'r') as file:
            content = file.read()

        match = re.search(r'\[echo\] m3uLink = (http[^\s]+)', content)
        if match:
            return match.group(1)
    except Exception:
        pass

    return None

# This allows the file to be run directly for testing
if __name__ == "__main__":
    m3u_link = extract_m3u_link_from_latest_logs()
    if m3u_link:
        print(f"Extracted m3u link: {m3u_link}")
    else:
        print("No m3u link found")
