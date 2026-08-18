# 🖱️ Virtual Mouse Using Hand Gesture Recognition

A real-time computer vision-based virtual mouse that allows users to control the computer cursor using hand gestures captured through a webcam.

The project uses **Python, OpenCV, MediaPipe, and PyAutoGUI** to detect hand landmarks, recognize gestures, and translate them into mouse actions.

---

## ✨ Features

- Real-time hand tracking using MediaPipe
- 21-point hand landmark detection
- Cursor movement using the index finger
- Left-click using thumb + index finger pinch
- Right-click using index + middle finger gesture
- Drag and drop using a held pinch gesture
- Scrolling using open-palm movement
- Fist gesture for temporarily freezing cursor control
- Cursor smoothing for stable movement
- Gesture cooldowns to reduce accidental repeated clicks
- Real-time FPS monitoring
- Optimized frame processing for improved performance

---

## 🛠️ Technologies Used

- **Python 3.12**
- **OpenCV**
- **MediaPipe**
- **PyAutoGUI**
- **NumPy**
- **Matplotlib**

---

## 📁 Project Structure

```text
virtualmouse/
│
├── assets/
│
├── main.py
├── hand_tracker.py
├── mouse_controller.py
├── gesture_controller.py
├── utils.py
├── requirements.txt
├── README.md
└── .gitignore
