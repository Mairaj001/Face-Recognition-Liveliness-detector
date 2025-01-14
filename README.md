# Face Recognition and Liveliness Detector

## Author
**Mairaj Ahmed Khoso**

## Project Overview
This project is a **Face Recognition and Liveliness Detector** application. It combines:
- **Silent-Face-Recognition** Python library for face recognition.
- **Spoof and Anti-Spoof Models** for detecting liveliness and preventing spoofing attempts.

The system is designed to ensure secure face authentication by validating both the identity and the liveliness of the individual.

---

## Features
- **Face Recognition**: Accurate face matching using the Silent-Face-Recognition library.
- **Liveliness Detection**: Detects whether the face is real or a spoof using anti-spoofing models.
- **Secure Authentication**: Combines recognition and liveliness detection for enhanced security.

---

## Requirements
Ensure you have the following installed:
- Python 3.8 or above
- Libraries:
  - face_recognition
  - numpy
  - tensorflow
  - opencv-python
  

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Mairaj001/Face-Recognition-Liveliness-detector.git
   cd face-recognition-liveliness
   ```

2. **Set Up Virtual Environment**:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # On Windows
   source venv/bin/activate   # On macOS/Linux
   ```



4. **Add Pretrained Models**:
   - Download the Silent-Face-Recognition model.
   - Download the Spoof and Anti-Spoof models.
   - Place them in the designated `models/` folder.

---

## Usage

1. **Run the Application**:
   ```bash
   python app.py
   ```

2. **Face Recognition**:
   - The system will capture a face and match it using the Silent-Face-Recognition library.

3. **Liveliness Detection**:
   - The anti-spoofing model will validate whether the face is real or a spoof.



## Models
### Face Recognition
The Face_Recognition library provides a high-accuracy model for face recognition.

### Spoof and Anti-Spoof Model
This model is used to determine whether the detected face is live or a spoof attempt (e.g., photo or video).

---

## Contributing
Contributions are welcome! Feel free to fork this repository, make improvements, and create a pull request.

---

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

---

## Acknowledgments
Special thanks to the developers of the Silent-Face-Recognition library and the authors of the anti-spoofing models.

---

## Contact
For queries or feedback, reach out to **Mairaj Ahmed Khoso** at mairajahmed2k21@gmail.com.

