import utime
from components.led import LED
from components.buzzer import Buzzer
from components.relay import Relay
from components.keypad import Keypad
from pico_controller import Pico
from pico_constants import RED_PIN, GREEN_PIN, YELLOW_PIN, BUZZER_PIN, RELAY_PIN

## Setting up Output Devices
pico = Pico(0) ## Use UART 0 
red_led = LED(RED_PIN)
green_led = LED(GREEN_PIN)
yellow_led = LED(YELLOW_PIN)
buzz = Buzzer(BUZZER_PIN)
solenoid_relay = Relay(RELAY_PIN)

keypad = Keypad(
    4, 4, 
    # [15, 14, 13, 12, 11, 10, 9, 8],
    [8, 9, 10, 11, 12, 13, 14, 15], 
    [['1','2',"3",'A'],['4','5','6','B'],['7','8','9','C'], ['*','0',"#","D"]]        
    )

def door_open():
    green_led.on()
    buzz.play_short(500)
    solenoid_relay.off()
    utime.sleep(3)
    green_led.off()

def door_close():
    red_led.on()
    solenoid_relay.on()
    
def no_face_led():
    for _ in range(10):
        yellow_led.toggle()
        utime.sleep_ms(200)
    
def left_keypad_operation():
    red_led.on()
    ## Keypad function will start.
    print("Checking Keypad input...")
    
    if keypad.check_pwd():
        door_open()

def right_camera_operation():
    ## Send data to Rpi to start Face Recognition process
    pico.send_data('start')
    
    ## Add exit function if waiting time is over 20 seconds to receive data from Rpi
    max_wait_time = 60 ## Assume as seconds
    
    while max_wait_time > 0:
        print(f"Pico waiting reply from Rpi for {max_wait_time} seconds...")
        if msg := pico.receive_data():
            red_led.off()
            print(f"Here's msg : {msg}")
            if msg == 'on':
                door_open()
                break
            elif msg == '000' or '111':
                no_face_led()
                continue
            elif msg == '999':
                print("Resetting Pico.")
                break
        else:
            red_led.on()
        
        max_wait_time -= 1 ## reduce 1, then wait 1 sec
        utime.sleep(1)