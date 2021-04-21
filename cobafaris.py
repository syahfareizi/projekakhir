import numpy as np
import cv2
import random

# multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
mouth_cascade = cv2.CascadeClassifier('haarcascade_mcs_mouth.xml')
upper_body = cv2.CascadeClassifier('haarcascade_upperbody.xml')
nose_cascade = cv2.CascadeClassifier('haarcascade_mcs_nose.xml')
mask_cascade = cv2.CascadeClassifier('cascade4.xml')



# Adjust threshold value in range 80 to 105 based on your light.
bw_threshold = 100

# User message
font = cv2.FONT_HERSHEY_SIMPLEX
org = (30,  30)
weared_mask_font_color = (255, 255, 255)
not_weared_mask_font_color = (0, 0, 255)
thickness = 2
font_scale = 0.5
weared_mask = "Terima Kasih Telah Menggunakan Masker"
not_weared_mask = "Anda Dilarang Masuk! Silahkan Pakai Masker dulu! "

# Read video
cap = cv2.VideoCapture(1)

while 1:
    # Get individual frame
    cond, img = cap.read()
    #img = cv2.flip(img,0)

    # Convert Image into gray
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Convert image in black and white
    (thresh, black_and_white) = cv2.threshold(gray, bw_threshold, 255, cv2.THRESH_BINARY)
    cv2.imshow('black_and_white', gray)

    # detect face
    faces = face_cascade.detectMultiScale(gray, 1.3, 2)
    # Face prediction for black and white
    faces_bw = face_cascade.detectMultiScale(black_and_white,1.3, 5)
    # Detect lips counters
    nose_rects = nose_cascade.detectMultiScale(gray, 1.3, 4)
    eyes = eye_cascade.detectMultiScale(gray, 1.3,4)


    if(len(faces) == 0 and len(eyes) == 0 and len(nose_rects) == 0):
        cv2.putText(img, "No face found...", org, font, font_scale, weared_mask_font_color, thickness, cv2.LINE_AA)
    elif(len(faces) == 1 and len(nose_rects) == 1 and len(eyes) == 1 ):
        cv2.putText(img, not_weared_mask, org, font, font_scale, not_weared_mask_font_color, thickness, cv2.LINE_AA)
    elif(len(eyes) == 1 and len(faces) == 1 and len(nose_rects) == 0 ):
        cv2.putText(img, weared_mask, org, font, font_scale, weared_mask_font_color, thickness, cv2.LINE_AA)
    else:
        # Draw rectangle on gace
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 5)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = img[y:y + h, x:x + w]
        for (x, y, w, h) in eyes:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 5)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = img[y:y + h, x:x + w]
        for (x, y, w, h) in nose_rects:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 5)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = img[y:y + h, x:x + w]
        

    # Show frame with results
    cv2.imshow('Mask Detection', img)
    k = cv2.waitKey(30) & 0xff
    if k == ord('q'):
        break

# Release video
cap.release()
cv2.destroyAllWindows()