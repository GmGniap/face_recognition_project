import face_recognition
import pickle
from pathlib import Path

class FaceRecognitionPi:
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def read_pickle_model(MODEL_PATH : Path) -> dict:
        '''
        MODEL_PATH : Exact location of Pickle file that stored model
        Return : Reconstituted object hierarchy (which is Dict)
        '''
        with MODEL_PATH.open(mode="rb") as model:
            return pickle.load(model)
    
    def take_webcam_img(self):
        pass

model_path = Path('output/encodings.pk1')
print(type(model_path))
fr = FaceRecognitionPi().read_pickle_model(model_path)
print(type(fr))
print(fr)
