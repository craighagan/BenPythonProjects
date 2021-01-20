# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
# esp.osdebug(None)
import uos
import machine
import network
# uos.dupterm(None, 1) # disable REPL on UART(0)
import gc
import webrepl
import passwords

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect(passwords.wifi_ssid, passwords.wifi_psk)


while not sta_if.isconnected():
    machine.idle()

webrepl.start()

gc.collect()
