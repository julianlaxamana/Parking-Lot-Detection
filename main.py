import cv2
import torch

torch.hub.set_dir('./cache')
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', _verbose=False)
model.classes = [2]

cap = cv2.VideoCapture(0)

if __name__ == "__main__":
    while True:
        # Read a frame from the camera
        ret, frame = cap.read()
        if not ret:
            break

        # Prepare for image processing
        readimg = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 

        # Do some image processing
        result = model(readimg) 

        # Draw the bounding boxes
        result.render()
        img =  cv2.cvtColor(readimg, cv2.COLOR_RGB2BGR)
    
        cv2.rectangle(img, (100, 100), (200, 200), color=(255,0,0), thickness=2)

        # Display the resulting frame
        cv2.imshow('frame', img)
    
        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

