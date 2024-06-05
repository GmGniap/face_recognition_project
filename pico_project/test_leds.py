from pico_constants import BUTTON_PIN, LED1_PIN, LED2_PIN, LED3_PIN
from components.led import LED
from components.button import Button
from utime import sleep

lst_leds = [LED1_PIN, LED2_PIN, LED3_PIN]
button = Button(BUTTON_PIN).get_button_pin()
count = 0
while True:
    if button.value() == 0:
        print("Button On")
        for led_pin in lst_leds:
            led = LED(led_pin)
            led.on()
    else:
        print("Button Off")
        for led_pin in lst_leds:
            led = LED(led_pin)
            led.off()

    