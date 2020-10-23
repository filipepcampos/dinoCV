import numpy as np
from score import Score
import time
from pynput.keyboard import Key, Controller
import threading

def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper

class AI:
    score = None
    right = 0
    top = 0
    reference_pixels = ((0, 0), (0, 0))
    kb = Controller()

    params = {}

    last_img = 0
    timeout = 0

    def __init__(self, params):
        self.params = params
        self.jump() # Get the game running
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

    def is_grounded(self, img):
        """
        Returns true if dino is currently on the ground
        """
        x1, y1 = self.reference_pixels[0]
        x2, y2 = self.reference_pixels[1]
        return img[y1, x1] == 255 and img[y1+1, x1] == 0 and img[y2, x2] == 255 and img[y2-1, x2] == 0

    def get_dist(self, img):
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

    def step(self, img):
        """
        Take an image as input, process it and do an action
        """
        self.update_timeout(img)
        if self.score is not None:
            self.score.step(img)

        dist, height = self.get_dist(img)                    
        on_ground = self.is_grounded(img)

        if height == self.top and on_ground:
            self.crouch(self.params["crouch_time"])
        elif dist < (self.params["jump_dist"] + int(self.score.get())*self.params["jump_dist_delta"]) and on_ground:
            self.jump(self.params["jump_time"])
        return dist, height

    def update_timeout(self, img):
        """
        Update the timeout value, it tracks how many steps since the img hasn't changed
        After enough time, gameover will occur
        """
        if (img == self.last_img).all():
            self.timeout += 1
        else:
            self.timeout = 0
        self.last_img = img.copy()

    def gameover(self):
        return self.timeout > 100

    @threaded
    def jump(self, t=0):
        self.kb.press(Key.space)
        time.sleep(t)
        self.kb.release(Key.space)
    
    @threaded
    def crouch(self, t=0):
        self.kb.press(Key.down)
        time.sleep(t)
        self.kb.release(Key.down)
