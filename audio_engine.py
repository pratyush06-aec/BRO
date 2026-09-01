import os
import asyncio
import edge_tts
import pygame
import speech_recognition as sr
from groq import Groq
from dotenv import load_dotenv
import time

load_dotenv()

# Initialize pygame mixer for audio playback
pygame.mixer.init()

async def async_speak(text, voice="en-US-ChristopherNeural"):
    """
    Asynchronously converts text to speech using edge-tts and plays it.
    """
    if not text or not str(text).strip():
        return
        
    output_file = "temp_response.mp3"
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)
    
    # Play the audio using pygame
    pygame.mixer.music.load(output_file)
    pygame.mixer.music.play()
    
    # Wait for the audio to finish playing
    while pygame.mixer.music.get_busy():
        await asyncio.sleep(0.1)
        
    # Unload and clean up
    pygame.mixer.music.unload()
    try:
        os.remove(output_file)
    except Exception:
        pass

def speak(text):
    """
    Synchronous wrapper for async_speak.
    """
    asyncio.run(async_speak(text))

def listen_and_transcribe():
    """
    Listens to the user's command using the microphone, records it to a temp wav file,
    and uses Groq's Whisper API to transcribe it.
    """
    groq_api_key = os.environ.get("GROQ_API_KEY")
    if not groq_api_key or groq_api_key == "your_groq_api_key_here":
        print("Please set your GROQ_API_KEY in the .env file.")
        return None

    client = Groq(api_key=groq_api_key)
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Bro is listening for your command...")
        # Adjust for ambient noise
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            # Listen to the command
            audio_data = recognizer.listen(source, timeout=5, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            print("Listening timed out.")
            return None
            
    # Save to a temporary wav file
    filename = "temp_command.wav"
    with open(filename, "wb") as f:
        f.write(audio_data.get_wav_data())
        
    print("Transcribing with Groq Whisper...")
    try:
        with open(filename, "rb") as file:
            transcription = client.audio.transcriptions.create(
              file=(filename, file.read()),
              model="whisper-large-v3",
              prompt="Specify context or spelling",
              response_format="json",
              language="en",
              temperature=0.0
            )
        # Clean up
        os.remove(filename)
        print(f"User said: {transcription.text}")
        return transcription.text
    except Exception as e:
        print(f"Error during transcription: {e}")
        try:
            os.remove(filename)
        except:
            pass
        return None
