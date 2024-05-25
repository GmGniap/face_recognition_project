## Follow Tutorial from this link - https://electrocredible.com/raspberry-pi-pico-external-interrupts-button-micropython/

from machine import Pin
import utime
led = Pin(16, Pin.OUT)
pin = Pin(2, Pin.IN, Pin.PULL_UP)
interrupt_flag = 0
debounce_time = 0

def callback(pin):
    global interrupt_flag, debounce_time
    if (utime.ticks_ms() - debounce_time) > 500:
        print("Callback function")
        if pin.value() == 0:
            print("Zero")
        else:
            print("One")
        interrupt_flag= 1
        debounce_time = utime.ticks_ms()

pin.irq(trigger=Pin.IRQ_FALLING, handler=callback)
while True:
    if interrupt_flag == 1:
        utime.sleep_ms(1000)
        print("Interrupt has occured!")
        interrupt_flag = 0
        led.toggle()
        
    else:
        print(f"Normal condition : {pin.value()}")
        