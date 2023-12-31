import os
from datetime import datetime
from typing import Any, List


from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()


client = MongoClient(os.getenv('CONNECTION_STRING'))
db = client[os.getenv('DB_NAME')]
user_collection = db[os.getenv('USER_COLLECTION')]


def update_messages(sender_id: int, query: str, response: str) -> bool:
    '''
    Update messages for the user and reduce the messages_count by one

    Parameters:
        - sender_id(int): user telegram id
        - response(str): response of the bot
        - query(str): query of the user

    Returns:
        - bool, 0 for failure and 1 for success
    '''
    message = {
        'query': query,
        'response': response,
        'created_at': datetime.now().strftime('%d/%m/%Y, %H:%M')
    }

    result = user_collection.find_one_and_update(
        {
            'sender_id': sender_id
        },
        {
            '$push': {
                'messages': message
            }
        }
    )

    if not result:
        return False
    else:
        return True


def create_user(data: dict, response: str) -> bool:
    '''
    Process the whole body and update the db

    Parameters:
        - data(dict): the incoming request from Telegram

    Returns:
        - bool, 0 for failure and 1 for success
    '''

    message = {
        'query': data['message'],
        'response': response,
        'created_at': datetime.now().strftime('%d/%m/%Y, %H:%M')
    }

    user = {
        'first_name': data['first_name'],
        'sender_id': data['sender_id'],
        'messages': [message],
        'mobile': '',
        'name': '',
        'channel': 'Telegram',
        'is_paid': False,
        'created_at': datetime.now().strftime('%d/%m/%Y, %H:%M')
    }

    result = user_collection.insert_one(user)

    return result.acknowledged


def update_all_records(update: dict) -> bool:
    '''
    Update all documents in the collection

    Parameters:
        - update(dict): update to the documents

    Returns:
        - bool, 0 for failure and 1 for success
    '''

    result = user_collection.update_many(
        {},
        {
            '$set': update
        }
    )

    if not result:
        return False
    else:
        return True


def get_user(sender_id: int) -> Any:
    '''
    Get user

    Parameters:
        - sender_id(str): sender id of the user

    Returns:
        - bool, 0 for failure and 1 for success
    '''

    result = user_collection.find_one(
        {
            'sender_id': sender_id
        }
    )

    if not result:
        None
    return result


def get_all_user() -> List[int]:
    '''
    Get user

    Parameters:
        - sender_id(str): sender id of the user

    Returns:
        - bool, 0 for failure and 1 for success
    '''

    try:
        cursor = user_collection.find({})
        sender_ids = []
        for doc in cursor:
            sender_ids.append(doc['sender_id'])

        return sender_ids
    except:
        return []
