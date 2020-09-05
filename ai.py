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

    def __init__(self, img):
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
        x1, y1 = self.reference_pixels[0]
        x2, y2 = self.reference_pixels[1]
        return img[y1, x1] == 255 and img[y1+1, x1] == 0 and img[y2, x2] == 255 and img[y2-1, x2] == 0

    def step(self, img):
        if self.score is not None:
            self.score.step(img)

        min_distance, height = 9999, 0
        track_heights = [self.top, self.top + (img.shape[0] - self.top) // 2, img.shape[0]-1]

        for h in track_heights:
            for i in range(img.shape[1] - self.right - 1):
                if img[h-1, self.right + i] == 0 and i < min_distance:
                    min_distance = i
                    height = h

        if min_distance < 100 and self.is_grounded(img):
            self.jump(.3)
        return min_distance, height

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
