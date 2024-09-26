import json
from .rebbit_coonection import rebbit_coonection
from pika import BasicProperties

def publish_message(action: str, action_param: dict | int | str):
    with rebbit_coonection() as connection:
        with connection.channel() as channel:
            channel.queue_declare(queue='book_action')
            message = {
                'action': action,
                'action_param': action_param
            }
            channel.basic_publish(
                exchange='',
                routing_key="book action",
                body=json.dumps(message),
                properties=BasicProperties(delivery_mode=2)
            )