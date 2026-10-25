import cv2 
import numpy as np
import pygame as game

class ImageTracker:
    def __init__(self, src=0, width=640, height=480):
        self.cap = cv2.VideoCapture(src)
        self.cap.set(CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(CAP_PROP_FRAME_HEIGHT, height)
        self.lower_black = np.array([0, 0, 0])
        self.upper_black = np.array([180, 255, 70])
        self.kernel = np.ones((5,5), np.uint8)

    def frameProcess(self, targetWidth, targetHeight):
        ret, frame = self.cap.read()
        if not ret:
            return None, None

        frame = cv2.flip(frame,1)
        frameRGB = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        frameResized = cv2.resize(frameRGB,(targetWidth, targetHeight))

        frameSurface = game.surfarray.make_surface(np.rot90(frameResized))
        webcamSurface = game.transform.flip(frameSurface,True,False)

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(frame,self.lower_black,self.upper_black)
        mask = cv2.erode(frame,kernel=self.kernel,iterations=1)
        mask = cv2.dilate(frame,kernel=self.kernel,iterations=2)

        contour,_ = cv2.findContours(
            mask,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
        )

        detectedXratio = None
        if contour :
            largestContour = max(contour, key=cv2.contourArea)
            if cv2.contourArea(largestContour) > 800:
                m = cv2.moments(largestContour)
                if m["m00"] != 0:
                    cx = int(m["m10"]/m["m00"])
                    detectedXratio = cx / frame.shape[1]

        return webcamSurface, frameSurface

    def release(self):
        self.cap.release()



