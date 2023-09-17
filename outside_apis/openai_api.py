import os


import openai
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


openai.api_key = os.getenv('OPENAI_API_KEY')


def chat_complition(messages: list[dict]) -> dict:
    '''
    Call Openai API for chat completion

    Parameters:
        - prompt: user query (str)

    Returns:
        - dict
    '''
    try:
        response = openai.ChatCompletion.create(
            model='gpt-4',
            messages=messages
        )
        return {
            'status': 1,
            'response': response['choices'][0]['message']['content']
        }
    except:
        return {
            'status': 0,
            'response': ''
        }
