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
        wake_word_detected = False
        captured_command = ""
        
        with sr.Microphone() as source:
            # Stay inside this context manager so the mic doesn't constantly open and close
            while not wake_word_detected:
                try:
                    # Listen for a short phrase
                    audio = r.listen(source, timeout=5, phrase_time_limit=5)
                    
                    # Using Google's free speech recognition (no API key required)
                    # It is highly accurate, though requires an internet connection.
                    text = r.recognize_google(audio).lower()
                    print(f"[Debug] I heard: '{text}'")
                    
                    # Check for "bro" instead of "hey bro" just to be more forgiving during testing
                    if "bro" in text or "hey" in text:
                        wake_word_detected = True
                        # Extract any commands spoken after the wake word
                        # e.g., "hey bro open youtube" -> "open youtube"
                        captured_command = text.replace("hey bro", "").replace("hey", "").replace("bro", "").strip()
                        break # Break the inner loop to drop the microphone handle
                        
                except sr.WaitTimeoutError:
                    # No speech detected within the timeout, just loop again without closing the mic
                    pass
                except sr.UnknownValueError:
                    # Speech was detected but not understood
                    print("[Debug] I heard some audio, but couldn't understand the words.")
                    pass
                except sr.RequestError as e:
                    print(f"Could not request results; {e}")
                except Exception as e:
                    print(f"Error in wake word detection: {e}")
                
        # Now outside the with block, the microphone handle is released for the main engine!
        if wake_word_detected:
            print("Wake word detected!")
            callback(captured_command)
            print("Listening for wake word again...")
