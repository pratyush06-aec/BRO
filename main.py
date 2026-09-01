import os
import json
from dotenv import load_dotenv
from groq import Groq

# Import our new modules
from wake_word import listen_for_wake_word
from audio_engine import speak, listen_and_transcribe
from tools import AVAILABLE_TOOLS, GROQ_TOOLS_SCHEMA

# Initialize environment and client
load_dotenv()
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# Create Groq client
if GROQ_API_KEY and GROQ_API_KEY != "your_groq_api_key_here":
    client = Groq(api_key=GROQ_API_KEY)
else:
    client = None

# Conversation Memory
messages = [
    {"role": "system", "content": "You are a highly capable AI assistant named Bro. You control the user's PC, can search the web, play music, open apps, and get news. Keep your spoken responses concise and natural. NEVER hallucinate or make up website URLs. If the user asks to play a song or video on YouTube, ALWAYS use the `play_on_youtube` tool, do NOT use `open_website`."}
]

def process_command_with_llm(user_input):
    """
    Sends the user input to Groq, checks if a tool should be called,
    executes the tool if necessary, and returns the final AI response.
    """
    if not client:
        return "Groq API key is not configured. Please set it in the dot env file."
        
    messages.append({"role": "user", "content": user_input})

    try:
        # Step 1: Send the conversation and available functions to the model
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=messages,
            tools=GROQ_TOOLS_SCHEMA,
            tool_choice="auto",
            max_tokens=4096
        )

        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        # Step 2: Check if the model wanted to call a function
        if tool_calls:
            messages.append(response_message)  # extend conversation with assistant's reply
            
            # Step 3: Call the functions
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = AVAILABLE_TOOLS.get(function_name)
                
                if function_to_call:
                    function_args = json.loads(tool_call.function.arguments)
                    print(f"Executing tool: {function_name} with args: {function_args}")
                    function_response = function_to_call(**function_args)
                    
                    # Append the function response to the conversation
                    messages.append(
                        {
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": function_name,
                            "content": str(function_response),
                        }
                    )
                else:
                    print(f"Tool {function_name} not found.")

            # Step 4: Send the info back to the model for a final response
            second_response = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=messages
            )
            final_text = second_response.choices[0].message.content
            messages.append({"role": "assistant", "content": final_text})
            return final_text
            
        else:
            # No tool called, just a normal response
            final_text = response_message.content
            messages.append({"role": "assistant", "content": final_text})
            return final_text

    except Exception as e:
        print(f"Error communicating with LLM: {e}")
        return "Sorry Bro, I ran into an error processing that."

def on_wake_word_detected(captured_command=""):
    """Callback function triggered when the wake word is heard."""
    if captured_command:
        print(f"Captured command from wake word: {captured_command}")
        command_text = captured_command
    else:
        speak("Yeah Bro?")
        command_text = listen_and_transcribe()
    
    if command_text:
        # Process the command
        ai_response = process_command_with_llm(command_text)
        print(f"Bro: {ai_response}")
        speak(ai_response)
    else:
        # If nothing was transcribed or timed out
        pass

import threading
import sys

if __name__ == "__main__":
    if not client:
        print("WARNING: Groq API Key is missing. The assistant will not function properly.")
    
    speak("Initializing Bro. System online and ready.")
    
    def keyboard_input_loop():
        print("\n--- TEXT MODE ENABLED ---")
        print("You can now type commands directly here, or speak 'hey bro' out loud.\n")
        while True:
            try:
                # We use a simple input prompt
                user_text = input()
                if user_text.strip():
                    print(f"\n[Typed Command]: {user_text}")
                    # Process it just like a voice command
                    ai_response = process_command_with_llm(user_text)
                    print(f"Bro: {ai_response}\n")
                    speak(ai_response)
            except (KeyboardInterrupt, EOFError):
                os._exit(0)
                
    # Run the keyboard listener in a background thread
    keyboard_thread = threading.Thread(target=keyboard_input_loop, daemon=True)
    keyboard_thread.start()
    
    # Start the wake word listener in the main thread. This is a blocking loop.
    listen_for_wake_word(on_wake_word_detected)