import fishtank
from machine import Pin, I2C
import ssd1306

i2c = I2C(-1, scl=Pin(22), sda=Pin(21))

oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

sensor = fishtank.FishtankSensor(4)
webserver = fishtank.FishtankWebserver(sensor, oled)
webserver.start()



