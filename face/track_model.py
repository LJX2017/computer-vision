import cv2
import mediapipe as mp
import time

class facedetector():
    def __init__(self,minDetectionCon=0.5):
        self.minDetectionCon=minDetectionCon

        self.mpFaceDetection=mp.solutions.face_detection
        self.mpDraw = mp.solutions.drawing_utils
        self.faceDetection=self.mpFaceDetection.FaceDetection(self.minDetectionCon)
    
    def findfaces(self,img,draw=True): 
        imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results=self.faceDetection.process(imgRGB)
        # print(results.multi_face_landmarks)
        bboxs=[]
        if self.results.detections:
            for id,detection in enumerate(self.results.detections):
                bboxC=detection.location_data.relative_bounding_box
                ih,iw,ic=img.shape
                bbox=int(bboxC.xmin*iw),int(bboxC.ymin*ih),int(bboxC.width*iw),int(bboxC.height*ih)
                bboxs.append([id,bbox,detection.score])
                cv2.rectangle(img,bbox,(255,0,255),2)
                cv2.putText(img,f'{int(detection.score[0]*100)}%',(bbox[0],bbox[1]-20),cv2.FONT_HERSHEY_PLAIN,2,(255,0,255),2)
                # if(draw==True):
                    # self.mpDraw.draw_landmarks(img,faceLms,self.mpfaces.face_CONNECTIONS)
        return img,bboxs
    # def findposition(self,img,faceNo=0,draw=True):
    #     lmList= []
    #     if self.results.multi_face_landmarks:
    #         myface=self.results.multi_face_landmarks[faceNo]
    #         for id,lm in enumerate(myface.landmark):
    #             # print(id,lm)
    #             h,w,c=img.shape
    #             cx,cy=int(lm.x*w),int(lm.y*h)
    #             # print(id,cx,cy)
    #             lmList.append([id,cx,cy])
    #             if draw:
    #                 cv2.circle(img,(cx,cy),15,(255,0,255),cv2.FILLED)
    #     return lmList
def main():
    
    cap=cv2.VideoCapture(0)

    Ptime=0
    Ctime=0
    detector=facedetector()
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
     

if __name__ == "__main__":
    main()