import os
import threading

try:
    from kafka import KafkaConsumer
    KAFKA_AVAILABLE = True
except ImportError:
    KafkaConsumer = None
    KAFKA_AVAILABLE = False


class KafkaConsumerClient:
    def __init__(self, topic: str):
        self.topic = topic
        self.bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
        self.consumer = None
        if KAFKA_AVAILABLE:
            try:
                self.consumer = KafkaConsumer(self.topic, bootstrap_servers=self.bootstrap_servers,
                                              auto_offset_reset='earliest', enable_auto_commit=True,
                                              value_deserializer=lambda m: m.decode('utf-8'))
            except Exception:
                self.consumer = None

    def consume(self, callback):
        if self.consumer is None:
            print(f'[KafkaConsumer] Fallback consumer for topic {self.topic} cannot start.')
            return

        def _run():
            for message in self.consumer:
                callback(message.value)

        thread = threading.Thread(target=_run, daemon=True)
        thread.start()
        return thread
