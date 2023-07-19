import cv2
import time
import mediapipe as mp
video = cv2.VideoCapture(0)
mpPose = mp.solutions.pose
pose = mpPose.Pose()

class Posedectector:
    def __init__(self,
               static_image_mode=False,
               model_complexity=1,
               smooth_landmarks=True,
               enable_segmentation=False,
               smooth_segmentation=True,
               min_detection_confidence=0.5,
               min_tracking_confidence=0.5):
        self.mpPose = mp.solutions.pose
        self.pose = mpPose.Pose(
               static_image_mode,
               model_complexity,
               smooth_landmarks,
               enable_segmentation,
               smooth_segmentation,
               min_detection_confidence,
               min_tracking_confidence)
        self.mpDraw = mp.solutions.drawing_utils
    def findPose(self,img,draw=True):
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results = pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img,self.results.pose_landmarks,self.mpPose.POSE_CONNECTIONS)
        return img
    def findPosition(self,img, draw = True):
        lmlist = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h,w,c = img.shape
                cx = int(lm.x*w)
                cy = int(lm.y*h)
                lmlist.append([id,cx,cy])
                if draw:
                    cv2.circle(img,(cx,cy),15,(255,12,200),cv2.FILLED)
        return lmlist
def main():
    pTime=0
    cTime=0
    video = cv2.VideoCapture(0)
    detector = Posedectector()
    while True:
        success, img = video.read()
        img = detector.findPose(img)
        lmlist = detector.findPosition(img)
        cTime = time.time()
        
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv2.imshow("Image", img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()