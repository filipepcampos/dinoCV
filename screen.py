from mss import mss
import cv2
import numpy as np

class Screen:
    sct = mss()
    monitor = {}

    def __init__(self, width, height):
        self.monitor = {'top': 0, 'left': 0, 'width': width, 'height': height}
        self.get_borders()

    def get_borders(self):
        sct_img = self.sct.grab(self.monitor)
        img = self.convert_img(sct_img, False)
        print("Please select game area")
        game_r = cv2.selectROI("Select Box", img)
        locs = ["left", "top", "width", "height"]
        for i, loc in enumerate(locs):
            self.monitor[loc] = game_r[i]
        print("Please select score area")
        score_r = cv2.selectROI("Select Box", img)
        cv2.destroyAllWindows()
        
    def convert_img(self, sct_img, convert_to_gray=True):
        img = np.array(sct_img)
        return img if not convert_to_gray else cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    def get_screen(self):
        return self.convert_img(self.sct.grab(self.monitor))