# from constants import BUTTON_PIN
from machine import Pin

class Button:
    def __init__(self, button_pin, callback=None) -> None:
        self.button_pin = Pin(button_pin, Pin.IN, Pin.PULL_UP)
        self.callback = callback ## for STOP function
        
        ## set irq 
        self.button_pin.irq(trigger=Pin.IRQ_FALLING, handler=self.irq_handler)
        
        self.debounce_time = 0
        
        self.button_state = False ## Default off False -> click on True
        print("Setting button pins - Done!")
        
    def change_button_state(self):
        self.button_state = not self.button_state
    
    def get_button_state(self):    
        return self.button_state
    
    def set_button_state(self, value: bool):
        self.button_state = value
    
    def irq_handler(self, irq_pin):
        ## add delay - why?
        # utime.sleep_ms(100)
        
        # if (utime.ticks_ms() - self.debounce_time) > 500:
        print("Calling IRQ Handler function")
        
        ## change button_state - do I need to change here?
        # self.change_button_state()
        
        ## If clicked, set button_state to True
        self.set_button_state(True)
        
        if self.callback is not None:
            self.callback(irq_pin)
                
            # self.debounce_time = utime.ticks_ms()
        return
    
    def deinit(self):
        self.button_pin.irq(trigger=0, handler=None)