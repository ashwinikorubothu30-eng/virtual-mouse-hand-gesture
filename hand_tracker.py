def findPosition(self, frame, handNo=0):

    landmark_list = []

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = self.hands.process(rgb)

    if results.multi_hand_landmarks:

        myHand = results.multi_hand_landmarks[handNo]

        h, w, c = frame.shape

        for id, lm in enumerate(myHand.landmark):

            cx = int(lm.x * w)
            cy = int(lm.y * h)

            landmark_list.append([id, cx, cy])

    return landmark_list