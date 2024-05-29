from rpi_controller import RaspberryPi
from face_recog_rpi import FaceRecognitionPi
from pathlib import Path
import time

model_path = Path('output/May18.pickle')
rpi = RaspberryPi()

while True:
    if rpi.receive_data() == 'start':
        ## Testing Code
        test = FaceRecognitionPi()

        status, name = test.recognize_face(model_path)
        if status == 200:
            print(f"Allow access for {name}")
            rpi.send_data('on')
            print("Sent data!")
            time.sleep(10)
            rpi.send_data('off')
        else:
            print(f"Can't allow for {name}")
