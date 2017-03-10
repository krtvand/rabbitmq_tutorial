import pika
import time


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    time.sleep(body.count(b'.'))
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


connection = pika.BlockingConnection(pika.ConnectionParameters(
               'localhost'))
channel = connection.channel()

# When RabbitMQ quits or crashes it will forget the queues and messages unless
#  you tell it not to. Two things are required to make sure that messages
# aren't lost: we need to mark both the queue and messages as durable.
channel.queue_declare(queue='task_queue', durable=True)

# the prefetch_count=1 setting. This tells RabbitMQ not to give more than one
# message to a worker at a time. Or, in other words, don't dispatch a new
# message to a worker until it has processed and acknowledged the previous
# one. Instead, it will dispatch it to the next worker that is not still busy.
channel.basic_qos(prefetch_count=1)

channel.basic_consume(callback,
                      queue='task_queue')

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
