from pico_controller import Pico
from components.led import LED
from components.button import Button
from components.slide_switch import Slide
from components.keypad import Keypad
from components.relay import Relay
from components.buzzer import Buzzer

from machine import Pin
from pico_constants import BUTTON_PIN, LED1_PIN, LED3_PIN, SLIDE_PIN, RELAY_PIN, BUZZER_PIN
import utime

## Setting Up
pico = Pico(0)

red_led = LED(LED1_PIN)
green_led = LED(LED3_PIN)

buzz = Buzzer(BUZZER_PIN)

solenoid_relay = Relay(RELAY_PIN)

slide = Slide(SLIDE_PIN)
keypad = Keypad(
    4, 4, 
    # [15, 14, 13, 12, 11, 10, 9, 8],
    [8, 9, 10, 11, 12, 13, 14, 15], 
    [['1','2',"3",'A'],['4','5','6','B'],['7','8','9','C'], ['*','0',"#","D"]]        
    )

def leff_keypad_operation():
    red_led.on()
    ## Keypad function will start.
    print("Checking Keypad input...")
    
    if keypad.check_pwd():
        green_led.on()
        buzz.play_short(500)
        solenoid_relay.off()
        red_led.off()
        utime.sleep(3)
        green_led.off()

def right_camera_operation():
    ## Send data to Rpi to start Face Recognition process
    pico.send_data('start')
    
    ## Add exit function if waiting time is over 30 second to receive data from Rpi
    while True:
        print("Pico waiting reply from Rpi...")
        if msg := pico.receive_data():
            red_led.off()
            print(f"Here's msg : {msg}")
            if msg == 'on':
                green_led.on()
                solenoid_relay.off()
                utime.sleep(2)
                green_led.off()
            break
        else:
            red_led.on()
            # utime.sleep(2)
    
def check_switch(pin):
    global switch_state
    global switched
    global last_switch_state
    switch_state = button.value()
    print(f"Switch Value : {switch_state}")
    if switch_state != last_switch_state:
        switched = True
    last_switch_state = switch_state
    print("Ending Interrupt handler func.")
    return
        
button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)
switch_state = button.value()
last_switch_state = switch_state
switched = False

## Setting irq
button.irq(trigger=Pin.IRQ_FALLING, handler=check_switch)
while True:
    ## At the beginning , disable irq interrupt
    
    ## Open Solenoid
    solenoid_relay.on()
    
    ## Check & Get Slider Position
    slide.set_slide_pos()
    slide_pos = slide.get_slide_pos()
    
    print(f"Slide: {slide_pos}, SS: {switch_state}, S: {switched}, LSS: {last_switch_state}")
    
    if switched:
        if switch_state == 1:
            if slide_pos == 'Left':
                leff_keypad_operation()

            elif slide_pos == 'Right':
                right_camera_operation()
        switched = False
                                
    utime.sleep_ms(200)
