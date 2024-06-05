from components.buzzer import Buzzer
from pico_constants import BUZZER_PIN

buzz = Buzzer(BUZZER_PIN)

buzz.play_short(500)