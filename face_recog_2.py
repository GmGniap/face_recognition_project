from pathlib import Path
import face_recognition
import pickle
from collections import Counter
from PIL import Image, ImageDraw, ImageFont
import cv2 as cv

DEFAULT_ENCODING_PATH = Path('output/encodings.pk1')

Path('train_images').mkdir(exist_ok=True)
Path('output').mkdir(exist_ok=True)
Path('validation').mkdir(exist_ok=True)

def encode_known_faces(
    model: str = 'hog', encodings_location: Path = DEFAULT_ENCODING_PATH
) -> None:
    names = []
    encodings = []
    for filepath in Path('train_images').glob('*/*'):
        name = filepath.parent.name
        image = face_recognition.load_image_file(filepath)

        face_locations = face_recognition.face_locations(image, model=model)
        face_encodings = face_recognition.face_encodings(image, face_locations)

        for encoding in face_encodings:
            names.append(name)
            encodings.append(encoding)

    name_encodings = {'names': names, 'encodings': encodings}
    with encodings_location.open(mode='wb') as f:
        pickle.dump(name_encodings, f)

def _recognize_face(unknown_encoding, loaded_encodings):
    boolean_matches = face_recognition.compare_faces(
        loaded_encodings['encodings'], unknown_encoding)
    votes = Counter(
        name
        for match, name in zip(boolean_matches, loaded_encodings['names'])
        if match
    )
    if votes:
        return votes.most_common(1)[0][0]

def _display_face(draw, bounding_box, name):
    BOUNDING_BOX_COLOR = "blue"
    TEXT_COLOR = "#ffff33"
    top, right, bottom, left = bounding_box
    draw.rectangle(((left, top), (right, bottom)), outline=BOUNDING_BOX_COLOR)
    text_left, text_top, text_right, text_bottom = draw.textbbox(
        (left, bottom), name
    )
    draw.rectangle(
        ((text_left, text_top), (text_right, text_bottom)),
        fill=BOUNDING_BOX_COLOR,
        outline=BOUNDING_BOX_COLOR,
    )
    draw.text(
        (text_left, text_top),
        name,
        fill=TEXT_COLOR,
    )
    
def recognize_faces(
    image_location: str,
    model: str = 'cnn',
    encodings_location: Path = DEFAULT_ENCODING_PATH,
) -> None:
    with encodings_location.open(mode='rb') as f:
        loaded_encodings = pickle.load(f)

    input_image = face_recognition.load_image_file(image_location)

    input_face_locations = face_recognition.face_locations(
        input_image, model=model)
    input_face_encodings = face_recognition.face_encodings(
        input_image, input_face_locations)

    pillow_image = Image.fromarray(input_image)
    draw = ImageDraw.Draw(pillow_image)

    for bounding_box, unknown_encoding in zip(
        input_face_locations, input_face_encodings
    ):
        name = _recognize_face(unknown_encoding, loaded_encodings)
        if not name:
            name = 'Unknown'
        print(name, bounding_box)
        _display_face(draw, bounding_box, name)

    del draw
    pillow_image.save('output.jpg')


recognize_faces("test_images/test.jpg")