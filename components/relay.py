from machine import Pin
class Relay:
    def __init__(self, relay_pin_id) -> None:
        self.relay_pin = Pin(relay_pin_id, Pin.OUT)
        
        ## default used connection - Normal Open
        self.relay_state = False 
    
    def on(self):
        self.relay_pin.value(0)
        
    def off(self):
        self.relay_pin.value(1)