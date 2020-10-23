from mss import mss
import cv2
import numpy as np

class Screen:
    """
    A class used to capture the game screen
    Takes screenshots of a game region, converts it and returns
    """
    sct = mss()
    score = 0
    RESOLUTION = (0,0)
    monitor, game_area = {}, {}
    HEIGHT_OFFSET = 10


    def __init__(self, resolution):
        self.RESOLUTION = resolution
        self.monitor = {'top': 0, 'left': 0, 'width': resolution[0], 'height': resolution[1]}
        self.get_borders()

    def get_borders(self):
        """
        Ask user where the game area is and store the it's borders
        """
        img = self.get_raw_screen()
        
        game_r = cv2.selectROI("Select Box", img)
        locs = ["left", "top", "width", "height"]
        for i, loc in enumerate(locs):
            self.monitor[loc] = game_r[i]

        if(not game_r[2] or not game_r[3]):
            print("ROI not selected, exiting.")
            with open("log.txt", "a") as file:
                file.write(" ERROR: Unable to read ROI, exit(1)\n")
            exit(1)

        self.game_area = self.monitor.copy()
        cv2.destroyAllWindows()
    
    def locate_game(self):
        """
        Locate where the correct game area is based on pixel landmarks
        """
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
        assert self.game_area['top'] >= 0 
        assert self.game_area['left'] >= 0
        assert self.game_area['top'] + self.game_area['height'] < self.RESOLUTION[1]
        assert self.game_area['left'] + self.game_area['width'] < self.RESOLUTION[0]


    def convert_img(self, sct_img):
        """
        Convert an image into Binary array, includes color correction for night mode
        making sure the game colors are always consistent
        """
        img = np.array(sct_img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        T, thresh_img = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)
        if cv2.countNonZero(thresh_img) <= 0.5 * img.shape[0] * img.shape[1]:
            img = cv2.bitwise_not(img)
            T, thresh_img = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)
        return thresh_img

    def get_raw_screen(self):
        """
        Take an screenshot
        """
        return np.array(self.sct.grab(self.monitor))

    def get(self):
        """
        Return game image
        """
        return self.convert_img(self.sct.grab(self.game_area))