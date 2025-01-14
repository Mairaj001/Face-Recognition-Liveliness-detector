import os
import sys
import cv2


root_dir = os.getcwd()
print(root_dir)


face_recog_venv_path = os.path.join(os.getcwd(), "FaceRecognition", "venv", "Lib", "site-packages")
if os.path.exists(face_recog_venv_path):
    sys.path.append(face_recog_venv_path)
else:
    print(f"Error: FaceRecognition virtual environment not found at {face_recog_venv_path}. Ensure it is set up correctly.")
    sys.exit(1)


anti_spoof_venv_path = os.path.join(os.getcwd(), "AntiSpoofing", "venv_py3.11", "Lib", "site-packages")
if os.path.exists(anti_spoof_venv_path):
    sys.path.append(anti_spoof_venv_path)
else:
    print(f"Error: AntiSpoofing virtual environment not found at {anti_spoof_venv_path}. Ensure it is set up correctly.")
    sys.exit(1)

try:
    from FaceRecognition.face_recog_main import FaceRecognitionMain
except ModuleNotFoundError as e:
    print(f"Error importing FaceRecognition module: {e}")
    sys.exit(1)

try:
    from AntiSpoofing.Anit_spoof_main import AntiSpoofingMain
except ModuleNotFoundError as e:
    print(f"Error importing AntiSpoofing module: {e}")
    sys.exit(1)



def main():
    """
    Main function to perform real-time face recognition and anti-spoofing detection.
    """
    
    try:
        face_recog = FaceRecognitionMain()
        anti_spoof = AntiSpoofingMain()
    except Exception as e:
        print(f"Error initializing modules: {e}")
        return

    # Start Video Capture
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open video capture.")
        return

    print("Press 'q' to quit.")
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to capture frame. Exiting...")
                break

           
            try:
                face_locations, face_names = face_recog.detect_faces(frame)
                print(face_locations,face_names)
            except Exception as e:
                print(f"Error during face recognition: {e}")
                face_locations, face_names = [], []

            for face_loc, name in zip(face_locations, face_names):
                y1, x2, y2, x1 = face_loc
                face = frame[max(0, y1-5):y2+5, max(0, x1-5):x2+5]

                
                try:
                    label = anti_spoof.predict_spoof(face)
                except Exception as e:
                    print(f"Error during anti-spoofing prediction: {e}")
                    label = "unknown"

                
                color = (0, 0, 255) if label == "spoof" else (0, 255, 0)

                
                cv2.putText(frame, f"{name} ({label})", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

            
            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1)
            if key == ord('q'): 
                break

    except KeyboardInterrupt:
        print("\nVideo capture interrupted by user.")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("Video capture ended.")

if __name__ == "__main__":
    main()
