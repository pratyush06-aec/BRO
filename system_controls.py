import webbrowser
import os
import subprocess
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import urllib.request
import urllib.parse
import re

def search_web(query):
    """Searches the web in a new browser tab."""
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open_new_tab(url)
    return f"Searching the web for: {query}"

def open_website(url):
    """Opens a specific website."""
    if not url.startswith("http"):
        url = "https://" + url
    webbrowser.open(url)
    return f"Opening website: {url}"

def play_on_youtube(query):
    """Searches YouTube and plays the first video result."""
    try:
        query_string = urllib.parse.urlencode({"search_query": query})
        html_content = urllib.request.urlopen("https://www.youtube.com/results?" + query_string)
        search_results = re.findall(r"watch\?v=(\S{11})", html_content.read().decode())
        
        if search_results:
            video_url = "https://www.youtube.com/watch?v=" + search_results[0]
            webbrowser.open(video_url)
            return f"Playing {query} on YouTube."
        else:
            return f"No YouTube results found for {query}."
    except Exception as e:
        return f"Failed to play on YouTube. Error: {e}"

def open_app(app_name):
    """Tries to open a local application."""
    app_name_lower = app_name.lower()
    try:
        # Common windows apps
        if 'notepad' in app_name_lower:
            subprocess.Popen('notepad.exe')
        elif 'calculator' in app_name_lower or 'calc' in app_name_lower:
            subprocess.Popen('calc.exe')
        elif 'code' in app_name_lower or 'vs code' in app_name_lower:
            subprocess.Popen('code', shell=True)
        elif 'explorer' in app_name_lower or 'files' in app_name_lower:
            subprocess.Popen('explorer.exe')
        else:
            return f"I don't know how to open {app_name} yet."
        return f"Opening {app_name}"
    except Exception as e:
        return f"Failed to open {app_name}. Error: {e}"

def system_volume(level):
    """Controls the system volume. Level should be between 0 and 100."""
    try:
        level = max(0, min(100, int(level))) # Clamp between 0 and 100
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        
        # Volume range is usually -65.25 to 0.0, we map 0-100 to this roughly or use SetMasterVolumeLevelScalar
        volume.SetMasterVolumeLevelScalar(level / 100.0, None)
        return f"Set system volume to {level} percent."
    except Exception as e:
        return f"Failed to set volume. Make sure pycaw is installed. Error: {e}"
