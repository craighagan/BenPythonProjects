# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import uos, machine
import network
#uos.dupterm(None, 1) # disable REPL on UART(0)
import gc
import webrepl

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('na', 'deadbeef')


while not sta_if.isconnected():
    pass

webrepl.start()

gc.collect()




