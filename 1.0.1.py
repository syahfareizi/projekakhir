#masker tanpa suhu video
import numpy as np
import cv2
import random
import time
#from smbus2 import SMBus
#from mlx90614 import MLX90614

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
mouth_cascade = cv2.CascadeClassifier('haarcascade_mcs_nose.xml')
mask_cascade = cv2.CascadeClassifier ('cascade.xml')

#sensor suhu
#bus = SMBus(1)
#sensor = MLX90614(bus, address=0x5A)

# set parameter video hitam putih
bw_threshold = 80

# pesan
font = cv2.FONT_HERSHEY_SIMPLEX
orgbaris1 = (30, 30)
orgbaris2 = (30,50)
orgbaris3 = (30,70)
orgbaris4= ( 30, 90)
orgbaris5= ( 30, 110)
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

#daftar fungsi 

def ambilgambar():
    cond, imge =cap.read()
    out = cv2.imwrite("filename.jpg",imge)
    
def nofaces():
    cv2.putText(img, noface , orgbaris1, font, font_scale, wfontnoface, thickness, cv2.LINE_AA)
    #cv2.putText(img, suhubadan + str(nilaisuhu) , orgbaris3, font, font_scale, wfontnoface, thickness, cv2.LINE_AA)
    #cv2.putText(img, pesanakhir1 , orgbaris4, font, font_scale, wfontnomask, thickness, cv2.LINE_AA)

def maskernosuhu():
    cv2.putText(img, maskerada , orgbaris1, font, font_scale, wfontwmask, thickness, cv2.LINE_AA)
    #cv2.putText(img, suhubadan + str(nilaisuhu), orgbaris3, font, font_scale, wfontnowmask, thickness, cv2.LINE_AA)
    #cv2.putText(img, pesanakhir1 , orgbaris4, font, font_scale, wfontnomask, thickness, cv2.LINE_AA)

def maskersuhu():
    cv2.putText(img, maskerada , orgbaris1, font, font_scale, wfontwmask, thickness, cv2.LINE_AA)
    #cv2.putText(img, suhubadan + str(nilaisuhu), orgbaris3, font, font_scale, wfontwmask, thickness, cv2.LINE_AA)
    #cv2.putText(img, pesanakhir2 , orgbaris4, font, font_scale, wfontnomask, thickness, cv2.LINE_AA)
    #time.sleep(5)

def nomaskernosuhu():
    cv2.putText(img, maskerno , orgbaris1, font, font_scale, wfontnomask, thickness, cv2.LINE_AA)
    #cv2.putText(img, suhubadan + str(nilaisuhu), orgbaris3, font, font_scale, wfontnomask, thickness, cv2.LINE_AA)
    #cv2.putText(img, pesanakhir1 , orgbaris4, font, font_scale, wfontnomask, thickness, cv2.LINE_AA)
    
# membaca video
cap = cv2.VideoCapture(1)

# fps
waktusebelum = 0
waktusesudah = 0
    
while 1:    
    #nilai suhu
    #nilaisuhu = sensor.get_object_1()
    
    #ambilgambar
    #ambilgambar()
    
    #baca gambar
    img = cv2.imread('filename.jpg')

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

    if(len(faces) == 0 ):
        nofaces ()
    else:
        # Draw rectangle on gace
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = img[y:y + h, x:x + w]
            # Detect lips counters
            mouth_rects = mouth_cascade.detectMultiScale(gray, 1.5, 5)
            adamasker = mask_cascade.detectMultiScale(gray, 1.1, 4 )
            # Face detected but Lips not detected which means person is wearing mask
            if(len(mouth_rects) == 0 and len(adamasker)==1 ):
                for (kx, ky, kw, kh) in adamasker :
                    cv2.rectangle(img, (kx, ky), (kx + kh, ky + kw), (255, 0, 255), 3)
                    maskersuhu()
            elif(len(mouth_rects) == 0 and len(adamasker)==0):
                nomaskernosuhu()
            elif(len(mouth_rects) == 1 and len(adamasker)== 1):
                for (mx, my, mw, mh) in mouth_rects:
                    cv2.rectangle(img, (mx, my), (mx + mh, my + mw), (255, 0, 0), 3)
                    nomaskernosuhu()
                for (kx, ky, kw, kh) in adamasker :
                    cv2.rectangle(img, (kx, ky), (kx + kh, ky + kw), (255, 0, 255), 3)
            else:
                for (mx, my, mw, mh) in mouth_rects:
                    cv2.rectangle(img, (mx, my), (mx + mh, my + mw), (255, 0, 0), 3)
                    nomaskernosuhu()
                    break
    
    waktusesudah = time.time()
    
    fps = 1/(waktusesudah-waktusebelum)
    waktusebelum = waktusesudah
  
    # converting the fps into integer
    fps = int(fps)
  
    # converting the fps to string so that we can display it on frame
    # by using putText function
    fps = str(fps)
    cv2.putText(img,  jumlahfps + format(fps), orgbaris2, font, font_scale, wfontnoface, thickness, cv2.LINE_AA)
                        
    # Show frame with results
    cv2.imshow('Mask Detection', img)
    k = cv2.waitKey(30) & 0xff
    if k == ord('q'):
        #bus.close()
        break

# Release video
cap.release()
cv2.destroyAllWindows()