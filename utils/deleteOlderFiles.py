
import glob
import os


def delete_older_files(pattern, keep=1):
    """
    Deletes all but the 'keep' most recent files matching the given pattern.

    Args:
        pattern (str): The glob pattern to match files.
        keep (int): Number of most recent files to keep. Default is 1.
    """
    files = glob.glob(pattern)
    if len(files) <= keep:
        return

    # Sort files by modification time (newest first)
    sorted_files = sorted(files, key=os.path.getmtime, reverse=True)

    # Files to delete
    files_to_delete = sorted_files[keep:]
    for file_path in files_to_delete:
        try:
            os.remove(file_path)
        except Exception:
            pass