import requests
import os
from system_controls import search_web, open_website, open_app, system_volume, play_on_youtube
import musicLibrary
import webbrowser

def play_music(song_name):
    """Plays music based on the song name using the local dictionary."""
    song_name_lower = song_name.lower().replace(" ", "_")
    link = musicLibrary.music.get(song_name_lower)
    if link:
        webbrowser.open(link)
        return f"Playing {song_name} from your library."
    else:
        return f"Song '{song_name}' not found in your local library."

def fetch_news():
    """Fetches the top headlines from India."""
    newsapi = os.environ.get("NEWS_API_KEY")
    if not newsapi:
        return "News API key is not configured."
    
    r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
    if r.status_code == 200:
        data = r.json()
        articles = data.get('articles', [])
        # We only return the top 3 headlines to not overwhelm the TTS
        headlines = [article['title'] for article in articles[:3]]
        return "Here are the top 3 headlines: " + "; ".join(headlines)
    else:
        return "Sorry, I couldn't fetch the news right now."

# Define the tools mapping for Groq
AVAILABLE_TOOLS = {
    "play_music": play_music,
    "fetch_news": fetch_news,
    "search_web": search_web,
    "open_website": open_website,
    "open_app": open_app,
    "system_volume": system_volume,
    "play_on_youtube": play_on_youtube
}

# Define the JSON schemas for the tools to pass to Groq API
GROQ_TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "play_music",
            "description": "Plays a specific song from the user's local music library.",
            "parameters": {
                "type": "object",
                "properties": {
                    "song_name": {
                        "type": "string",
                        "description": "The name of the song to play (e.g., 'desi kalakar', 'glory')."
                    }
                },
                "required": ["song_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "play_on_youtube",
            "description": "Searches YouTube and plays the first video result. Use this when the user asks to play a song or video on YouTube.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query for the YouTube video."
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "fetch_news",
            "description": "Fetches the current top news headlines.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Searches the internet for a query in a new browser tab. Use this to find information online.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query."
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "open_website",
            "description": "Opens a specific website url.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The website URL (e.g., 'youtube.com', 'google.com')."
                    }
                },
                "required": ["url"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "open_app",
            "description": "Opens a local system application.",
            "parameters": {
                "type": "object",
                "properties": {
                    "app_name": {
                        "type": "string",
                        "description": "The name of the application to open (e.g., 'notepad', 'calculator', 'vs code')."
                    }
                },
                "required": ["app_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "system_volume",
            "description": "Sets the system volume to a specific level (0 to 100).",
            "parameters": {
                "type": "object",
                "properties": {
                    "level": {
                        "type": "integer",
                        "description": "The volume level from 0 to 100."
                    }
                },
                "required": ["level"]
            }
        }
    }
]
