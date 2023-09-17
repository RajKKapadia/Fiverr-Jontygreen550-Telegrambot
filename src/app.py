import os
import json


from outside_apis.telegram_api import send_message, set_webhook
from helper.utils import process_request, generate_response
from outside_apis.database_api import get_user, create_user, update_messages

from flask import Flask, request
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)


@app.route('/')
def home():
    return 'All is well...'


@app.route('/telegram', methods=['POST'])
def telegram_api():
    if request.is_json:
        body = request.get_json()
        data = process_request(body)
        # Make sure the request has text and is not from a Telegram bot
        if data['is_text'] and not data['is_bot']:
            # Check user exists
            user = get_user(data['sender_id'])
            if user:
                response = generate_response(
                    data['message'], user['messages'])
                update_messages(data['sender_id'], data['message'], response)
                _ = send_message(data['sender_id'], response)
            # IF user does not exists
            else:
                response = generate_response(data['message'], [])
                create_user(data, response)
                _ = send_message(data['sender_id'], response)
        # Message is from bot, send myself an alert
        elif data['is_bot']:
            response = 'I know you are a bot.'
            _ = send_message(data['sender_id'], response)
        # For everything else coming to the bot, IGNORE
        else:
            pass
        return 'OK', 200
    else:
        _ = send_message(os.getenv('ME'), 'Fire in the whole.')
        return 'OK', 200


@app.route('/set-telegram-webhook', methods=['POST'])
def set_telegram_webhook():
    if request.is_json:
        body = request.get_json()
        flag = set_webhook(body['url'], body['secret_token'])
        if flag:
            return 'OK', 200
        else:
            return 'BAD REQUEST', 400
    else:
        return 'BAD REQUEST', 400
