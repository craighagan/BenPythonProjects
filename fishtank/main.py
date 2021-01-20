import fishtank
from machine import Pin, I2C
import machine
import time
import ssd1306
from adafruit_mqtt import AdafruitMQTTClient
import passwords



try:

    i2c = I2C(-1, scl=Pin(22), sda=Pin(21))

    oled_width = 128
    oled_height = 64
    oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

    sensor = fishtank.FishtankSensor(4)

    mqtt_client = AdafruitMQTTClient(passwords.adafruit_io_url,
                                     passwords.adafruit_io_username,
                                     passwords.adafruit_io_key)


    webserver = fishtank.FishtankWebserver(sensor, oled, mqtt_client=mqtt_client)
    webserver.start()


except Exception as e:
    print("something has gone wrong %s\nrebooting in 30 seconds" % str(e))
    time.sleep(30)
    machine.reset()
