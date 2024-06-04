import cv2
import os

from rpi_constants import VIDEO_WIDTH, VIDEO_HEIGHT, NUM_TRAINING_IMG
cap = cv2.VideoCapture(0)

## Check if the webcam is opened correctly
if not cap.isOpened():
    raise Exception('Could not open webcam!')

cap.set(cv2.CAP_PROP_FRAME_WIDTH, VIDEO_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, VIDEO_HEIGHT)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

## Asking face_id - do I need to ask?

def quit_opencv(cap):
    cap.release()
    cv2.destroyAllWindows()
def prep_training(person_name: str, count:int):
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        print(f"Detected face for {person_name} : {len(faces)}")
        if len(faces) < 1:
            print("Can't find face!")
            prep_training(person_name, count)
            
        for (x, y, w, h) in faces:
            # cv2.rectangle(gray, (x, y), (x + w, y + h), (255, 0, 0), 2)
            # roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y-25:y+h+25, x-25:x+w+25]
            cv2.namedWindow("taken_img", cv2.WINDOW_AUTOSIZE)
            cv2.imshow('taken_img', roi_color)
            key = cv2.waitKey()
            if key == ord('y'):
                print("Saving image")
                count += 1
                cv2.imwrite(f'/Users/thetpaing/Documents/Coding/face_recognition_project/train_images/{person_name}/{count}.jpg', roi_color)
                cv2.destroyWindow('taken_img')
            elif key == ord('n'):
                print("Retake image again!")
                prep_training(person_name, count) ## recall the function
            elif key == ord('q'):
                print("Quit")
                quit_opencv(cap)
        if count >= NUM_TRAINING_IMG:
            print("Image requirements meet!")
            quit_opencv(cap)
        print("---x---")

def main():
    ## Asking person_name
    person_name = input("Enter name of the person to take training data: ").strip().replace(" ","_")
    person_folder = f"./train_images/{person_name}"

    try:
        os.mkdir(person_folder)
        count = 0
        prep_training(person_name, count)
    except FileExistsError:
        print("Delete created folder")
        os.system(f"rm -rf {person_folder}")
        main()

if __name__ == "__main__":
    main()