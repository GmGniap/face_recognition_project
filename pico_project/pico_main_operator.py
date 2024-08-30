from components.slide_switch import Slide
from pico_operations import left_keypad_operation, right_camera_operation, door_close
from machine import Pin
from pico_constants import BUTTON_PIN, SLIDE_PIN
import utime

class PicoMainOperator:
    def __init__(self) -> None:
        ## Setting Input Devices (Switches)
        self.slide = Slide(SLIDE_PIN)
        self.button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)
        self.switch_state = self.button.value()
        self.last_switch_state = self.switch_state
        self.switched = False
        ## Setting irq
        self.button.irq(trigger=Pin.IRQ_FALLING, handler=self.check_switch)
        
        self.slide_pos = None ## It shouldn't be assigned as default 'Left', right?
    
    def check_switch(self, pin):
        """
        Interrupt handler function to be called with button is click
        """
        self.switch_state = self.button.value()
        if self.switch_state != self.last_switch_state:
            self.switched = True
        self.last_switch_state = self.switch_state
        print("End Interrupt handler func.")
    
    def run_operation_BySwitchData(self):
        """
        Depend on switches data, run keypad (or) camera operations
        """
        if self.switched:
            if self.switch_state == 1:
                if self.slide_pos == 'Left':
                    left_keypad_operation()

                elif self.slide_pos == 'Right':
                    right_camera_operation()
            self.switched = False
    
    def main(self):
        try:
            ## Main code block that will indefinitely run
            while True:
                ## Start -> Door Close condition
                door_close()
                
                ## Check & Get Slider Position
                self.slide.set_slide_pos()
                self.slide_pos = self.slide.get_slide_pos()
                
                print(f"Slide: {self.slide_pos}, SS: {self.switch_state}, S: {self.switched}, LSS: {self.last_switch_state}")
                
                ## Left -> Keypad operation , Right -> Camera operation
                self.run_operation_BySwitchData()                          
                utime.sleep_ms(200)
        except Exception as e:
            print(f"Error : {str(e)}")
            
