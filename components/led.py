from machine import Pin
class LED:
    def __init__(self, led_pin_id) -> None:
        self.led = Pin(led_pin_id, Pin.OUT)
        
        ## Tracking led condition : on (or) off
        self.led_state = False
    
    def on(self):
        self.led_state = True
        self.led.value(1)
    
    def off(self):
        self.led_state = False
        self.led.value(0)
    
    def toggle(self):
        self.led_state = not self.led_state
        self.led.toggle()
    
    def get_led_state(self):
        return self.led_state