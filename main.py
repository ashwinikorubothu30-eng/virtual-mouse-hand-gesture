import cv2
from hand_tracker import HandTracker
from mouse_controller import MouseController
from gesture_controller import GestureController
import pyautogui


camera = cv2.VideoCapture(0)

camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

tracker = HandTracker()
mouse = MouseController()
gesture = GestureController()


while True:

    success, frame = camera.read()

    if not success:
        break

    # Mirror the camera
    frame = cv2.flip(frame, 1)

    # Detect hand
    frame = tracker.findHands(frame)

    # Get landmarks
    landmarks = tracker.findPosition(frame)

    if landmarks:

        x = landmarks[8][1]
        y = landmarks[8][2]

        # Move mouse
        mouse.move(x, y)

        # Detect left click
        if gesture.detect_left_click(landmarks):
            pyautogui.click()
            print("LEFT CLICK")

        # Show index fingertip
        cv2.circle(
            frame,
            (x, y),
            12,
            (255, 0, 255),
            cv2.FILLED
        )

    cv2.imshow("Virtual Mouse", frame)

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


camera.release()
cv2.destroyAllWindows()