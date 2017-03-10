"""
То же самое, что и routing, но routing_key состоит из нескольких аргументов
"""

import sys

import pika


message = ' '.join(sys.argv[2:]) or "Hello World!"

connection = pika.BlockingConnection(pika.ConnectionParameters(
               'localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='topic_logs',
                         type='topic')
routing_key = sys.argv[1] if len(sys.argv) > 2 else 'anonymous.info'

channel.basic_publish(exchange='topic_logs',
                      routing_key=routing_key,
                      body=message)
print(" [x] Sent %r:%r" % (routing_key, message))

# Before exiting the program we need to make sure the network buffers were
# flushed and our message was actually delivered to RabbitMQ. We can do it
# by gently closing the connection.
connection.close()



