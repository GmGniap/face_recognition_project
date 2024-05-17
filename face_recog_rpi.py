import face_recognition
import pickle
from pathlib import Path
import cv2

class FaceRecognitionPi:
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def read_pickle_model(MODEL_PATH : Path) -> dict:
        '''
        MODEL_PATH : Exact location of Pickle file that stored model
        Return : Reconstituted object hierarchy (which is Dict)
        '''
        
        ## check MODEL_PATH is a file
        if MODEL_PATH.is_file():
            with MODEL_PATH.open(mode="rb") as model:
                return pickle.load(model)
        else:
            raise ValueError("Provided path is wrong.")
    
    def take_webcam_img(self):
        ## open the webcam
        cap = cv2.VideoCapture(0)
        
        ## Check if the webcam is opened correctly
        if not cap.isOpened():
            raise Exception('Could not open webcam!')
        
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1200)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
        while True:
            ## Capture a frame
            ret, frame = cap.read()
            
            ## Show image
            cv2.imshow('WebCam', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()

# model_path = Path('output/encodings.pk1')
# print(type(model_path))
# fr = FaceRecognitionPi().read_pickle_model(model_path)
# print(type(fr))
# print(fr)

test = FaceRecognitionPi()
test.take_webcam_img()
