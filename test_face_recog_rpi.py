from face_recog_rpi import FaceRecognitionPi
from pathlib import Path

model_path = Path('output/June8_MODEL2.pickle')
if __name__ == "__main__":
    face_recog = FaceRecognitionPi(model_path)
    name = face_recog.recognize_face()
    print(f"Matched person : {name}")