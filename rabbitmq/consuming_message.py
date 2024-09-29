import aio_pika
from dotenv import load_dotenv
import os

load_dotenv()

RMQ_HOST = os.getenv("RMQ_HOST")
RMQ_PORT = os.getenv("RMQ_PORT")
RMQ_USER = os.getenv("RABBITMQ_DEFAULT_USER")
RMQ_PASSWORD = os.getenv("RABBITMQ_DEFAULT_PASS")

RABBITMQ_URL = f'amqp://{RMQ_USER}:{RMQ_PASSWORD}@{RMQ_HOST}:{RMQ_PORT}/'

async def rabbit_consumer():
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    channel = await connection.channel()  
    queue = await channel.declare_queue('book action', durable=True)
    print("Connecting to RabbitMQ and waiting for messages...")
    async for message in queue:
        async with message.process():
            print(f"Message: {message.body.decode()}")























# def callback(ch, method, properties, body: bytes):
#     print(body.decode('utf-8'))

# def rabbit_consumer():
#     with rebbit_coonection() as connection:
#         with connection.channel() as channel:
#             channel.queue_declare(queue='book action')
#             channel.basic_consume(
#                     queue='book action',
#                     on_message_callback=callback,
#                     auto_ack=True
#                 )
#             channel.start_consuming()