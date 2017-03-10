"""
То же самое, что и routing, но routing_key состоит из нескольких аргументов
"""

import sys

import pika


def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))


connection = pika.BlockingConnection(pika.ConnectionParameters(
               'localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='topic_logs',
                         type='topic')

# Firstly, whenever we connect to Rabbit we need a fresh, empty queue.
# To do it we could create a queue with a random name, or, even
# better - let the server choose a random queue name for us. We can do this
# by not supplying the queue parameter to queue_declare:
# Secondly, once we disconnect the consumer the queue should be deleted.
# There's an exclusive flag for that:
result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

binding_keys = sys.argv[1:]
if not binding_keys:
    sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
    sys.exit(1)

for binding_key in binding_keys:
    channel.queue_bind(exchange='topic_logs',
                       queue=queue_name,
                       routing_key=binding_key)

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()