import os 
import re
import numpy as np
import PIL.Image
import face_recognition

# DEFAULT_ENCODING_PATH = Path('output/encodings.pk1')
# Path('output').mkdir(exist_ok=True)
# Path('validation').mkdir(exist_ok=True)

def list_imgs_under_folder(folder_path:str):
    return [os.path.join(folder_path, file) for file in os.listdir(folder_path) if re.match(r".*\.(jpg|jpeg|png)", file)]

def list_folders_under_folder(folder_path:str):
    sub_folders = []
    with os.scandir(folder_path) as it:
        for entry in it:
            if not entry.name.startswith('.') and entry.is_dir():
                sub_folders.append(os.path.join(folder_path, entry.name))
    return sub_folders
    
def train_known_folder(known_folder):
    known_names = []
    known_face_encodings = []
    for file in list_imgs_under_folder(known_folder):
        # print(os.path.splitext(os.path.basename(file)))
        
        ## get person folder name
        train_person_name = os.path.split(os.path.dirname(file))[1]
        
        image = face_recognition.load_image_file(file)
        
        encodings = face_recognition.face_encodings(image)
        
        if len(encodings) > 1 :
            print("WARNING : more than one face found!")
        elif len(encodings) == 0:
            print(f"WARNING : no face found. Skip this file {file}")
        else:
            known_names.append(train_person_name)
            known_face_encodings.append(encodings[0])
    return known_names, known_face_encodings

def print_result(filename, name, distance, show_distance=False):
    if show_distance:
        print("{},{},{}".format(filename, name, distance))
    else:
        print("Filename : {}, Name : {}".format(filename, name))
        
def test_image(image_to_check, known_names, known_face_encodings, tolerance=0.6, show_distance=False):
    unknown_image = face_recognition.load_image_file(image_to_check)

    # Scale down image if it's giant so things run a little faster
    if max(unknown_image.shape) > 1600:
        pil_img = PIL.Image.fromarray(unknown_image)
        pil_img.thumbnail((1600, 1600), PIL.Image.LANCZOS)
        unknown_image = np.array(pil_img)

    unknown_encodings = face_recognition.face_encodings(unknown_image)

    print(len(unknown_encodings))
    for unknown_encoding in unknown_encodings:
        distances = face_recognition.face_distance(known_face_encodings, unknown_encoding)
        result = list(distances <= tolerance)

        if True in result:
            print(f"Found! : {result}")
            [print_result(image_to_check, name, distance, show_distance) for is_match, name, distance in zip(result, known_names, distances) if is_match]
            print("---x---")
        else:
            print_result(image_to_check, "unknown_person", None, show_distance)

    if not unknown_encodings:
        # print out fact that no faces were found in image
        print_result(image_to_check, "no_persons_found", None, show_distance)


print(list_folders_under_folder('./train_images/'))

'''
kn , kfe = train_known_folder('./train_images/paing')
for test_img in list_imgs_under_folder("./test_images"):
    test_image(test_img, known_names= kn, known_face_encodings=kfe, tolerance=0.5, show_distance=False)

print("===x===")
print("Ye Naung Soe photossss")
kn , kfe = train_known_folder('./train_images/ye_naung_soe')
for test_img in list_imgs_under_folder("./test_images"):
    test_image(test_img, known_names= kn, known_face_encodings=kfe, tolerance=0.5, show_distance=False)
'''
