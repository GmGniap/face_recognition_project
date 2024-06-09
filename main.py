from rpi_controller import RaspberryPi
from face_recog_rpi import FaceRecognitionPi
from pathlib import Path
import time

model_path = Path('output/June8_MODEL3.pickle')
rpi = RaspberryPi()

while True:
    if rpi.receive_data() == 'start':
        ## Testing Code
        recogTask = FaceRecognitionPi(model_path)

        try:
            name = recogTask.recognize_face()
            if name != 'Unknown':
                print(f"Allow access for {name}")
            else:
                print(f"Can't allow for {name}")
        except Exception as e:
            print(f"Error from main.py : {str(e)}")