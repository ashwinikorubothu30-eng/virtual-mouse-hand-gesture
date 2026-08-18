import pyautogui


class MouseController:

    def __init__(self, camera_width=640, camera_height=480):
        self.screen_width, self.screen_height = pyautogui.size()

        self.camera_width = camera_width
        self.camera_height = camera_height

        self.prev_x = 0
        self.prev_y = 0

        self.smoothing = 5

    def move(self, x, y):

        screen_x = int(x / self.camera_width * self.screen_width)
        screen_y = int(y / self.camera_height * self.screen_height)

        smooth_x = self.prev_x + (screen_x - self.prev_x) / self.smoothing
        smooth_y = self.prev_y + (screen_y - self.prev_y) / self.smoothing

        pyautogui.moveTo(int(smooth_x), int(smooth_y))

        self.prev_x = smooth_x
        self.prev_y = smooth_y