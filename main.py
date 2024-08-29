import cv2
import pandas as pd
from ultralytics import YOLO
from tracker import Tracker
import mysql.connector
from datetime import datetime

# Load YOLO model
model = YOLO('yolov8s.pt')

# Read class list
with open("coco.txt", "r") as f:
    class_list = f.read().split("\n")

# Initialize video capture
cap = cv2.VideoCapture('p3.mp4')

# Get video frame rate
fps = cap.get(cv2.CAP_PROP_FPS)

# Calculate the interval for processing frames
frame_interval = int(fps)  # process one frame per second

# Initialize Tracker
tracker = Tracker()

# Load age and gender models
age_net = cv2.dnn.readNetFromCaffe('age_deploy.prototxt', 'age_net.caffemodel')
gender_net = cv2.dnn.readNetFromCaffe('gender_deploy.prototxt', 'gender_net.caffemodel')

# Mean values for age and gender models
MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)

# Age and gender lists
AGE_LIST = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
GENDER_LIST = ['Male', 'Female']

# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="iitbbsr"
)
cursor = db.cursor()

# Clear the table at the start
#cursor.execute("DELETE FROM detections")
#db.commit()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS detections (
    camera_id INT,
    frame INT,
    center_x INT,
    center_y INT,
    width INT,
    height INT,
    class VARCHAR(10),
    age VARCHAR(10),
    gender VARCHAR(10)
)
""")

# Initialize frame count
frame_count = 0

# Initialize the frame save count
save_frame_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    orgframe = frame
    if not ret:
        break

    # Process every nth frame based on the frame interval
    if frame_count % frame_interval == 0:
        save_frame_count += 1  # Increment the save frame count
        frame = cv2.resize(frame, (1020, 500))

        # Perform YOLO detection
        results = model.predict(frame)
        detections = results[0].boxes.data
        px = pd.DataFrame(detections).astype("float")

        # List to store detected persons
        person_bboxes = []
        for index, row in px.iterrows():
            x1, y1, x2, y2 = int(row[0]), int(row[1]), int(row[2]), int(row[3])
            class_id = int(row[5])
            class_name = class_list[class_id]
            if 'person' in class_name:
                person_bboxes.append([x1, y1, x2, y2])

        # Update tracker with current frame's detections
        bbox_id = tracker.update(person_bboxes)

        for bbox in bbox_id:
            x3, y3, x4, y4, id = bbox

            # Calculate center coordinates, width, and height of the bounding box
            center_x = (x3 + x4) // 2
            center_y = (y3 + y4) // 2
            w = x4 - x3
            h = y4 - y3

            # Extract the face region
            face = frame[y3:y4, x3:x4]

            # Prepare the face for age and gender detection
            blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)

            # Predict gender
            gender_net.setInput(blob)
            gender_preds = gender_net.forward()
            gender = GENDER_LIST[gender_preds[0].argmax()]

            # Predict age
            age_net.setInput(blob)
            age_preds = age_net.forward()
            age = AGE_LIST[age_preds[0].argmax()]

            # Draw bounding boxes and IDs on the frame
            cv2.rectangle(frame, (x3, y3), (x4, y4), (0, 255, 0), 2)  # Green bounding box with thickness 2
            cv2.putText(frame, f"ID: {id}", (x3, y3 - 35), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1, cv2.LINE_AA)  # Yellow text
            cv2.putText(frame, f"Age: {age}", (x3, y3 - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 1, cv2.LINE_AA)  # Magenta text
            cv2.putText(frame, f"Gender: {gender}", (x3, y3 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1, cv2.LINE_AA)  # Cyan text

            # Insert data into the database
            cursor.execute("INSERT INTO detections (frame, center_x, center_y, width, height, class, age, gender) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                           (save_frame_count, center_x, center_y, w, h, 'person', age, gender))
            db.commit()

        # Display the frame
        cv2.imshow("RGB", frame)
        folder_name = "camera-1/"
        file_name = folder_name + str(save_frame_count) + ".jpeg"
        cv2.imwrite(file_name, orgframe)

        if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
            break

    # Increment frame count
    frame_count += 1

# Release video capture and close all windows
cap.release()
cv2.destroyAllWindows()

# Close database connection
db.close()