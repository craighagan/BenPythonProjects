# Fishtank Sensor System

This project implements fishtank sensors using an ESP32
controller. It may work with an ESP8266 as well.

Right now, only temperature is supported, PH and other
sensors will be added in future.

This project supports pushing metrics to adafruit IO's mqtt service.

## Install micropython with esptool

esp8266 example:

```
esptool.py  --port /dev/ttyUSB0 --baud 460800 --before default_reset --after hard_reset erase_flash
```

```
esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=detect 0 ~/Downloads/esp8266-20200911-v1.13.bin
```

esp32 example:

```
esptool.py  --port /dev/ttyUSB0 --baud 460800 --before default_reset --after hard_reset erase_flash
```

```
esptool.py --chip esp32 --port /dev/ttyUSB0 write_flash -z 0x1000 ~/Downloads/esp32-idf3-20200902-v1.13.bin
```
## Parts:

1. ESP32 board: https://www.amazon.com/AITRIP-ESP32-DevKitC-Development-ESP32-WROOM-32D-Compatible/dp/B08HMJ1X6W
1. Temperature Sensor: https://www.amazon.com/gp/product/B00M1PM55K
1. SSD1306 Display: https://www.amazon.com/UCTRONICS-SSD1306-Self-Luminous-Display-Raspberry/dp/B072Q2X2LL
1. 4.7kOhm Resistor: https://www.amazon.com/Projects-100EP5124K70-4-7k-Resistors-Pack/dp/B0185FIIVE

## Assemble the Circuit

![circuit diagram](fishtank_bb.png)

## Create an Adafruit IO User

Go to https://accounts.adafruit.com/users/sign_up and create an account

Once your account is created, sign in, go to "IO" then click on "My Key". You will need
the information there for later.


## Get Your Adafruit IO Key

## Create webrepl_cfg.py file

Create the file "webrepl_cfg.py" with the following contents:

```
PASS = '<some password>'
```

## Create passwords.py File

Create the file "passwords.py" with the following contents, fill in where <> is with the actual value:

```
wifi_ssid = "<your wireless ssid>"
wifi_psk = "<your wireless password>"

adafruit_io_url = b"io.adafruit.com"
adafruit_io_username = b"<your adafruit io username>"
adafruit_io_key = b"<your adafruit io key>"
```
## upload the code via ampy:

```
pip3 install adafruit-ampy
```

```
ampy -p /dev/ttyUSB0 put fishtank.py
ampy -p /dev/ttyUSB0 put passwords.py
ampy -p /dev/ttyUSB0 put ssd1306.py
ampy -p /dev/ttyUSB0 put adafruit_mqtt.py
ampy -p /dev/ttyUSB0 put boot.py
ampy -p /dev/ttyUSB0 put main.py
```
# Connecting to your device remotely

If you want to remotely debug your device, you can use http://micropython.org/webrepl/?#<your device's ip address>:8266/ e.g. http://micropython.org/webrepl/?#192.168.1.104:8266/

From there, click "connect", you should get prompted for a password, then you'll see the console output. You can stop execution by pressing Control-C.

# Footnotes/Resources

## ssd1306 code and library from:

https://randomnerdtutorials.com/micropython-oled-display-esp32-esp8266/

## DSP example and some code from:

https://randomnerdtutorials.com/micropython-ds18b20-esp32-esp8266/

