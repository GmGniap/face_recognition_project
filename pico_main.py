from pico_controller import Pico
from components.led import LED
from components.button import Button
from constants import BUTTON_PIN, LED1_PIN
import utime

stop_flag = False

pico = Pico(0)
led = LED(LED1_PIN)

led.on()
utime.sleep(3)
print(led.get_led_state())
led.off()

def callback_reset(pin):
    global stop_flag
    stop_flag = not stop_flag
    print(f"Reset here - {stop_flag}")
    if stop_flag == False:
        print("1st time runner")
        pico.send_data("start")
    else:
        print("Interrupt running task")
        pico.send_data("start")
        

main_button = Button(button_pin=BUTTON_PIN, callback=callback_reset)
print("Main button set")
try:
    while True:
        if msg := pico.receive_data():
            print(f"Here's msg : {msg}")
            if msg == 'on':
                led.on()
                utime.sleep(2)
            else:
                led.off()
                utime.sleep(2)
        else:
            pass
except Exception as e:
    print(f"Something error : {str(e)}")
    


