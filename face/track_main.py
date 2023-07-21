import cv2
import mediapipe as mp
import time
import track_model
cap=cv2.VideoCapture(0)

Ptime=0
Ctime=0
detector=track_model.facedetector()
while True:
    success,img =cap.read()
    img,bboxs=detector.findfaces(img) 
    print(bboxs)
    # lmList=detector.findposition(img)
    # if(len(lmList)!=0):
    #     print(lmList[4])
    Ctime =time.time()
    fps=1/(Ctime-Ptime)
    Ptime=Ctime

    cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3 )

    cv2.imshow("Image",img)
    cv2.waitKey(1)