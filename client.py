from openai import OpenAI
# The OpenAI library is imported to allow interaction with the GPT models.

# client = OpenAI()
# This line is commented out. It's the standard way to initialize if the API key
# were set as an environment variable (best practice).

client= OpenAI(
    # Initialize the OpenAI client object.
    api_key="<YOUR_OPENAI_API_KEY>"
    # The API key is passed directly to the client for authentication.
)

completion= client.chat.completions.create(
    # Call the chat completions endpoint to generate a response.
    model= "gpt-3.5-turbo",
    # Specify the language model to use (GPT-3.5 Turbo).
    messages= [
        # Define the conversation history (a list of message objects).
    {"role" : "system" , "content" : "You are a virtual assistant named bro, killed in explaining general tasks"},
        # The 'system' message sets the AI's persona, guiding its responses.
    {"role" : "user" , "content" : "What is Coding?"}
        # The 'user' message is the actual question or prompt being sent to the AI.
    ]
)
print(completion.choices[0].message.content)
# Access the generated text:
# 1. `completion`: The entire response object.
# 2. `.choices`: A list of potential responses (we take the first one: [0]).
# 3. `.message`: The message object containing the AI's reply.
# 4. `.content`: The actual text string of the AI's response.