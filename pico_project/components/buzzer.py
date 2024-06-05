from machine import Pin, PWM
from utime import sleep

class Buzzer:
    def __init__(self, buzzer_pin) -> None:
        self.buzzer = PWM(Pin(buzzer_pin, Pin.OUT))
        
    def play_short(self, freq_num):
        """
        freq_num : choose number between 10 and 12,000.
        higher the number, higher the pitch.
        """
        self.buzzer.freq(freq_num)
        self.buzzer.duty_u16(1000) ## highest loud
        sleep(2)
        self.buzzer.duty_u16(0)
        