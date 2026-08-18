import cv2
import mediapipe as mp


class HandTracker:

    def __init__(self):

        self.mpHands = mp.solutions.hands

        self.hands = self.mpHands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )

        self.mpDraw = mp.solutions.drawing_utils

        # Store latest detection result
        self.results = None

    def findHands(self, frame):

        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        # Process frame only once
        self.results = self.hands.process(rgb)

        if self.results.multi_hand_landmarks:

            for hand in self.results.multi_hand_landmarks:

                self.mpDraw.draw_landmarks(
                    frame,
                    hand,
                    self.mpHands.HAND_CONNECTIONS
                )

        return frame

    def findPosition(self, frame, handNo=0):

        landmark_list = []

        if self.results is None:
            return landmark_list

        if self.results.multi_hand_landmarks:

            if handNo >= len(self.results.multi_hand_landmarks):
                return landmark_list

            myHand = self.results.multi_hand_landmarks[handNo]

            h, w, c = frame.shape

            for id, lm in enumerate(myHand.landmark):

                cx = int(lm.x * w)
                cy = int(lm.y * h)

                landmark_list.append(
                    [id, cx, cy]
                )

        return landmark_list