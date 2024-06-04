from machine import Pin, UART
from pico_constants import UART_DICT
import utime

class Pico:
    def __init__(self, uart_num) -> None:
        if uart_num in UART_DICT.keys():
            tx_pin, rx_pin = UART_DICT[uart_num]
            self.pico_uart = UART(uart_num, baudrate=9600, tx=Pin(tx_pin), rx=Pin(rx_pin))
        else:
            raise ValueError("UART num isn't included in dictionary.")
    
    def send_data(self, data, sending_times = None):
        # for _ in range(sending_times):
        self.pico_uart.write(f"{data}\n")
        utime.sleep_ms(200)
    
    def receive_data(self):
        while self.pico_uart.any() > 0:
            msg = self.pico_uart.read().decode()
            print(f"Receiving msg {msg} from Rpi.")
            return msg
        
    def get_uart(self):
        return self.pico_uart
            