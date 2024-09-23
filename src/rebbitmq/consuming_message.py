from .rebbit_coonection import rebbit_coonection


def callback(ch, method, properties, body: bytes):
    print(body.decode('utf-8'))

def rabbit_consumer():
    with rebbit_coonection() as connection:
        with connection.channel() as channel:
            channel.queue_declare(queue='book action')
            channel.basic_consume(
                    queue='book action',
                    on_message_callback=callback,
                    auto_ack=True
                )
            channel.start_consuming()