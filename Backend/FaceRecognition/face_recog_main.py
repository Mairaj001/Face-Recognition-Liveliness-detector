import cv2
from .face_recog_script import SimpleFacerec


class FaceRecognitionMain:
    def __init__(self):
        self.sfr = SimpleFacerec()
        self.sfr.load_encoding_images("Backend/FaceRecognition/images/")  

    def detect_faces(self, frame):
        # Detect faces and names
        face_locations, face_names = self.sfr.detect_known_faces(frame)
        return face_locations, face_names
