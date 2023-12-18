import os, time, imutils, cv2
from multiprocessing import Process
import numpy as np
from playsound import playsound

from addr import passs, hossst


# [rtsp @ 00000274c3d224c0] Nonmatching transport in server reply
os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"
# os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;0"
# os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;tcp"
# os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "dummy"
##face_d = cv2.CascadeClassifier('haarcascade\haarcascade_frontalface_default.xml')
first_frame = 0
w_size = 1200

mp3file = 'ping.mp3'
cou = 1
ogasdsa = 'n'


def chuongCua() :
    playsound(mp3file)
    print(cou, 'times')
    cou += 1


def doikichthuoc_xoanhieu(img):
    img = imutils.resize(img, width=w_size)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    return img, gray


def f_fmpeg():
    os.system('ffplay -rtsp_transport udp rtsp://admin:' + passs + '@' + hossst + ':554/onvif2')


def run():
    #capture = cv2.VideoCapture('demo.mp4')
    capture = cv2.VideoCapture('rtsp://admin:' + passs + '@' + hossst + ':554/onvif2', cv2.CAP_FFMPEG)
##    https://community.home-assistant.io/t/trying-to-get-ip-camera-to-work-yoosee/32842/21?page=2

    result, first_frame = capture.read()
    _, first_frame = doikichthuoc_xoanhieu(first_frame)
    take_time = time.time()
    main_emer = 0
    con_emer = time.time()

    while True:
        r, img = capture.read()
        img, gray = doikichthuoc_xoanhieu(img)

        frameDel = cv2.absdiff(first_frame, gray)
        thresh = cv2.threshold(frameDel, 30, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations = 2)

        cv2.imshow("W", frameDel)

        cnts,res = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in cnts:
            if cv2.contourArea(contour) < 10000 :
                continue
            if (time.time() - take_time > 3) :
                cv2.imwrite(str(time.time()) + ".jpg", img)
                take_time = time.time()
            if (time.time() - con_emer > 1) :
                main_emer = 0
            else :
                main_emer += time.time() - con_emer
            con_emer = time.time()
            if main_emer > 10 :
                first_frame = gray
            (x,y,w,h) = cv2.boundingRect(contour)
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0), 3)
        cv2.putText(img, str(main_emer), (200, 200), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 2)     
           
        cv2.imshow("key", img)
        if cv2.waitKey(1) == ord("q"):
            break

if __name__ == '__main__':
    pass
    os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"
    run()
##    p = Process(target=run)
##    p.start()
##    p.join()
