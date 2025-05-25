import os
from utils.deleteOlderFiles import delete_older_files
from utils.parsingFromLogs import extract_m3u_link_from_latest_logs
from utils.urlDownloader import download_file
from utils.declutterPlaylist import declutter_playlist
from utils.runUIAutomationScript import run_ui_automation_script


def driver(forceRefresh = False):
    run_ui_automation_script(forceRefresh);

    # Get the m3u link
    m3u_link = extract_m3u_link_from_latest_logs(delete_older=True)

    if m3u_link:
        print(f"Got the m3u link: {m3u_link}")
        # With the m3u Link, download the file
        downloaded_playlist_path = download_file(m3u_link, "my_downloads")
        
        pattern = os.path.join("my_downloads", "tv_channels_*.m3u")
        delete_older_files(pattern)
        
        # With the file downloaded, declutter the playlist
        declutter_playlist(downloaded_playlist_path, 'outputs/output.m3u')
        return m3u_link
    else:
        print("Could not find an m3u link")
