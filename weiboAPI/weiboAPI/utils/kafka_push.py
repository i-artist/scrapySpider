from kafka import KafkaProducer
from kafka.errors import KafkaError
import json
class weiboUserPushKafka(object):
    def __init__(self,KafkaTopic):
        self.kafkaHost = "139.198.0.141"
        self.kafkaPort = "9092"
        self.kafkaTopic = KafkaTopic
        self.producer = KafkaProducer(
            bootstrap_servers = "{kafka_host}:{kafka_port}".format(
                kafka_host = self.kafkaHost,
                kafka_port = self.kafkaPort
            )
        )
    def push(self,item):
        params_message = json.dumps(dict(item))
        producer = self.producer
        try:
            producer.send(self.kafkaTopic,params_message.encode("utf-8"))
            producer.flush()
        except KafkaError as e:
            print(e)