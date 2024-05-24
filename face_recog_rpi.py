import face_recognition
import pickle
from numpy import argmin
import cv2
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
            
            ## Convert to Gray for face detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            ## run opencv face detection
            face_cascade = cv2.CascadeClassifier(f'{cv2.data.haarcascades}haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
            
            if len(faces) < 1:
                print("No face detected!")
            elif len(faces) > 1:
                print(f"Multiple {len(faces)} faces more than 1.")
            else:
                print("Only 1 face detected!")
                for (x,y,w,h) in faces:
                    roi_color = frame[y:y+h, x:x+w]
                    cv2.imwrite('camera.jpg', roi_color)
                    image = face_recognition.load_image_file('camera.jpg')
                    
                    face_location = face_recognition.face_locations(image, model="hog")
                    face_encoding = face_recognition.face_encodings(image, face_location)
                ## return first & only encoding
                return face_encoding[0]
        
    def recognize_face(self, model_path):
        camera_encoding = self.take_webcam_img()
        train_model = self.read_pickle_model(model_path)
        boolean_matches = face_recognition.compare_faces(
            train_model['encodings'], camera_encoding
        )
        
        face_distances = face_recognition.face_distance(train_model['encodings'], camera_encoding)
        
        best_match_index = argmin(face_distances)
        print(set(train_model['names']))
        if boolean_matches[best_match_index]:
            name = train_model['names'][best_match_index]
            print(name)
        else:
            print("something")

