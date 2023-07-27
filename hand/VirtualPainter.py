import cv2
import numpy as np
import os
import Handtrack_module
brushThickness=15
eraserThickness=30
xp,yp=0,0
folderPath ="Header"
myList=os.listdir(folderPath)
print(myList)
overlayList=[]
drawColor=(255,0,255)
for imPath in myList:
    image =cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)
header=overlayList[0]

cap=cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
detector=Handtrack_module.handdetector(detectionCon=0.1)
imgCanvas=np.zeros((720,1280,3),np.uint8)
while True:
    success,img=cap.read()
    img=cv2.flip(img,1)
    img[0:167,0:1258]=header
    img=detector.findHands(img,draw=False)
    lmList=detector.findposition(img,draw=False)
    if len(lmList)!=0:
        # print(lmList)
        _,x1,y1=lmList[8]
        __,x2,y2=lmList[12]
        fingers=detector.fingersUp()
        # print(fingers)
        if fingers[1] and fingers[2]:
            cv2.rectangle(img,(x1,y1-25),(x2,y2+25),(255,0,255),cv2.FILLED)
            print("Selection Mode")
            xp,yp=0,0
            if y1<167:
                if(0<x1<314):
                    drawColor=(0,0,255)
                if(314<x1<628):
                    drawColor=(0,255,0)
                if(628<x1<942):
                    drawColor=(255,0,0)
                if(942<x1<1258):
                    drawColor=(0,0,0)
            cv2.rectangle(img,(x1,y1-25),(x2,y2+25),drawColor,cv2.FILLED)

        if fingers[1] and fingers[2]==0:
            cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
            print("Drawing Mode")
            if xp!=0 and yp!=0:
                if(drawColor!=(0,0,0)):
                    cv2.line(img,(xp,yp),(x1,y1),drawColor,brushThickness)
                    cv2.line(imgCanvas,(xp,yp),(x1,y1),drawColor,brushThickness)
                else:
                    cv2.line(img,(xp,yp),(x1,y1),drawColor,eraserThickness)
                    cv2.line(imgCanvas,(xp,yp),(x1,y1),drawColor,eraserThickness)
            xp=x1
            yp=y1   
    img=cv2.addWeighted(img,0.5,imgCanvas,0.5,0)
    cv2.imshow("image",img)
    # cv2.imshow("hh",imgCanvas)
    cv2.waitKey(1)
