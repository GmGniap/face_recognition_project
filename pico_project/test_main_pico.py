from pico_controller import Pico
from components.led import LED
from components.button import Button
from components.slide_switch import Slide
from components.keypad import Keypad
from components.relay import Relay

from pico_constants import BUTTON_PIN, LED1_PIN, LED3_PIN, SLIDE_PIN, RELAY_PIN
import utime

stop_flag = False
last_time = 0 ## the last time we pressed button

pico = Pico(0)

red_led = LED(LED1_PIN)
green_led = LED(LED3_PIN)

solenoid_relay = Relay(RELAY_PIN)

slide = Slide(SLIDE_PIN)
keypad = Keypad(
    4, 4, 
    # [15, 14, 13, 12, 11, 10, 9, 8],
    [8, 9, 10, 11, 12, 13, 14, 15], 
    [['1','2',"3",'A'],['4','5','6','B'],['7','8','9','C'], ['*','0',"#","D"]]        
    )

def callback_reset(pin):
    print(f"Reset here for {str(pin)}")

    '''
    ## what is the purpose of below if-statement?? no need?
    
    if not stop_flag and '16' in str(pin):
        print("1st time runner")
        # pico.send_data("start")
    else:
        print("Interrupt running task")
        # pico.send_data("start")
    stop_flag = not stop_flag
    '''
        

button = Button(button_pin=BUTTON_PIN, callback=callback_reset)

while True:
    ## Open Solenoid
    solenoid_relay.on()
    
    ## Check & Get Slider Position
    slide.set_slide_pos()
    slide_pos = slide.get_slide_pos()
    
    ## After knowing slider position, get button state
    button_state = button.get_button_state()

    print(f"S: {slide_pos}, B: {button_state}")
    if slide_pos == 'Left':
        red_led.on()
        ## Keypad function will start when button is pressed.
        if button_state:
            print("Checking Keypad input...")
            
            if keypad.check_pwd():
                solenoid_relay.off()
                red_led.off()
                green_led.on()
                utime.sleep(3)
                green_led.off()
                
            ## change back from True to False
            button.change_button_state()
            # break
    elif slide_pos == 'Right':
        if button_state:
            ## Send data to Rpi to start Face Recognition process
            pico.send_data('start')
            
            ## Waiting reply from Rpi
            while pico.get_uart().any():
                ## Add exit function if waiting time is over 30 second to receive data from Rpi
                if msg := pico.receive_data():
                    red_led.off()
                    print(f"Here's msg : {msg}")
                    if msg == 'on':
                        green_led.on()
                        solenoid_relay.off()
                        utime.sleep(2)
                        green_led.off()
                    ## After solenoid task, button_state need to change back to False
                    button.set_button_state(False)
                else:
                    red_led.on()
                    # utime.sleep(2)
                             
    utime.sleep_ms(200)
