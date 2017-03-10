"""
То же самое, что и hellow world, но добавляется routing_key для продюсера и очереди
"""

import sys

import pika


def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))


connection = pika.BlockingConnection(pika.ConnectionParameters(
               'localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='direct_logs',
                         type='direct')

# Firstly, whenever we connect to Rabbit we need a fresh, empty queue.
# To do it we could create a queue with a random name, or, even
# better - let the server choose a random queue name for us. We can do this
# by not supplying the queue parameter to queue_declare:
# Secondly, once we disconnect the consumer the queue should be deleted.
# There's an exclusive flag for that:
result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

severities = sys.argv[1:]
if not severities:
    sys.stderr.write("Usage: %s [info] [warning] [error]\n" % sys.argv[0])
    sys.exit(1)

# The routing algorithm behind a direct exchange is simple - a message goes to
# the queues whose binding key exactly matches the routing key of the message
for severity in severities:
    channel.queue_bind(exchange='direct_logs',
                       queue=queue_name,
                       routing_key=severity)

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()