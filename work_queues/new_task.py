import sys

import pika


message = ' '.join(sys.argv[1:]) or "Hello World!"

connection = pika.BlockingConnection(pika.ConnectionParameters(
               'localhost'))
channel = connection.channel()

# When RabbitMQ quits or crashes it will forget the queues and messages unless
#  you tell it not to. Two things are required to make sure that messages
# aren't lost: we need to mark both the queue and messages as durable.
channel.queue_declare(queue='task_queue', durable=True)

channel.basic_publish(exchange='',
                      routing_key='task_queue',
                      body=message,
                      properties=pika.BasicProperties(
                          delivery_mode=2,  # make message persistent
                      ))
print(" [x] Sent %r" % message)

# Before exiting the program we need to make sure the network buffers were
# flushed and our message was actually delivered to RabbitMQ. We can do it
# by gently closing the connection.
connection.close()