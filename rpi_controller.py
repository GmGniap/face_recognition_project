import serial
from constants import UART_PORT, BAUDRATE

class RaspberryPi:
    """
    RaspberryPi UART communication using Pyserial Library
    """
    def __init__(self):
        self.UART_PORT = UART_PORT
        self.BAUDRATE = BAUDRATE
    
    def open_serial_conn(self, timeout_val):
        try:
            return serial.Serial(port = self.UART_PORT, baudrate = self.BAUDRATE, timeout=timeout_val)
        except serial.SerialException as e:
            print(f"Failed to open serial port {self.UART_PORT} : {str(e)}")
            raise
    
    @staticmethod
    def calculate_checksum(data_bytes):
        return sum(data_bytes) & 0xFF
    
    def send_data(self, text):
        msg = text.encode('utf-8')
        # checksum = self.calculate_checksum(msg)   ## I'm not sure why I should use checksum
        try:
            with self.open_serial_conn(2) as serial_port:
                serial_port.write(msg)
        except serial.SerialException as e:
            print(f"Error sending data : {str(e)}")
            
                
            