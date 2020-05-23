from flask import Flask, render_template, Response, jsonify
import time
import cv2
from detection import detection


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

        # keras models not thread-safe. Initalize the model here!
        # https://stackoverflow.com/questions/53391618/tensor-tensorpredictions-softmax0-shape-1000-dtype-float32-is-not-an
        
        #self..model = detection.CascadeClassifier()
        self.model = detection.VGG16Classifier()

    def __del__(self):
        self.video.release()        

    def get_frame(self):
        ret, image = self.video.read()
        image = cv2.flip(image, 1)
        image = self.model.process(image)

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