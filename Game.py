import numpy as np
from Score import Score
from KeyboardController import KeyboardController
import time


class Game:
    """
    Game environment
    """
    right, top, last_img, timeout = 0, 0, 0, 0
    reference_pixels = ((0, 0), (0, 0))
    kb = KeyboardController()

    def __init__(self):
        self.kb.jump() # Start the game
        time.sleep(1)

    def start(self, img):
        self.score = Score(img)
        self.right = np.argmax(img.sum(axis=0) == 255 * img.shape[0])
        self.top = img.shape[0] - np.argmax(img[::-1,:self.right].sum(axis=1) == 255 * self.right)
        
        # Get dinossaur's nose location to track if he is on the ground
        x, y = 0, 0
        for i in range(0, img.shape[0] - 1 - self.top):
            if img[self.top + i, self.right-1] == 0:
                x, y = self.right - 1, self.top + i - 1
                break
        for i in range(1, img.shape[0] - 1 - y):            
            if img[y + i, self.right-1] == 255:
                self.reference_pixels = ((x, y), (self.right - 1, y + i))
                break
    
    def get_state(self, img):
        """
        Return current game state
        """
        self._update_timeout(img)
        if self.score is not None:
            self.score.step(img)
        dist, height = self._get_dist(img)     
        return dist, height, self._is_grounded(img), self.score.get()
    
    def get_dinossaur_height(self):
        return self.top
    
    def act(self, action, time=0):
        if(action == "jump"):
            self.kb.jump(time)
        elif(action == "crouch"):
            self.kb.crouch(time)
    
    def gameover(self):
        return self.timeout > 100

    def _is_grounded(self, img):
        """
        Returns true if dino is currently on the ground
        """
        x1, y1 = self.reference_pixels[0]
        x2, y2 = self.reference_pixels[1]
        return img[y1, x1] == 255 and img[y1+1, x1] == 0 and img[y2, x2] == 255 and img[y2-1, x2] == 0

    def _get_dist(self, img):
        """
        Traces 3 pixels into the nearest object
        Returns distance to the nearest object and height of the corresponding trace
        """
        min_distance, height = 9999, 0
        track_heights = (self.top, self.top + (img.shape[0] - self.top) // 2, img.shape[0]-1)

        for h in track_heights:
            for i in range(img.shape[1] - self.right - 1):
                if img[h-1, self.right + i] == 0 and i < min_distance:
                    min_distance = i
                    height = h
        return min_distance, height

    def _update_timeout(self, img):
        """
        Update the timeout value, it tracks how many steps since the img hasn't changed
        After enough time, gameover will occur
        """
        if (img == self.last_img).all():
            self.timeout += 1
        else:
            self.timeout = 0
        self.last_img = img.copy()