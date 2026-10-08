import os

from app.utils.logger import logger

try:
    from kafka import KafkaProducer
    KAFKA_AVAILABLE = True
except ImportError:
    KafkaProducer = None
    KAFKA_AVAILABLE = False


class KafkaProducerClient:
    def __init__(self, topic: str):
        self.topic = topic
        self.bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
        self.producer = None
        if KAFKA_AVAILABLE:
            try:
                self.producer = KafkaProducer(bootstrap_servers=self.bootstrap_servers,
                                              value_serializer=lambda v: v.encode('utf-8'))
            except Exception:
                self.producer = None

    def send(self, message: str):
        if self.producer is None:
            logger.warning('Kafka unavailable; dropped message for topic %s', self.topic)
            return False
        self.producer.send(self.topic, message)
        self.producer.flush()
        return True
