import os 
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI( api_key=st.secrets["API_KEY"], 
                 #api_key=os.environ.get("API_KEY")
                )

async def call_openai(message):
    """
    This function calls an openai model chat

    Args
    message(list[{}]): A set of messages to use to generate a message from

    Return
    res.choices[0].message.content: The message from OpenAI
    """
    res = client.chat.completions.create(
        model = "gpt-3.5-turbo-16k",
        messages = message
    )

    return res.choices[0].message.content
