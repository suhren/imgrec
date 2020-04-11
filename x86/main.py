import cv2
import numpy as np
from mtcnn.mtcnn import MTCNN

# MTCNN detector for faces
detector = MTCNN()

def highlight_faces(image, faces):
    """
    Draw a bouding box around each face in the image

    Args:
        image (img): Image on which to draw the bounding boxes
        faces (array): The array containing the faces
    
    Returns:
        The image with the bounding boxes drawn
    """
    
    # Red: OpenCV uses BGR instead of RGB!
    color = (0, 0, 255)
    thickness = 2
    for face in faces:
        x, y, width, height = face['box']
        top_left = (x, y)
        bottom_right = (x + width, y + height)    
        image = cv2.rectangle(image, top_left, bottom_right, color, thickness) 
    return image

# https://gist.github.com/tedmiston/6060034
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
        faces = detector.detect_faces(image)
        image = highlight_faces(image, faces)
        cv2.imshow('my webcam', image)
        if cv2.waitKey(1) == 27:
            break # ESC to quit
        
    cv2.destroyAllWindows()

def main():
    show_webcam(mirror=True)


if __name__ == '__main__':
    main()