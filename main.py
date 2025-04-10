import cv2
import torch
import threading
import numpy as np
from flask import Flask, render_template, request, jsonify, Response

app = Flask(__name__)
car_count = 0

print("Imported Packages")

frame = np.empty(shape=(0, 0))
img = np.empty(shape=(0, 0))
bits = None

model = torch.hub.load('ultralytics/yolov5', 'yolov5n', _verbose=False)
model.classes = [2]
mutex = threading.Lock()

def processImg():
    global frame
    global img
    global car_count
    prevInside1 = False;
    while True:
         # Prepare for image processing
        try:
            readimg = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 

            # Do some image processing
            result = model(readimg) 

            # Draw the bounding boxes
            result.render()
            img =  cv2.cvtColor(readimg, cv2.COLOR_RGB2BGR)

            # Get the data in a pandas dataset
            pd_df = result.pandas()
            df = pd_df.xyxy[0].transpose()

            x1, y1 = 100, 100
            x2, y2 = 500, 500
            inside1 = False
            for col in df.columns:
                box = []
                for index, row in df.iterrows():
                    box.append(row[col])

                if x1 < box[0] and y1 < box[1] and x2 > box[2] and y2 > box[3]:
                    inside1 = True 
                    if inside1 and not prevInside1:
                        car_count += 1
                    prevInside1 = True

            if inside1:
                cv2.rectangle(img, (x1, y1), (x2, y2), color=(0,255,0), thickness=2)
            else:
                cv2.rectangle(img, (x1, y1), (x2, y2), color=(0,0,255), thickness=2)
                prevInside1 = False

            x1, y1 = 400, 100
            x2, y2 = 900, 500
            inside2 = False
            for col in df.columns:
                box = []
                for index, row in df.iterrows():
                    box.append(row[col])

                if x1 < box[0] and y1 < box[1] and x2 > box[2] and y2 > box[3]:
                    inside2 = True 
                    if inside2 and not prevInside2:
                        car_count -= 1
                    prevInside2 = True

            if inside2:
                cv2.rectangle(img, (x1, y1), (x2, y2), color=(0,255,0), thickness=2)
            else:
                cv2.rectangle(img, (x1, y1), (x2, y2), color=(0,0,255), thickness=2)
                prevInside2 = False
        except:
            continue

def test():
    global frame
    global img
    global bits
    cap = cv2.VideoCapture("http://192.168.8.161:81/stream")
    while True:
        try:
            ret, frame = cap.read()
        finally:
            continue

def gen_frames():
    global frame
    global bits
    cap = cv2.VideoCapture("http://10.0.0.51:81/stream")
    while True:
        # Read a frame from the camera
        try:
            ret, frame = cap.read()
            ret, buffer = cv2.imencode('.jpg', img)
            bits = buffer.tobytes()
            yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + bits + b'\r\n')
        except:
            yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n\r\n')

@app.route("/stream")
def stream():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace;boundary=frame')

@app.route("/")
def index():
    return render_template("index.html", car_count=car_count)

def updateCount():
    action = request.json.get("action")
    if action == "increment":
        car_count += 1
    elif action == "decrement":
        car_count = max(0, car_count - 1)
    

@app.route("/update")
def update():
    global car_count
    return jsonify({"car_count": car_count})

  


if __name__ == "__main__":
    t = threading.Thread(target=processImg)
    t.start()
    app.run(debug=True)
