import math
import time


class GestureController:

    def __init__(self):
        self.last_click_time = 0
        self.last_right_click_time = 0

        self.click_cooldown = 0.5
        self.right_click_cooldown = 0.5

    def distance(self, x1, y1, x2, y2):
        return math.hypot(x2 - x1, y2 - y1)

    def detect_left_click(self, landmarks):

        if not landmarks:
            return False

        thumb_x = landmarks[4][1]
        thumb_y = landmarks[4][2]

        index_x = landmarks[8][1]
        index_y = landmarks[8][2]

        distance = self.distance(
            thumb_x,
            thumb_y,
            index_x,
            index_y
        )

        if distance < 35:

            current_time = time.time()

            if current_time - self.last_click_time > self.click_cooldown:
                self.last_click_time = current_time
                return True

        return False

    def detect_right_click(self, landmarks):

        if not landmarks:
            return False

        # Fingertip Y coordinates
        index_y = landmarks[8][2]
        middle_y = landmarks[12][2]

        # PIP joint Y coordinates
        index_pip_y = landmarks[6][2]
        middle_pip_y = landmarks[10][2]

        # Ring and pinky fingertips
        ring_y = landmarks[16][2]
        pinky_y = landmarks[20][2]

        ring_pip_y = landmarks[14][2]
        pinky_pip_y = landmarks[18][2]

        # Index and middle fingers are UP
        index_up = index_y < index_pip_y
        middle_up = middle_y < middle_pip_y

        # Ring and pinky fingers are DOWN
        ring_down = ring_y > ring_pip_y
        pinky_down = pinky_y > pinky_pip_y

        if index_up and middle_up and ring_down and pinky_down:

            current_time = time.time()

            if current_time - self.last_right_click_time > self.right_click_cooldown:

                self.last_right_click_time = current_time
                return True

        return False