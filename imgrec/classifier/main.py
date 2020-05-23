import cv2
import time
import numpy as np

from tensorflow.keras import applications
from tensorflow.keras.applications.vgg16 import decode_predictions, preprocess_input

vggmodel = applications.VGG16(weights='imagenet', include_top=True)

font = cv2.FONT_HERSHEY_SIMPLEX
line_type = cv2.LINE_AA

def classify_image(image):
    # Red: OpenCV uses BGR instead of RGB!
    img = image.copy()
    img = cv2.resize(img, (224, 224), cv2.INTER_NEAREST)
    img = img.reshape(1, 224, 224, 3)
    output = vggmodel.predict(img)
    labels = decode_predictions(output)
    # [[(class_name, class_description, score), ...]]
    label, prob = labels[0][0][1], labels[0][0][2]
    return label, prob

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
        t0 = time.time()
        ret_val, image = cam.read()
        if mirror:
            image = cv2.flip(image, 1)    
        label, prob = classify_image(image)
        if label is not None:
            #print(label)
            t1 = time.time()
            duration = t1 - t0
            fps = 1 / duration 
            image = cv2.putText(image, f'{fps:.2f} FPS', (8,24), font, 1, (0, 0, 255), 2, line_type)
            image = cv2.putText(image, f'{prob:.2f}: {label}', (8,56), font, 1, (0, 0, 255), 2, line_type)

        cv2.imshow('my webcam', image)
        if cv2.waitKey(1) == 27:
            break # ESC to quit

    cv2.destroyAllWindows()

def main():
    show_webcam(mirror=True)


if __name__ == '__main__':
    main()