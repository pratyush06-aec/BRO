import speech_recognition as sr # Imports the library for converting speech to text.
import webbrowser             # Imports the library for opening web pages in a browser.
import pyttsx3                # Imports the library for Text-to-Speech (TTS) conversion.
import musicLibrary           # Imports a custom module expected to contain music links.
import requests               # Imports the library for making HTTP requests (used for News API).
from openai import OpenAI     # Imports the library to interact with OpenAI models.

recognizer = sr.Recognizer()  # Initialize the Recognizer object from speech_recognition.
engine = pyttsx3.init()       # Initialize the TTS engine for speaking output.

newsapi = "3b187329f41e4a29b1b34ffd605d7e63" # Your personal NewsAPI key for fetching headlines.

# --- Helper Functions ---

def speak(text):
    # Function to convert the given text into speech and play it.
    engine.say(text)
    engine.runAndWait() # Blocks until all queued speech commands are complete.

def processed_by_ai(command):
    # Function to send a command to the OpenAI GPT model and get a response.
    client = OpenAI(api_key="<YOUR_OPENAI_API_KEY>")
    # Initialize OpenAI client (API key is hardcoded here).
    completion = client.chat.completions.create(
        # Call the chat completions API.
        model="gpt-3.5-turbo",
        # Use the specified model for conversational AI.
        messages=[
            # Define the AI's persona (system role) and the user's prompt.
            {"role": "system", "content": "You are a virtual assistant named bro"},
            {"role": "user", "content": command}
        ]
    )
    return completion.choices[0].message.content
    # Return the generated text content from the AI's response.

def process_command(c):
    # Function to analyze the recognized command and execute the appropriate action.
    if "open_google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open_facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    # ... (other web opening commands follow a similar pattern) ...
    elif "open_youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open_instagram" in c.lower():
        webbrowser.open("https://instagram.com")
    elif "open_twitter" in c.lower():
        webbrowser.open("https://twitter.com")
    elif "open_linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif "open_comet" in c.lower():
        webbrowser.open("https://comet.com")
    elif "open_spotify" in c.lower():
        # Note: The Spotify URL seems non-standard, likely for local testing/placeholder.
        webbrowser.open("https://spotify.com")
    elif c.lower().startswith("play"):
        # Handles commands that start with "play" for music.
        song = c.lower().split(" ")[1] # Extracts the song name (assuming it's the second word).
        link = musicLibrary.music.get(song) # Looks up the song in the imported musicLibrary dictionary.
        if link:
            webbrowser.open(link) # Opens the song link if found.
        else:
            speak("Song not found in your library.") # Informs the user if the song isn't mapped.
    elif "news" in c.lower():
        # Handles the "news" command to fetch and read headlines.
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        # Makes an API request for top Indian headlines.
        if r.status_code == 200:
            # Check if the API request was successful.
            data = r.json()
            articles = data.get('articles', [])
            # Extract the list of articles.
            for article in articles:
                speak(article['title']) # Speaks the title of each article.
        else:
            speak("Sorry, I couldn't fetch the news.") # Handles API errors.
    else:
        # If no specific command is matched, the command is sent to the AI.
        speak(processed_by_ai(c))

# --- Main Execution Block ---

if __name__ == "__main__":
    # Ensures the code only runs when the script is executed directly.
    speak("Initializing Bro!!!") # Announce initialization.
    while True:
        # Main loop that continuously listens for the wake word.
        r = sr.Recognizer() # Re-initialize the Recognizer in the loop for robustness.
        print("Recognizing.....")
        try:
            with sr.Microphone() as source:
                # Use the default system microphone as the audio source.
                print("Listening.....")
                audio = r.listen(source, timeout=5, phrase_time_limit=3)
                # Listen for a short phrase for the wake word, with limits to prevent long listening times.
            word = r.recognize_google(audio)
            # Convert the first audio segment to text using Google's service.
            if word.lower() == "bro":
                # Check for the wake word.
                speak("Yeahh, Bro!!!!") # Acknowledge the wake word.
                with sr.Microphone() as source:
                    # Start listening for the actual command after the wake word.
                    print("Yeah bro....")
                    audio = r.listen(source) # Listen for the command (no time limit here).
                    command = r.recognize_google(audio)
                    # Convert the command audio to text.
                    process_command(command) # Pass the command to the processing function.
        except Exception as e:
            # Catch exceptions, such as 'Unknown Value Error' (no speech recognized) or timeout.
            print("Error, {0}".format(e))