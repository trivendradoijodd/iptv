Pseudocode

"C:\Program Files\Mozilla Firefox\firefox.exe" "file:///C:\Users\rainbow\Desktop\scripts\iptv\ui.vision.html?direct=1&macro=iptv/freeiptv2023&savelog=C:\Users\rainbow\Desktop\scripts\iptv\iptv2023-logs/logs.txt&closeBrowser=1"

1. Run the runAutomation.bat file.
2. It will have saved a log file in Downloads, with the name iptvLogs.txt or something like that.
3. Run the `parsingFromLogs` file with `python parsingFromLogs.py`
4. The script above will yield the value of m3u link, and will delete the previous files.
5. Download the file with the link if you wanna.
6. Get the file. 
7. Extract the username & password, for good measure.
8. Parse the playlist with `python declutterPlaylist.py`
9. Serve it with `python serve.py`