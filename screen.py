from mss import mss
import cv2
import numpy as np

class Screen:
    sct = mss()
    score = 0
    monitor, game_area = {}, {}
    HEIGHT_OFFSET = 10


    def __init__(self, resolution):
        self.monitor = {'top': 0, 'left': 0, 'width': resolution[0], 'height': resolution[1]}
        self.get_borders()

    def get_borders(self):
        img = self.get_raw_screen()
        
        game_r = cv2.selectROI("Select Box", img)
        locs = ["left", "top", "width", "height"]
        for i, loc in enumerate(locs):
            self.monitor[loc] = game_r[i]

        self.game_area = self.monitor.copy()
        cv2.destroyAllWindows()
    
    def locate_game(self):
        img = cv2.cvtColor(self.get_raw_screen(), cv2.COLOR_BGR2GRAY)
        binary_img = (img < 100).astype(int)

        column_sum = binary_img.sum(axis=1)
        top = np.argmax(column_sum > 0)
        bot = np.argmax(column_sum)
        left = np.argmax(binary_img.sum(axis=0) > 10)

        self.game_area['top'] = top + self.monitor["top"]
        self.game_area['height'] = bot - top - self.HEIGHT_OFFSET
        self.game_area['left'] = left + self.monitor["left"]
        self.game_area['width'] = self.monitor['width'] - left

    def convert_img(self, sct_img):
        img = np.array(sct_img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        T, thresh_img = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)
        if cv2.countNonZero(thresh_img) == 0:
            img = cv2.bitwise_not(img)
            T, thresh_img = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)
        return thresh_img

    def get_raw_screen(self):
        return np.array(self.sct.grab(self.monitor))

    def get(self):
        return self.convert_img(self.sct.grab(self.game_area))