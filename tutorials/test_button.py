from machine import UART, Pin
import utime 

pico_uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
for _ in range(3):
    print("Sending data ...")
    pico_uart.write("start\n")
    utime.sleep_ms(400)
    
"""
def test(irq_pin):
    print(f"Value : {pin.value()} for flag {interrupt_flag}")
    
pin = Pin(2, Pin.IN, Pin.PULL_UP)
pin.irq(trigger=Pin.IRQ_FALLING, handler=test)
interrupt_flag = False
"""
