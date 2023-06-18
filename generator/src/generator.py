import sys
import json
import socket
import logging

import pandas as pd

from confluent_kafka import SerializingProducer


logger = logging.getLogger('GENERATOR')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)-15s %(levelname)-8s %(message)s'))
logger.addHandler(handler)


def json_serializer(msg, s_obj):
    return json.dumps(msg).encode('utf-8')


class HistoryProducer:
    def __init__(self, topic=None, main_source_file=None) -> None:
        conf = {
            'bootstrap.servers': "kafka-1:9092",
            'client.id': socket.gethostname(),
            'value.serializer': json_serializer
        }

        self.producer = SerializingProducer(conf)
        self.topic = topic if topic else "history-topic"
        self.main_source_file = main_source_file if main_source_file else sys.argv[1]

    def main_loop(self):

        infile = open(self.main_source_file, "r")
        df = pd.read_csv(infile)

        for msg in df.to_dict(orient="records"):
            self.send(msg)

    def send(self, message):
        self.producer.produce(self.topic, value=message)
        self.producer.flush()


if __name__ == '__main__':
    producer = HistoryProducer("history-topic", sys.argv[1])
    producer.main_loop()
