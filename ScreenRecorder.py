from mss import mss
import cv2
import numpy as np

from ImageConverter import ImageConverter

class ScreenRecorder:
    """
    A class used to capture the game screen
    Takes screenshots of a game region, converts it and returns
    """
    sct = mss()
    HEIGHT_OFFSET = 10
    converter = ImageConverter()


    def __init__(self, resolution):
        self.RESOLUTION = resolution
        self.game_area = {'top': 0, 'left': 0, 'width': resolution[0], 'height': resolution[1]}
        self._get_borders()

    def _get_borders(self):
        """
        Select the proper game area
        """
        img = self._get_screen()
        
        game_r = cv2.selectROI("Select Box", img)
        locs = ["left", "top", "width", "height"]
        for i, loc in enumerate(locs):
            self.game_area[loc] = game_r[i]

        if(not game_r[2] or not game_r[3]):
            print("ROI not selected, exiting.")
            with open("log.txt", "a") as file:
                file.write(" ERROR: Unable to read ROI, exit(1)\n")
            raise "Invalid game area selection"

        cv2.destroyAllWindows()
    
    def locate_game(self):
        """
        Locate where the correct game area is based on pixel landmarks
        """
        img = cv2.cvtColor(self._get_screen(), cv2.COLOR_BGR2GRAY)
        binary_img = (img < 100).astype(int)

        column_sum = binary_img.sum(axis=1)
        top = np.argmax(column_sum > 0)
        bot = np.argmax(column_sum)
        left = np.argmax(binary_img.sum(axis=0) > 10)

        self.game_area['top'] += top
        self.game_area['height'] = bot - top - self.HEIGHT_OFFSET
        self.game_area['left'] += left 
        self.game_area['width'] -= left
        assert self.game_area['top'] >= 0 
        assert self.game_area['left'] >= 0
        assert self.game_area['top'] + self.game_area['height'] < self.RESOLUTION[1]
        assert self.game_area['left'] + self.game_area['width'] < self.RESOLUTION[0]


    def convert_img(self, sct_img):
        return self.converter.convert(sct_img)

    def _get_screen(self):
        """
        Take an screenshot
        """
        return np.array(self.sct.grab(self.game_area))

    def get(self):
        """
        Return game image
        """
        return self.converter.convert(self.sct.grab(self.game_area))