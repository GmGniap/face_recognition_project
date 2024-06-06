import dlib
import cv2
# from rpi_constants import VIDEO_WIDTH, VIDEO_HEIGHT



cap = cv2.VideoCapture(0)

# cap.set(cv2.CAP_PROP_FRAME_WIDTH, VIDEO_WIDTH)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, VIDEO_HEIGHT)

def quit_opencv(cap):
    cap.release()
    cv2.destroyAllWindows()

def dlib_hog_method(img_gray):
    detector = dlib.get_frontal_face_detector()
    faces = detector(img_gray, 0)

    if len(faces) == 1:
        print("Dlib : single face detected!")
        for rect in faces:
            x = rect.left()
            y = rect.top()
            w = rect.right() - x
            h = rect.bottom() - y
            return (x,y,w,h)
    elif len(faces) > 1:
        print("Dlib : Multiple faces detected.")
    else:
        print("Dlib : No face detected!")

def haar_cascade_method(gray_img):
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = faceCascade.detectMultiScale(
        gray_img,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(100,100),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    if len(faces) == 1:
        print("Cascade : single face detected!")
        for (x,y,w,h) in faces:
            return (x,y,w,h)
    elif len(faces) > 1:
        print("Cascade : Multiple faces detected.")
    else:
        print("Cascade : No face detected!")


while cap.isOpened():
    flag, im_rd = cap.read()

    img_gray = cv2.cvtColor(im_rd, cv2.COLOR_RGB2GRAY)

    hog_result = dlib_hog_method(img_gray)
    haar_result = haar_cascade_method(img_gray)
    if hog_result is not None and haar_result is not None:
        x,y,w,h = hog_result
        x1,y1,w1,h1 = haar_result

        # draw rectangle
        cv2.rectangle(im_rd, (x,y), (x+w, y+h), (0,255,0), 2)   ## green
        cv2.rectangle(im_rd, (x1, y1), (x1+w1, y1+h1), (255,0,255), 4)  ## purple

        cv2.imshow("FaceDetect", im_rd)
        key = cv2. waitKey()
        if key == ord('q'):
            print("Quit")
            quit_opencv(cap)
