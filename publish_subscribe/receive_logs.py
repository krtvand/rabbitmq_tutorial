import pika
import time


def callback(ch, method, properties, body):
    print(" [x] %r" % body)


connection = pika.BlockingConnection(pika.ConnectionParameters(
               'localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs',
                         type='fanout')

# Firstly, whenever we connect to Rabbit we need a fresh, empty queue.
# To do it we could create a queue with a random name, or, even
# better - let the server choose a random queue name for us. We can do this
# by not supplying the queue parameter to queue_declare:
# Secondly, once we disconnect the consumer the queue should be deleted.
# There's an exclusive flag for that:
result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

# We've already created a fanout exchange and a queue. Now we need to tell the
#  exchange to send messages to our queue. That relationship between exchange
# and a queue is called a binding.
channel.queue_bind(exchange='logs',
                   queue=queue_name)

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()