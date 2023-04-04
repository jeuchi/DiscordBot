import discord
import openai
from constants import OPEN_API_KEY

# Set up OpenAI API key
openai.api_key = OPEN_API_KEY

# Set up the conversation history
conversation_history = []

def generate_response(user_id, prompt):
    # Filter the conversation history to include only messages from the current user
    #user_history = [(x['role'], x['content']) for x in conversation_history if x['role'] == 'user' and x['content'] != '']

    # Combine the user's messages into a single string
    #conversation = "\n".join([x[1] for x in user_history])
    conversation_history.append({"role": "user", "content": prompt})

    try:
        # Create a new chat completion request to the GPT-3 model
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation_history,
            max_tokens=75,
            n=1,
            temperature=0.65,
            stop=None,
            frequency_penalty=0,
            presence_penalty=0,
        )

        # Extract the generated text from the response
        answer = response.choices[0].message.content
        answer = answer.replace("AI", "Pepega")
    except Exception as e:
        # Handle any exceptions that may occur during the API request
        answer = f"Sorry, I couldn't generate a response. Error message: {e}"

    return answer