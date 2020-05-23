import cv2
import numpy as np

from detection import detection

#model = detection.CascadeClassifier()
model = detection.VGG16Classifier()

def show_webcam(mirror=False):
    """
    Shows the webcam feed in a windows with detected faces.
    Press ESC to close this window.

    Args:
        mirror (boolean): Wether or not to flip the image horizontally
    """
    
    cam = cv2.VideoCapture(0)
    while True:
        ret_val, image = cam.read()
        if mirror:
            image = cv2.flip(image, 1)

        image = model.process(image)

        cv2.imshow('my webcam', image)
        if cv2.waitKey(1) == 27:
            break # ESC to quit

    cv2.destroyAllWindows()

def main():
    show_webcam(mirror=True)


if __name__ == '__main__':
    main()