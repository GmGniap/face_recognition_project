from machine import Pin
import utime

led = Pin(16, Pin.OUT)
pin = Pin(2, Pin.IN, Pin.PULL_UP)
counter = 0
state = 0

while True:
    if pin.value()==0:
        if state == 0:
            led.value(1)
            utime.sleep_ms(100)
            while pin.value() == 0:
                state = 1
        else:
            led.value(0)
            utime.sleep_ms(100)
            while pin.value() == 0:
                state = 0