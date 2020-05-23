import cv2

class Face:

    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.box = (x, y, w, h)


class CascadeClassifier:

    def __init__(self):
        self.detector = cv2.CascadeClassifier(
            'detection/haarcascade_frontalface_default.xml')

    def detect(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.detector.detectMultiScale(img, 1.1, 4)
        return [Face(*f) for f in faces]