import cv2
import mediapipe as mp
import time
import Handtrack_module
cap=cv2.VideoCapture(0)

Ptime=0
Ctime=0
detector=Handtrack_module.handdetector()
tipIds=[4,8,12,16,20]
while True:
    success,img =cap.read()
    img=detector.findHands(img) 
    lmList=detector.findposition(img,draw=False)
    if(len(lmList)!=0):
        fingers=[]
        if((lmList[4][1]>lmList[3][1])^(lmList[12][1]>lmList[8][1])):
            fingers.append(1)
        else:
            fingers.append(0)
        for id in range(1,5):
            if(lmList[tipIds[id]][2]<lmList[tipIds[id]-2][2]):
                fingers.append(1)
            else:
                fingers.append(0)
        print(fingers)
        totalFingers=fingers.count(1)
        # print(totalFingers)
        cv2.putText(img,str(totalFingers),(45,375),cv2.FONT_HERSHEY_PLAIN,10,(255,0,0),25)
    Ctime =time.time()
    fps=1/(Ctime-Ptime)
    Ptime=Ctime

    cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3 )

    cv2.imshow("Image",img)
    cv2.waitKey(1)