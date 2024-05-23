from machine import UART, Pin
import utime 

pico_uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

led = Pin(16, Pin.OUT)

while True:
    if pico_uart.any():
        
        msg = pico_uart.read().decode()
        print(f"Receiving msg {msg} from Rpi ...")
        
        if msg == "on":
            led.value(1)
        else:
            led.value(0)