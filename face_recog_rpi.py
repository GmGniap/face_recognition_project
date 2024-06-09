import face_recognition
import pickle
from numpy import argmin
import cv2
import dlib
from pathlib import Path
from rpi_controller import RaspberryPi
import time
from custom_errors import CameraEncodingError

class FaceRecognitionPi(RaspberryPi):
    def __init__(self, model_path : Path) -> None:
        super().__init__()
        self.model_path = model_path
        ## To count multiple face & no face error
        self.error_count = 0
         
    def read_pickle_model(self) -> dict:
        '''
        MODEL_PATH : Exact location of Pickle file that stored model
        Return : Reconstituted object hierarchy (which is Dict)
        '''
        ## check MODEL_PATH is a file
        if self.model_path.is_file():
            with self.model_path.open(mode="rb") as model:
                return pickle.load(model)
        else:
            raise ValueError("Provided path is wrong.")
    
    @staticmethod
    def dlib_hog_method(img_gray):
        detector = dlib.get_frontal_face_detector()
        faces = detector(img_gray)
        return faces
    
    @staticmethod
    def haar_cascade_method(img_gray):
        face_cascade = cv2.CascadeClassifier(f'{cv2.data.haarcascades}haarcascade_frontalface_alt.xml')
        faces = face_cascade.detectMultiScale(
            img_gray,
            scaleFactor=1.3,
            minNeighbors=5,
            minSize=(100,100),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        return faces
    
    def select_detection_method(self, gray):
        if self.error_count <= 5:
            print("Dlib face detection method")
            faces = self.dlib_hog_method(gray)
        else:
            print("OpenCV haar cascade face detection method")
            faces = self.haar_cascade_method(gray)
            if self.error_count > 10:
                print("Reset error_count!")
                self.send_data('999') ## also reset pico code
                self.error_count = 0
        return faces
        
    def take_webcam_img(self):
        ## open the webcam
        cap = cv2.VideoCapture(0)
        
        ## Check if the webcam is opened correctly
        if not cap.isOpened():
            raise Exception('Could not open webcam!')
        
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 300)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 300)
        
        
        while True:
            ## Capture a frame
            ret, frame = cap.read()
            
            ## Convert to Gray for face detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            ## run face detection method - default OpenCV Cascade
            faces = self.select_detection_method(gray)
        
            if len(faces) < 1:
                print("No face detected!")
                self.send_data('000') 
                self.error_count += 1
                time.sleep(2)
                continue
            elif len(faces) > 1:
                print(f"Multiple {len(faces)} faces more than 1.")
                self.send_data('111')
                self.error_count += 1
                time.sleep(2)
                continue
            else:
                print(f"Only {len(faces)} face detected!")
                
                cv2.imwrite('camera.jpg', frame)
                image = face_recognition.load_image_file('camera.jpg')
                
                face_location = face_recognition.face_locations(image, model="hog")
                face_encoding = face_recognition.face_encodings(image, face_location)
                ## return first & only encoding
                return face_encoding[0] if len(face_encoding) == 1 else None
        
    def recognize_face(self):
        try:
            camera_encoding = self.take_webcam_img()
            if camera_encoding is None:
                raise CameraEncodingError("Camera Encoding return None!")
            
            train_model = self.read_pickle_model()
            boolean_matches = face_recognition.compare_faces(
                train_model['encodings'], camera_encoding, 0.35
            )
            
            face_distances = face_recognition.face_distance(train_model['encodings'], camera_encoding)
            best_match_index = argmin(face_distances)
            
            ## get all trained_names
            # print(set(train_model['names']))
            
            if boolean_matches[best_match_index]:
                if name := train_model['names'][best_match_index]:
                    ## Send authorized code to open door
                    self.send_data('on')
                    print("Sent authorized code!")
                    return name
                else:
                    print("Name not included!")
            else:
                print("Can't find in boolean_matches")
            return 'Unknown'
        except CameraEncodingError as e:
            print("Make sure your face is in front of camera!")
            time.sleep(2)
            self.recognize_face()
            
