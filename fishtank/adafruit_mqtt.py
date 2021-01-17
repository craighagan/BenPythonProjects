import os
from umqtt.robust import MQTTClient


class AdafruitMQTTClient(object):
    def __init__(self, mqtt_url, username, key):
        self.mqtt_url = mqtt_url
        self.username = username
        self.key = key
        self._mqtt_client = None

    @property
    def mqtt_client(self):
        if self._mqtt_client is None:
            random_num = int.from_bytes(os.urandom(3), 'little')
            mqtt_client_id = bytes('client_' + str(random_num), 'utf-8')

            client = MQTTClient(client_id=mqtt_client_id,
                                server=self.mqtt_url,
                                user=self.username,
                                password=self.key,
                                ssl=False)
            try:
                client.connect()
                self._mqtt_client = client

            except Exception as e:
                print('could not connect to MQTT server {}{}'.format(type(e).__name__, e))

        return self._mqtt_client

    def get_adafruit_feedname(self, metric):
        return bytes('{:s}/feeds/{:s}'.format(self.username, metric), 'utf-8')

    def publish_metric(self, metric, value):
        if self.mqtt_client:
            self.mqtt_client.publish(self.get_adafruit_feedname(metric), bytes(str(value), 'utf-8'),
                                     qos=0)
