import cv2
import pyautogui
import time

from hand_tracker import HandTracker
from mouse_controller import MouseController
from gesture_controller import GestureController


# --------------------------------------------------
# Camera
# --------------------------------------------------

camera = cv2.VideoCapture(0)

camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


# --------------------------------------------------
# Components
# --------------------------------------------------

tracker = HandTracker()
mouse = MouseController()
gesture = GestureController()


# --------------------------------------------------
# FPS
# --------------------------------------------------

previous_time = 0


# --------------------------------------------------
# Main loop
# --------------------------------------------------

while True:

    success, frame = camera.read()

    if not success:
        break

    # Mirror camera
    frame = cv2.flip(frame, 1)

    # Hand detection
    frame = tracker.findHands(frame)

    # Landmarks
    landmarks = tracker.findPosition(frame)


    if landmarks:

        # Index fingertip
        x = landmarks[8][1]
        y = landmarks[8][2]


        # --------------------------------------------------
        # FIST = FREEZE
        # --------------------------------------------------

        if gesture.detect_freeze(landmarks):

            cv2.putText(
                frame,
                "FROZEN",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2
            )


        else:

            # --------------------------------------------------
            # DRAG
            # --------------------------------------------------

            drag_status = gesture.detect_drag(landmarks)

            if drag_status == "START":

                pyautogui.mouseDown()

                print("DRAG START")


            elif drag_status == "DRAGGING":

                # Cursor movement continues
                # while mouse button is held

                mouse.move(x, y)


            elif drag_status == "DROP":

                pyautogui.mouseUp()

                print("DROP")


            # --------------------------------------------------
            # Normal cursor movement
            # --------------------------------------------------

            else:

                # Don't move cursor with right-click gesture
                # or open palm scrolling gesture

                if not gesture.is_open_palm(landmarks):

                    mouse.move(x, y)


            # --------------------------------------------------
            # LEFT CLICK
            # --------------------------------------------------

            if gesture.detect_left_click(landmarks):

                pyautogui.click()

                print("LEFT CLICK")


            # --------------------------------------------------
            # RIGHT CLICK
            # --------------------------------------------------

            if gesture.detect_right_click(landmarks):

                pyautogui.rightClick()

                print("RIGHT CLICK")


            # --------------------------------------------------
            # SCROLL
            # --------------------------------------------------

            scroll_direction = gesture.detect_scroll(landmarks)

            if scroll_direction == 1:

                pyautogui.scroll(2)

                print("SCROLL UP")


            elif scroll_direction == -1:

                pyautogui.scroll(-2)

                print("SCROLL DOWN")


        # --------------------------------------------------
        # Fingertip indicator
        # --------------------------------------------------

        cv2.circle(
            frame,
            (x, y),
            10,
            (255, 0, 255),
            cv2.FILLED
        )


    # --------------------------------------------------
    # FPS calculation
    # --------------------------------------------------

    current_time = time.time()

    fps = 1 / (current_time - previous_time) \
        if previous_time != 0 else 0

    previous_time = current_time


    cv2.putText(
        frame,
        f"FPS: {int(fps)}",
        (20, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2
    )


    # --------------------------------------------------
    # Instructions
    # --------------------------------------------------

    cv2.putText(
        frame,
        "Q = Quit",
        (20, 115),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )


    # --------------------------------------------------
    # Display
    # --------------------------------------------------

    cv2.imshow("Virtual Mouse", frame)


    # --------------------------------------------------
    # Quit
    # --------------------------------------------------

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# --------------------------------------------------
# Cleanup
# --------------------------------------------------

camera.release()
cv2.destroyAllWindows()