"""
То же самое, что и hellow world, но добавляется routing_key для продюсера и очереди
"""

import sys

import pika


message = ' '.join(sys.argv[2:]) or "Hello World!"

connection = pika.BlockingConnection(pika.ConnectionParameters(
               'localhost'))
channel = connection.channel()

# The fanout exchange is very simple. As you can probably guess from the name,
#  it just broadcasts all the messages it receives to all the queues it knows.
# And that's exactly what we need for our logger.
# Listing exchanges
# To list the exchanges on the server you can run the ever useful rabbitmqctl:
# $ sudo rabbitmqctl list_exchanges.
channel.exchange_declare(exchange='direct_logs',
                         type='direct')

severity = sys.argv[1] if len(sys.argv) > 2 else 'info'

# The routing algorithm behind a direct exchange is simple - a message goes to
# the queues whose binding key exactly matches the routing key of the message
channel.basic_publish(exchange='direct_logs',
                      routing_key=severity,
                      body=message)
print(" [x] Sent %r" % message)

# Before exiting the program we need to make sure the network buffers were
# flushed and our message was actually delivered to RabbitMQ. We can do it
# by gently closing the connection.
connection.close()



