import cv2
from hand_tracker import HandTracker

camera = cv2.VideoCapture(0)

tracker = HandTracker()

while True:

    success, frame = camera.read()

    if not success:
        break

    frame = tracker.findHands(frame)

    landmarks = tracker.findPosition(frame)

    if landmarks:

        x = landmarks[8][1]
        y = landmarks[8][2]

        cv2.circle(frame, (x, y), 15, (255, 0, 255), cv2.FILLED)

        print(x, y)

    cv2.imshow("Virtual Mouse", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()