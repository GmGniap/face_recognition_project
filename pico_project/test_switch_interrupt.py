from machine import Pin
from pico_constants import BUTTON_PIN
from utime import sleep_ms

def check_switch(p):
  global switch_state
  global switched
  global last_switch_state
  print(f"Switch Value : {switch.value()}")
  switch_state = switch.value()
  if switch_state != last_switch_state:
    switched = True
  last_switch_state = switch_state
  print("Ending Interrupt handler func.")

switch = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)
switch_state = switch.value()
last_switch_state = switch_state
switched = False

## Setting irq
switch.irq(trigger=Pin.IRQ_FALLING, handler=check_switch)

while True:
    
    if switched:
        if switch_state == 1:
            print('tipped')
            print('--x--')
        switched = False
    sleep_ms(100)