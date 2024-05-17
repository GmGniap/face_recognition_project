## Get all person folders inside train_images
## Get each person name from folder 
## Image encodings
## Match with names & encodings

from pathlib import Path
import face_recognition
import pickle

names = []
encodings = []

for path in Path('train_images').iterdir():
    if path.is_dir():
        person_name = path.name
        print(f"Person : {person_name}")
    
        for img_file in path.glob('*.jpg'):
            print(img_file)
            image = face_recognition.load_image_file(img_file)

            face_location = face_recognition.face_locations(image, model='hog')
            
            ## check training_img has only 1 person face
            if len(face_location) > 1:
                raise ValueError(f"There're more than 1 person in training image : {person_name}")
            
            face_encodings = face_recognition.face_encodings(image, face_location)
            print(f"Length of encodings : {len(face_encodings)}")
            if len(face_encodings) < 1 or len(face_encodings) > 1:
                print("Can't train model for this image")
                continue
            ## There will be only 1 encoding as result
            names.append(person_name)
            encodings.append(face_encodings[0])
    print("---x---")
        
name_encodings = {'names': names, 'encodings': encodings}

model_name = input("Enter model name for this training : ").strip().replace(" ", "_")
encodings_location = Path(f'output/{model_name}.pickle')
with encodings_location.open(mode='wb') as f:
    pickle.dump(name_encodings, f)