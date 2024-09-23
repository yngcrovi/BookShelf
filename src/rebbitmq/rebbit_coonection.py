from pika import BlockingConnection, ConnectionParameters, PlainCredentials
from dotenv import load_dotenv
import os

load_dotenv()

RMQ_HOST = os.getenv("RMQ_HOST")
RMQ_PORT = os.getenv("RMQ_PORT")
RMQ_USER = os.getenv("RABBITMQ_DEFAULT_USER")
RMQ_PASSWORD = os.getenv("RABBITMQ_DEFAULT_PASS")

connection_params = ConnectionParameters(
    host=RMQ_HOST,
    port=RMQ_PORT,
    credentials=PlainCredentials(
        RMQ_USER, RMQ_PASSWORD
    )
)
def rebbit_coonection() -> BlockingConnection:
    return BlockingConnection(
        parameters=connection_params
    )