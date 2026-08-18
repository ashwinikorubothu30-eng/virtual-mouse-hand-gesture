import math
import time


class GestureController:

    def __init__(self):

        # Click
        self.last_click_time = 0
        self.last_right_click_time = 0

        self.click_cooldown = 0.5
        self.right_click_cooldown = 0.7

        # Scroll
        self.previous_scroll_y = None
        self.scroll_threshold = 20

        # Drag
        self.pinch_start_time = None
        self.drag_hold_time = 0.6
        self.dragging = False

        # Gesture state
        self.frozen = False

    # --------------------------------------------------
    # Distance
    # --------------------------------------------------

    def distance(self, x1, y1, x2, y2):
        return math.hypot(x2 - x1, y2 - y1)

    # --------------------------------------------------
    # Finger states
    # --------------------------------------------------

    def fingers_up(self, landmarks):

        if not landmarks:
            return []

        fingers = []

        # Thumb
        thumb_up = landmarks[4][1] < landmarks[3][1]
        fingers.append(thumb_up)

        # Index
        fingers.append(landmarks[8][2] < landmarks[6][2])

        # Middle
        fingers.append(landmarks[12][2] < landmarks[10][2])

        # Ring
        fingers.append(landmarks[16][2] < landmarks[14][2])

        # Pinky
        fingers.append(landmarks[20][2] < landmarks[18][2])

        return fingers

    # --------------------------------------------------
    # Pinch
    # --------------------------------------------------

    def is_pinching(self, landmarks):

        if not landmarks:
            return False

        distance = self.distance(
            landmarks[4][1],
            landmarks[4][2],
            landmarks[8][1],
            landmarks[8][2]
        )

        return distance < 35

    # --------------------------------------------------
    # Open Palm
    # --------------------------------------------------

    def is_open_palm(self, landmarks):

        fingers = self.fingers_up(landmarks)

        if len(fingers) != 5:
            return False

        return all(fingers)

    # --------------------------------------------------
    # Fist
    # --------------------------------------------------

    def is_fist(self, landmarks):

        fingers = self.fingers_up(landmarks)

        if len(fingers) != 5:
            return False

        # All four main fingers down
        return not any(fingers[1:])

    # --------------------------------------------------
    # Left Click
    # --------------------------------------------------

    def detect_left_click(self, landmarks):

        if not landmarks:
            return False

        # Don't click while dragging
        if self.dragging:
            return False

        if not self.is_pinching(landmarks):
            self.pinch_start_time = None
            return False

        if self.pinch_start_time is None:
            self.pinch_start_time = time.time()
            return False

        duration = time.time() - self.pinch_start_time

        # Quick pinch
        if duration < self.drag_hold_time:

            current_time = time.time()

            if current_time - self.last_click_time > self.click_cooldown:

                self.last_click_time = current_time

                # Prevent repeated clicks
                self.pinch_start_time = time.time() + 100

                return True

        return False

    # --------------------------------------------------
    # Right Click
    # --------------------------------------------------

    def detect_right_click(self, landmarks):

        if not landmarks or self.dragging:
            return False

        fingers = self.fingers_up(landmarks)

        # Index + middle UP
        # Ring + pinky DOWN
        if (
            fingers[1]
            and fingers[2]
            and not fingers[3]
            and not fingers[4]
        ):

            current_time = time.time()

            if (
                current_time - self.last_right_click_time
                > self.right_click_cooldown
            ):

                self.last_right_click_time = current_time
                return True

        return False

    # --------------------------------------------------
    # Scroll
    # --------------------------------------------------

    def detect_scroll(self, landmarks):

        # Scroll ONLY with open palm
        if not self.is_open_palm(landmarks):

            self.previous_scroll_y = None
            return 0

        current_y = landmarks[12][2]

        if self.previous_scroll_y is None:

            self.previous_scroll_y = current_y
            return 0

        movement = self.previous_scroll_y - current_y

        self.previous_scroll_y = current_y

        if movement > self.scroll_threshold:
            return 1

        if movement < -self.scroll_threshold:
            return -1

        return 0

    # --------------------------------------------------
    # Drag
    # --------------------------------------------------

    def detect_drag(self, landmarks):

        if not landmarks:
            return "NONE"

        pinching = self.is_pinching(landmarks)

        if pinching:

            if self.pinch_start_time is None:
                self.pinch_start_time = time.time()

            duration = time.time() - self.pinch_start_time

            if duration >= self.drag_hold_time:

                if not self.dragging:

                    self.dragging = True
                    return "START"

                return "DRAGGING"

        else:

            if self.dragging:

                self.dragging = False
                self.pinch_start_time = None

                return "DROP"

            self.pinch_start_time = None

        return "NONE"

    # --------------------------------------------------
    # Freeze with fist
    # --------------------------------------------------

    def detect_freeze(self, landmarks):

        if self.is_fist(landmarks):

            self.frozen = True
            return True

        self.frozen = False
        return False