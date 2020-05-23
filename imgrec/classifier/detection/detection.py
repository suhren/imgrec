import cv2
import time
from tensorflow.keras import applications
from tensorflow.keras.applications.vgg16 import decode_predictions, preprocess_input


class Face:

    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.box = (x, y, w, h)


class VGG16Classifier:

    def __init__(self):
        self.model = applications.VGG16(weights='imagenet', include_top=True)
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.line_type = cv2.LINE_AA
        self.color = (0, 0, 255)
        self.thickness = 2
        self.font_scale = 1

    
    def classify(self, image):
        img = image.copy()
        img = cv2.resize(img, (224, 224), cv2.INTER_NEAREST)
        img = img.reshape(1, 224, 224, 3)
        output = self.model.predict(img)
        labels = decode_predictions(output)
        # [[(class_name, class_description, score), ...]]
        label, prob = labels[0][0][1], labels[0][0][2]
        return label, prob
    
    def process(self, image):
        try:
            t0 = time.time()
            label, prob = self.classify(image)
            if label is not None:
                t1 = time.time()
                duration = t1 - t0
                fps = 1 / duration 
                image = cv2.putText(image, f'{fps:.2f} FPS', (8,24), self.font, self.font_scale, self.color, self.thickness, self.line_type)
                image = cv2.putText(image, f'{prob:.2f}: {label}', (8,56), self.font, self.font_scale, self.color, self.thickness, self.line_type)
            return image
        except Exception as e:
            print(str(e))
            return image


class CascadeClassifier:

    def __init__(self):
        self.model = cv2.CascadeClassifier(
            'detection/haarcascade_frontalface_default.xml')

        self.color = (0, 0, 255)
        self.thickness = 2

    def highlight_faces(self, image, faces):
        """
        Draw a bouding box around each face in the image

        Args:
            image (img): Image on which to draw the bounding boxes
            faces (array): The array containing the faces
        
        Returns:
            The image with the bounding boxes drawn
        """
        for f in faces:
            top_left = (f.x, f.y)
            bottom_right = (f.x + f.w, f.y + f.h)    
            image = cv2.rectangle(image, top_left, bottom_right, self.color, self.thickness) 
        
        return image

    def process(self, image):
        grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.model.detectMultiScale(grayscale, 1.1, 4)
        faces = [Face(*f) for f in faces]
        return self.highlight_faces(image, faces)

