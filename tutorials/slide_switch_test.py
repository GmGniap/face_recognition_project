import machine
import utime
button = machine.Pin(17, machine.Pin.IN, machine.Pin.PULL_UP)

while True:
    if button.value() == 0:
        print("Zero : Left")

    else:
        print("One : Right")
    utime.sleep(1)