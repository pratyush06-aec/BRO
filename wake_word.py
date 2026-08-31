import speech_recognition as sr

def listen_for_wake_word(callback):
    """
    Listens for the wake word using the SpeechRecognition library.
    Calls the provided callback function when detected.
    This alternative requires no API keys.
    """
    r = sr.Recognizer()
    
    # Adjust for ambient noise once at the start
    with sr.Microphone() as source:
        print("Adjusting for ambient noise... Please wait.")
        r.adjust_for_ambient_noise(source, duration=2)
        
    print("Listening for wake word 'hey bro'...")
    
    while True:
        with sr.Microphone() as source:
            try:
                # Listen for a short phrase
                audio = r.listen(source, timeout=1, phrase_time_limit=3)
                
                # Using Google's free speech recognition (no API key required)
                # It is highly accurate, though requires an internet connection.
                text = r.recognize_google(audio).lower()
                
                if "hey bro" in text:
                    print("Wake word detected!")
                    callback()
                    print("Listening for wake word again...")
                    
            except sr.WaitTimeoutError:
                # No speech detected within the timeout, just loop again
                pass
            except sr.UnknownValueError:
                # Speech was detected but not understood
                pass
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
            except Exception as e:
                print(f"Error in wake word detection: {e}")
