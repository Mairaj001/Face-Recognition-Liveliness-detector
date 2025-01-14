import sys
import sqlite3
import cv2
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog, QFileDialog
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from backend.main_backend import FaceRecognitionMain, AntiSpoofingMain

DATABASE_PATH = "Database/users.db"
IMAGES_PATH = "backend/FaceRecognition/images"

class MainApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.loader = QUiLoader()

        self.main_window = self.loader.load("Frontend/main.ui")
        self.register_window = self.loader.load("Frontend/register.ui")
        self.login_window = self.loader.load("Frontend/login.ui")

        self.main_window.btn_register.clicked.connect(self.open_register_window)
        self.main_window.btn_login.clicked.connect(self.open_login_window)

        self.register_window.btn_capture.clicked.connect(self.capture_image)
        self.register_window.btn_submit.clicked.connect(self.register_user)

        self.login_window.btn_login.clicked.connect(self.perform_login)

        self.db_init()

    def db_init(self):
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            image_path TEXT NOT NULL
        )
        """)
        conn.commit()
        conn.close()

    def open_register_window(self):
        self.register_window.show()

    def open_login_window(self):
        self.login_window.show()

    def capture_image(self):
        name = self.register_window.line_name.text()
        email = self.register_window.line_email.text()

        if not name or not email:
            QMessageBox.warning(self.register_window, "Error", "Name and Email are required.")
            return

        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            QMessageBox.critical(self.register_window, "Error", "Camera not available.")
            return

        QMessageBox.information(self.register_window, "Capture", "Press 'C' to capture and 'Q' to quit.")
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            cv2.imshow("Capture Image", frame)
            key = cv2.waitKey(1)
            if key == ord('c'):
                image_path = f"{IMAGES_PATH}/{name}.png"
                cv2.imwrite(image_path, frame)
                QMessageBox.information(self.register_window, "Success", f"Image saved at {image_path}.")
                self.register_window.image_path = image_path
                break
            elif key == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

    def register_user(self):
        name = self.register_window.line_name.text()
        email = self.register_window.line_email.text()
        image_path = getattr(self.register_window, "image_path", None)

        if not name or not email or not image_path:
            QMessageBox.warning(self.register_window, "Error", "All fields are required.")
            return

        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (name, email, image_path) VALUES (?, ?, ?)", (name, email, image_path))
            conn.commit()
            QMessageBox.information(self.register_window, "Success", "User registered successfully.")
        except sqlite3.IntegrityError:
            QMessageBox.warning(self.register_window, "Error", "User already exists.")
        finally:
            conn.close()

    def perform_login(self):
        face_recog = FaceRecognitionMain()
        anti_spoof = AntiSpoofingMain()

        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            QMessageBox.critical(self.login_window, "Error", "Camera not available.")
            return

        QMessageBox.information(self.login_window, "Login", "Press 'Q' to quit.")
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            face_locations, face_names = face_recog.detect_faces(frame)
            for face_loc, name in zip(face_locations, face_names):
                y1, x2, y2, x1 = face_loc
                face = frame[max(0, y1 - 5):y2 + 5, max(0, x1 - 5):x2 + 5]
                label = anti_spoof.predict_spoof(face)
                if label != "spoof":
                    conn = sqlite3.connect(DATABASE_PATH)
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM users WHERE name = ?", (name,))
                    user = cursor.fetchone()
                    conn.close()
                    if user:
                        QMessageBox.information(self.login_window, "Login", f"Welcome back, {name}!")
                        cap.release()
                        cv2.destroyAllWindows()
                        return
                    else:
                        QMessageBox.warning(self.login_window, "Error", "User not found.")
            cv2.imshow("Login", frame)
            key = cv2.waitKey(1)
            if key == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

    def run(self):
        self.main_window.show()
        sys.exit(self.app.exec())

if __name__ == "__main__":
    app = MainApp()
    app.run()
