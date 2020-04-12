from abc import ABC

import mtcnn
import cv2

class Face:

    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h


class FaceDetector(ABC):

    def __init__(self):
        pass

    def detect(self, img):
        pass


class CascadeClassifier(FaceDetector):

    def __init__(self):
        self.detector = cv2.CascadeClassifier(
            'haarcascade_frontalface_default.xml')

    def detect(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.detector.detectMultiScale(img, 1.1, 4)
        return [Face(*f) for f in faces]


class MTCNNDetector(FaceDetector):

    def __init__(self):
        self.detector = mtcnn.MTCNN()

    def detect(self, img):
        faces = self.detector.detect_faces(img)
        return [Face(*f['box']) for f in faces]