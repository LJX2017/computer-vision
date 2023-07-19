import cv2
import mediapipe as mp
import time
import Handtrack_module
cap=cv2.VideoCapture(0)

Ptime=0
Ctime=0
detector=Handtrack_module.handdetector()
while True:
    success,img =cap.read()
    img=detector.findHands(img) 
    lmList=detector.findposition(img)
    if(len(lmList)!=0):
        print(lmList[4])
    Ctime =time.time()
    fps=1/(Ctime-Ptime)
    Ptime=Ctime

    cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3 )

    cv2.imshow("Image",img)
    cv2.waitKey(1)