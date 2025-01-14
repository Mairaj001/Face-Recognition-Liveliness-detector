import cv2
from tensorflow.keras.preprocessing.image import img_to_array
import os
import numpy as np
from tensorflow.keras.models import load_model

root_dir = os.getcwd()
print(root_dir)


# Load Face Detection Model
face_cascade_path = os.path.join(root_dir, "Models/CascadeModel/haarcascade_frontalface_default.xml")
if not os.path.exists(face_cascade_path):
    print(f"Error: Face cascade file not found at {face_cascade_path}.")
    exit(1)

face_cascade = cv2.CascadeClassifier(face_cascade_path)

# Load Anti-Spoofing Model
model_path = os.path.join(root_dir, 'Models/AntiSpoofIngModel/antispoofing_model.h5')
if not os.path.exists(model_path):
    print(f"Error: Anti-spoofing model file not found at {model_path}.")
    exit(1)

try:
    model = load_model(model_path)
    print("Anti-Spoofing model loaded successfully test.")
except Exception as e:
    print(f"Error loading the anti-spoofing model: {e}")
    exit(1)

# Start Video Capture
video = cv2.VideoCapture(0)
if not video.isOpened():
    print("Error: Could not open video capture.")
    exit(1)

try:
    print("Press 'q' to quit.")
    while True:
        ret, frame = video.read()
        if not ret:
            print("Failed to capture frame. Exiting...")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            face = frame[max(0, y-5):y+h+5, max(0, x-5):x+w+5]
            try:
                resized_face = cv2.resize(face, (160, 160))
                resized_face = resized_face.astype("float32") / 255.0
                resized_face = np.expand_dims(resized_face, axis=0)

                # Predict real or spoof
                preds = model.predict(resized_face)[0]
                label = "spoof" if preds > 0.5 else "real"
                color = (0, 0, 255) if label == "spoof" else (0, 255, 0)

                cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            except Exception as face_error:
                print(f"Error processing face region: {face_error}")

        # Display the frame
        cv2.imshow('Frame', frame)
        key = cv2.waitKey(1)
        if key == ord('q'):  # Press 'q' to quit
            break
except KeyboardInterrupt:
    print("\nVideo capture interrupted by user.")
finally:
    video.release()
    cv2.destroyAllWindows()
    print("Video capture ended.")
