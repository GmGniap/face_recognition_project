from pico_constants import BUTTON_PIN, RED_PIN, GREEN_PIN, YELLOW_PIN
from components.led import LED
from components.button import Button

lst_leds = [RED_PIN, GREEN_PIN, YELLOW_PIN]
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

    