import cv2
import torch

torch.hub.set_dir('./cache')
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', _verbose=False)
model.classes = [2]

cap = cv2.VideoCapture(0)

if __name__ == "__main__":
    count = 0
    prevInside = False;
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

        # Get the data in a pandas dataset
        pd_df = result.pandas()
        df = pd_df.xyxy[0].transpose()

        x1, y1 = 100, 100
        x2, y2 = 200, 200
        inside = False
        for col in df.columns:
            box = []
            for index, row in df.iterrows():
                box.append(row[col])

            if x1 < box[0] and y1 < box[1] and x2 > box[2] and y2 > box[3]:
                inside = True 
                if inside and not prevInside:
                    count += 1
                prevInside = True

        if inside:
            cv2.rectangle(img, (x1, y1), (x2, y2), color=(0,255,0), thickness=2)
        else:
            cv2.rectangle(img, (x1, y1), (x2, y2), color=(0,0,255), thickness=2)
            prevInside = False

        # Text properties
        text = "Count: " + str(count)
        font = cv2.FONT_HERSHEY_SIMPLEX
        position = (10, 450) # Bottom-left corner of the text
        font_scale = 1
        color = (255, 255, 255) # White color
        thickness = 2
        line_type = cv2.LINE_AA

        # Write the text on the image
        cv2.putText(img, text, position, font, font_scale, color, thickness, line_type)

        # Display the resulting frame
        cv2.imshow('frame', img)
    
        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

