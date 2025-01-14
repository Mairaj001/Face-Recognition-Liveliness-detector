import cv2
import os
import numpy as np
from tensorflow.keras.models import load_model

class AntiSpoofingMain:
    def __init__(self):
        # Load Face Detection Model
        root_dir = os.getcwd()
        face_cascade_path = os.path.join(root_dir, "Backend/AntiSpoofing/Models/CascadeModel/haarcascade_frontalface_default.xml")
        if not os.path.exists(face_cascade_path):
            raise FileNotFoundError(f"Face cascade file not found at {face_cascade_path}.")

        self.face_cascade = cv2.CascadeClassifier(face_cascade_path)

        # Load Anti-Spoofing Model
        model_path = os.path.join(root_dir, 'Backend/AntiSpoofing/Models/AntiSpoofIngModel/antispoofing_model.h5')
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Anti-spoofing model file not found at {model_path}.")

        try:
            self.model = load_model(model_path)
        except Exception as e:
            raise RuntimeError(f"Error loading the anti-spoofing model: {e}")

    def predict_spoof(self, face):
        try:
            resized_face = cv2.resize(face, (160, 160))
            resized_face = resized_face.astype("float32") / 255.0
            resized_face = np.expand_dims(resized_face, axis=0)

            # Predict real or spoof
            preds = self.model.predict(resized_face)[0]
            label = "spoof" if preds > 0.5 else "real"
            return label
        except Exception as face_error:
            print(f"Error processing face region: {face_error}")
            return "Error"
