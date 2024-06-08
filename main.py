from rpi_controller import RaspberryPi
from face_recog_rpi import FaceRecognitionPi
from pathlib import Path
import time

model_path = Path('output/May18.pickle')
rpi = RaspberryPi()

while True:
    if rpi.receive_data() == 'start':
        ## Testing Code
        test = FaceRecognitionPi(model_path)

        name = test.recognize_face()
        if name != 'Unknown':
            print(f"Allow access for {name}")
            rpi.send_data('on')
            print("Sent data!")
        else:
            print(f"Can't allow for {name}")
