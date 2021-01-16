

## install micropython with esptool

esp8266 example:

esptool.py  --port /dev/ttyUSB0 --baud 460800 --before default_reset --after hard_reset erase_flash

esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=detect 0 ~/Downloads/esp8266-20200911-v1.13.bin


esp32 example:

esptool.py  --port /dev/ttyUSB0 --baud 460800 --before default_reset --after hard_reset erase_flash

esptool.py --chip esp32 --port /dev/ttyUSB0 write_flash -z 0x1000 ~/Downloads/esp32-idf3-20200902-v1.13.bin


## upload the code via ampy:

pip3 install adafruit-ampy

ampy -p /dev/ttyUSB0 put main.py


## ssd1306 code and library from:

https://randomnerdtutorials.com/micropython-oled-display-esp32-esp8266/

## DSP example and some code from:

