# from constants import BUTTON_PIN
from machine import Pin
import utime
class Button:
    def __init__(self, button_pin, callback=None) -> None:
        self.button_pin = Pin(button_pin, Pin.IN, Pin.PULL_UP)
        self.callback = callback ## for STOP function
        
        ## set irq 
        self.button_pin.irq(trigger=Pin.IRQ_FALLING, handler=self.irq_handler)
        
        self.interrupt_flag = False
        self.debounce_time = 0
        print("Setting button pins - Done!")
        
    
    def irq_handler(self, irq_pin):
        print("Starting IRQ ")
        ## add delay - why?
        # utime.sleep_ms(100)
        
        # if (utime.ticks_ms() - self.debounce_time) > 500:
        print("IRQ Handler function")
        self.interrupt_flag = True
        
        if self.callback is not None:
            self.callback(irq_pin)
                
            # self.debounce_time = utime.ticks_ms()
    
    def deinit(self):
        self.button_pin.irq(trigger=0, handler=None)