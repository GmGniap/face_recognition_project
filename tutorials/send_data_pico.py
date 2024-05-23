import serial
import time

def main():
    s = serial.Serial(port="/dev/tty.usbmodem11201", baudrate=9600, parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_ONE, timeout=1)
    # s.flush()
    while True:
        print("Sending data...")
        s.write("on".encode())
        time.sleep(2)


if __name__ == "__main__":
    main()