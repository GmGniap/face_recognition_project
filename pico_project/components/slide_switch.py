from machine import Pin

class Slide:
    def __init__(self, slide_id) -> None:
        self.slide_pin = Pin(slide_id, Pin.IN, Pin.PULL_UP)
        self.slide_pos = None
    
    def set_slide_pos(self):
        '''
        Default : Left(GND) -> 0, Right(Postive) -> 1
        '''
        if self.slide_pin.value() == 0:
            self.slide_pos = "Left"
        else:
            self.slide_pos = "Right"
    
    def get_slide_pos(self):
        return self.slide_pos
    
    