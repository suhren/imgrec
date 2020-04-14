from flask import Flask, render_template, Response, jsonify
import time
from detection import detection
import cv2

# MTCNN detector for faces
detector = detection.CascadeClassifier()

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
    
    for f in faces:
        top_left = (f.x, f.y)
        bottom_right = (f.x + f.w, f.y + f.h)    
        image = cv2.rectangle(image, top_left, bottom_right, color, thickness) 
    
    return image


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()        

    def get_frame(self):
        ret, image = self.video.read()

        faces = detector.detect(image)
        image = highlight_faces(image, faces)

        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port='5000')