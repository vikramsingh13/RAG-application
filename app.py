import os
from openai import OpenAI
from dotenv import load_dotenv


# Load the enviroment variables from .env
load_dotenv()

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.getenv("OPENAI_API_KEY"),
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Say this is a test",
        }
    ],
    model="gpt-3.5-turbo",
)

print(chat_completion.choices[0].message.content)