import json

from flask import request

from outside_apis.openai_api import chat_complition


def process_request(body: dict) -> dict:
    '''
    Process the incoming data of the Telegram request

    Parameters:
        - body(dict)

    Returns:
        - dict of these key and value 
        {
            'is_text': is_text,
            'is_chat_deleted': is_chat_deleted,
            'sender_id': sender_id,
            'message': message,
            'secret_token': secret_token,
            'first_name': first_name
        }
    '''

    body = request.get_json()

    message = ''
    is_bot = True
    is_text = False
    first_name = ''
    sender_id = None

    if 'message' in body.keys():
        sender_id = body['message']['from']['id']
        first_name = body['message']['from']['first_name']
        is_bot = body['message']['from']['is_bot']

        if 'text' in body['message'].keys():
            message += body['message']['text']
            is_text = True

    return {
        'is_text': is_text,
        'sender_id': sender_id,
        'message': message,
        'first_name': first_name,
        'is_bot': is_bot
    }


def format_messages(messages: list[dict], query: str) -> list[dict]:
    formated_messages = []
    formated_messages.append(
        {"role": "system", "content": "You are a helpful assistant."}
    )
    for message in messages:
        formated_messages.append(
            {
                "role": "user",
                "content": message['query']
            }
        )
        formated_messages.append(
            {
                "role": "assistant",
                "content": message['response']
            }
        )
    formated_messages.append(
        {
            "role": "user",
            "content": query
        }
    )
    return formated_messages


def generate_response(query: str, messages: list[dict]) -> str:
    '''
    Process the incoming message for different command and generate a response string

    Parameters:
        - message(str): incoming message from Telegram

    Returns:
        - str: formated response for the command
    '''
    formated_messages = format_messages(messages, query)
    result = chat_complition(formated_messages)
    return result['response']
