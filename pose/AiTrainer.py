import cv2
import mediapipe as mp
import time
import PoseDetectionModule
cap=cv2.VideoCapture(0)

Ptime=0
Ctime=0
detector=PoseDetectionModule.Posedectector()
while True:
    success,img =cap.read()
    img=detector.findPose(img,False) 
    lmList=detector.findPosition(img,False)
    
    if(len(lmList)!=0):
        detector.findAngle(img,12,14,16)
        detector.findAngle(img,11,13,15)
    Ctime =time.time()
    fps=1/(Ctime-Ptime)
    Ptime=Ctime

    cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3 )

    cv2.imshow("Image",img)
    cv2.waitKey(1)