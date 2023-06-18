import logging
import json
from collections import Counter
import tldextract


from confluent_kafka import Consumer, KafkaException, KafkaError


logger = logging.getLogger('CONSUMER')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)-15s %(levelname)-8s %(message)s'))
logger.addHandler(handler)


COUNTER = Counter()


def msg_process(msg):
    data = tldextract.extract(json.loads(msg.value())["url"])
    visit = {x: 1 for x in str(data.suffix).split(".")}
    COUNTER.update(visit)
    logger.info(COUNTER)


def basic_consume_loop(consumer, topics):
    try:
        consumer.subscribe(topics)
        while running:
            msg = consumer.poll(timeout=1.0)
            if msg is None: continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    logger.info('%% %s [%d] reached end at offset %d\n' %
                                     (msg.topic(), msg.partition(), msg.offset()))
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                msg_process(msg)
    finally:
        consumer.close()


def shutdown():
    running = False


if __name__ == '__main__':

    conf = {'bootstrap.servers': 'kafka-1:9092',
            'group.id': "super3",
            'enable.auto.commit': False,
            'auto.offset.reset': 'earliest',
            }

    consumer = Consumer(conf)
    running = True
    basic_consume_loop(consumer, ["history-topic"])
    shutdown()
