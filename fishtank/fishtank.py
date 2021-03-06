"""

This implements a class to control and present sensor data for a fishtank


"""

import socket
import time
import os
import random

try:
    import network
    import machine
    import onewire
    import ds18x20
    import gc
    import passwords

    is_esp_device = True

except ImportError:
    # not on esp device
    import mock

    is_esp_device = False


class FishtankSensor(object):
    def __init__(self, temperature_pin):
        if is_esp_device:
            self.ds_pin = machine.Pin(temperature_pin)
            self.ds_sensor = ds18x20.DS18X20(onewire.OneWire(self.ds_pin))
        else:
            self.ds_sensor = mock.Mock()
            self.ds_sensor.scan.return_value = [self.ds_sensor]
            self.ds_sensor.read_temp.return_value = 71.123

    def get_temperature(self):
        try:
            # prep the sensor
            self.ds_sensor.convert_temp()
            time.sleep_ms(750) # wait for sensor to set up

            roms = self.ds_sensor.scan()
            print('Found DS devices: ', roms)
            print('Temperatures: ')
            for rom in roms:
                temp = self.ds_sensor.read_temp(rom)
                if isinstance(temp, float):
                    msg = round(temp, 2)
                    print(temp, end=' ')
                    print('Valid temperature')
                    return msg
        except Exception as e:
            print(str(e))

        return random.uniform(15, 30)


class FishtankWebserver(object):
    def __init__(self, temp_sensor, oled, mqtt_client=None,
                 port=80, refresh_secs=60, sensor_refresh_secs=30,
                 mqtt_publish_secs=60):
        self.port = port
        self.temp_sensor = temp_sensor
        self.refresh_secs = refresh_secs
        self.mqtt_publish_secs = mqtt_publish_secs
        self.last_mqtt_publish = 0
        self.oled = oled
        self._temp = None
        self._temp_last_updated = time.time()
        self.sensor_refresh_secs = sensor_refresh_secs
        self.network_info = None
        self.mqtt_client = mqtt_client

    def fahrenheit_to_celsius(self, temp):
        return round(temp * (9 / 5) + 32.0, 2)

    @property
    def temp(self):
        now = time.time()
        delta = now - self._temp_last_updated

        if delta < 0:
            # this shouldn't happen, did time wrap?
            machine.reset()

        if self._temp is None or delta > self.sensor_refresh_secs:
            self._temp = self.temp_sensor.get_temperature()
        return self._temp

    def serve_web_page(self):

        html = """<!DOCTYPE HTML><html><head>
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <meta http-equiv="refresh" content="%(refresh_secs)d">
      <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.2/css/all.css" integrity="sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr" crossorigin="anonymous">
      <style> html { font-family: Arial; display: inline-block; margin: 0px auto; text-align: center; }
        h2 { font-size: 3.0rem; } p { font-size: 3.0rem; } .units { font-size: 1.2rem; }
        .ds-labels{ font-size: 1.5rem; vertical-align:middle; padding-bottom: 15px; }
      </style></head><body><h2>ESP with DS18B20</h2>
      <p><i class="fas fa-thermometer-half" style="color:#059e8a;"></i>
        <span class="ds-labels">Temperature</span>
        <span id="temperature">%(celsius)0.2f</span>
        <sup class="units">&deg;C</sup>
      </p>
        <p><i class="fas fa-thermometer-half" style="color:#059e8a;"></i>
        <span class="ds-labels">Temperature</span>
        <span id="temperature">%(fahrenheit)0.2f</span>
        <sup class="units">&deg;F</sup>
      </p></body></html>""" % {
            "celsius": self.temp,
            "fahrenheit": self.fahrenheit_to_celsius(self.temp),
            "refresh_secs": self.refresh_secs
        }
        return html

    def update_display(self):

        # fill all pixels with color 0
        self.oled.fill(0)

        self.oled.text("%0.2fC" % self.temp, 0, 0)
        self.oled.text("%0.2fF" % self.fahrenheit_to_celsius(self.temp), 0, 20)

        if self.network_info:
            self.oled.text(self.network_info[0], 0, 40)

        self.oled.show()

        print("updated display")

    def update_mqtt(self):
        cur_time = time.time()
        if cur_time - self.last_mqtt_publish > self.mqtt_publish_secs:
            print("will update mqtt data")
            if self.mqtt_client:
                self.mqtt_client.publish_metric("temperature_F", self.fahrenheit_to_celsius(self.temp))

            self.last_mqtt_publish = cur_time

    def handle_requests(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        s.settimeout(5)  # listen timeout
        s.bind(('', self.port))
        s.listen(5)

        while True:
            try:
                if is_esp_device:
                    if gc.mem_free() < 102000:
                        gc.collect()

                self.update_mqtt()
                self.update_display()

                try:
                    conn, addr = s.accept()
                except Exception as e:
                    print(str(e))
                    continue

                conn.settimeout(3.0)
                print('Got a connection from %s' % str(addr))
                request = conn.recv(1024)
                conn.settimeout(None)
                request = str(request)
                if request:
                    print('Content = %s' % request)
                    response = self.serve_web_page()
                    conn.send('HTTP/1.1 200 OK\n')
                    conn.send('Content-Type: text/html\n')
                    conn.send('Connection: close\n\n')
                    conn.sendall(response.encode())
                conn.close()
            except OSError as e:
                conn.close()
                print(str(e))
                print('Connection closed')

    def connect_wifi(self):
        sta_if = network.WLAN(network.STA_IF)

        if not sta_if.isconnected():
            sta_if.active(True)
            sta_if.connect(passwords.wifi_ssid, passwords.wifi_psk)

        while not sta_if.isconnected():
            print("waiting to connect to wifi")
            machine.idle()

        self.network_info = sta_if.ifconfig()
        return(self.network_info)

    def start(self):
        print(self.connect_wifi())
        self.update_display()
        self.handle_requests()







