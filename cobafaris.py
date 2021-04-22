# final_version dengan sensor suhu
import numpy as np
import cv2
import random
from smbus2 import SMBus
from mlx90614 import MLX90614

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
mouth_cascade = cv2.CascadeClassifier('haarcascade_mcs_mouth.xml')
upper_body = cv2.CascadeClassifier('haarcascade_upperbody.xml')

#sensor suhu
bus = SMBus(1)
sensor = MLX90614(bus, address=0x5A)

# set parameter video hitam putih
bw_threshold = 80

# pesan
font = cv2.FONT_HERSHEY_SIMPLEX
orgbaris1 = (30, 30)
orgbaris2 = (30,50)
orgbaris3 = (30,70)
orgbaris4= ( 30, 90)
wfontnoface = (0,0,0)
wfontwmask = (255, 255, 255)
wfontnomask = (0, 0, 255)
thickness = 2
font_scale = 0.5
maskerada = "Terima Kasih Telah Menggunakan Masker"
maskerno = "Silahkan Pakai Masker dulu! "
noface = "Wajah Tidak Ditemukan! "
jumlahfps = "Frames per second : "
suhubadan = "Suhu badan anda : "
pesanakhir1 = "Anda Dilarang Masuk! "
pesanakhir2 = "Silahkan Masuk! "


# membaca video
cap = cv2.VideoCapture(0)

while 1:
    # FPS COUNTER
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    #nilai suhu
    nilaisuhu = sensor.get_object_1()

    # membaca setiap frame
    ret, img = cap.read()
    img = cv2.flip(img,1)

    # konversi gambar ke grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Convert image in black and white
    (thresh, black_and_white) = cv2.threshold(gray, bw_threshold, 255, cv2.THRESH_BINARY)
    #cv2.imshow('black_and_white', black_and_white)

    # detect face
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    # Face prediction for black and white
    faces_bw = face_cascade.detectMultiScale(black_and_white, 1.1, 4)


    if(len(faces) == 0 and len(faces_bw) == 0 ):
        cv2.putText(img, noface , orgbaris1, font, font_scale, wfontnoface, thickness, cv2.LINE_AA)
        cv2.putText(img,  jumlahfps + format(fps), orgbaris2, font, font_scale, wfontnoface, thickness, cv2.LINE_AA)
        cv2.putText(img, suhubadan + str(nilaisuhu) , orgbaris3, font, font_scale, wfontnoface, thickness, cv2.LINE_AA)
        cv2.putText(img, pesanakhir1 , orgbaris4, font, font_scale, wfontnomask, thickness, cv2.LINE_AA)
    elif(len(faces) == 0 and len(faces_bw) == 1 and nilaisuhu >= 38):
        # It has been observed that for white mask covering mouth, with gray image face prediction is not happening
        cv2.putText(img, maskerada , orgbaris1, font, font_scale, wfontwmask, thickness, cv2.LINE_AA)
        cv2.putText(img, jumlahfps + format(fps), orgbaris2, font, font_scale, wfontwmask, thickness, cv2.LINE_AA)
        cv2.putText(img, suhubadan + str(nilaisuhu), orgbaris3, font, font_scale, wfontwmask, thickness, cv2.LINE_AA)
        cv2.putText(img, pesanakhir1 , orgbaris4, font, font_scale, wfontnomask, thickness, cv2.LINE_AA)
    elif(len(faces) == 0 and len(faces_bw) == 1 and nilaisuhu < 38 ):
        # It has been observed that for white mask covering mouth, with gray image face prediction is not happening
        cv2.putText(img, maskerada , orgbaris1, font, font_scale, wfontwmask, thickness, cv2.LINE_AA)
        cv2.putText(img, jumlahfps + format(fps), orgbaris2, font, font_scale, wfontwmask, thickness, cv2.LINE_AA)
        cv2.putText(img, suhubadan + str(nilaisuhu), orgbaris3, font, font_scale, wfontwmask, thickness, cv2.LINE_AA)
        cv2.putText(img, pesanakhir2 , orgbaris4, font, font_scale, wfontwmask, thickness, cv2.LINE_AA)
    else:
        # Draw rectangle on gace
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = img[y:y + h, x:x + w]
            # Detect lips counters
            mouth_rects = mouth_cascade.detectMultiScale(gray, 1.5, 5)
        # Face detected but Lips not detected which means person is wearing mask
        if(len(mouth_rects) == 0 and nilaisuhu >= 38):
            cv2.putText(img, maskerada , orgbaris1, font, font_scale, wfontwmask, thickness, cv2.LINE_AA)
            cv2.putText(img, jumlahfps + format(fps), orgbaris2, font, font_scale, wfontwmask, thickness, cv2.LINE_AA)
            cv2.putText(img, suhubadan + str(nilaisuhu), orgbaris3, font, font_scale, wfontwmask, thickness, cv2.LINE_AA)
            cv2.putText(img, pesanakhir1 , orgbaris4, font, font_scale, wfontnomask, thickness, cv2.LINE_AA)
        if(len(mouth_rects) == 0 and nilaisuhu < 38 ):
            cv2.putText(img, maskerada , orgbaris1, font, font_scale, wfontwmask, thickness, cv2.LINE_AA)
            cv2.putText(img, jumlahfps + format(fps), orgbaris2, font, font_scale, wfontwmask, thickness, cv2.LINE_AA)
            cv2.putText(img, suhubadan + str(nilaisuhu), orgbaris3, font, font_scale, wfontwmask, thickness, cv2.LINE_AA)
            cv2.putText(img, pesanakhir2 , orgbaris4, font, font_scale, wfontwmask, thickness, cv2.LINE_AA)
        else:
            for (mx, my, mw, mh) in mouth_rects:
                if(y < my < y + h):
                    # Face and Lips are detected but lips coordinates are within face cordinates which `means lips prediction is true and
                    # person is not waring mask
                    cv2.putText(img, maskerno , orgbaris1, font, font_scale, wfontnomask, thickness, cv2.LINE_AA)
                    cv2.putText(img, jumlahfps + format(fps), orgbaris2, font, font_scale, wfontnomask, thickness, cv2.LINE_AA)
                    cv2.putText(img, suhubadan + str(nilaisuhu), orgbaris3, font, font_scale, wfontnomask, thickness, cv2.LINE_AA)
                    cv2.putText(img, pesanakhir1 , orgbaris4, font, font_scale, wfontnomask, thickness, cv2.LINE_AA)
                    cv2.rectangle(img, (mx, my), (mx + mh, my + mw), (255, 0, 0), 3)
                    break
                    
    


    # Show frame with results
    cv2.imshow('Mask Detection', img)
    k = cv2.waitKey(30) & 0xff
    if k == ord('q'):
        bus.close()
        break

# Release video
cap.release()
cv2.destroyAllWindows()