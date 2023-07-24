import cv2
import mediapipe as mp
import time
import math
import numpy as np
import Handtrack_module

from ctypes import cast,POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities,IAudioEndpointVolume

devices=AudioUtilities.GetSpeakers()
interface=devices.Activate(
    IAudioEndpointVolume._iid_,CLSCTX_ALL,None)
volume=cast(interface,POINTER(IAudioEndpointVolume))
volRange=volume.GetVolumeRange()
volBar=400
volPer=0
print(volRange)
volume.SetMasterVolumeLevel(0,None)
minVol=volRange[0]
maxVol=volRange[1]
cap=cv2.VideoCapture(0)

Ptime=0
Ctime=0
detector=Handtrack_module.handdetector()
while True:
    success,img =cap.read()
    img=detector.findHands(img) 
    lmList=detector.findposition(img,draw=False)
    if(len(lmList)!=0):
        # print(lmList[4],lmList[8])
        x1,y1=lmList[4][1],lmList[4][2]
        x2,y2=lmList[8][1],lmList[8][2]
        cx=(x1+x2)//2
        cy=(y1+y2)//2
        cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
        cv2.circle(img,(x2,y2),15,(255,0,255),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)
        cv2.circle(img,(cx,cy),15,(255,0,255),cv2.FILLED)
        length=math.hypot(x1-x2,y1-y2)
        # print(length) 
        vol=np.interp(length,[50,300],[minVol,maxVol])
        volBar=np.interp(length,[50,300],[400,150])
        volPer=np.interp(length,[50,300],[0,100])
        # print(vol)
        volume.SetMasterVolumeLevel(vol,None)
    cv2.rectangle(img,(50,150),(85,400),(0,255,0),3)
    cv2.rectangle(img,(50,int(volBar)),(85,400),(0,255,0),cv2.FILLED)
    cv2.putText(img,f'{int(volPer)}%',(40,450),cv2.FONT_HERSHEY_COMPLEX,1,(0,250,0),3)
    Ctime =time.time()
    fps=1/(Ctime-Ptime)
    Ptime=Ctime

    cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3 )

    cv2.imshow("Image",img)
    cv2.waitKey(1)