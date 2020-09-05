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
    reference_pixel = (0, 0)
    kb = Controller()

    def __init__(self, img):
        self.score = Score(img)
        self.right = np.argmax(img.sum(axis=0) == 255 * img.shape[0])
        self.top = img.shape[0] - np.argmax(img[::-1,:self.right].sum(axis=1) == 255 * self.right)
        
        for i in range(0, img.shape[0] - 1 - self.top):
            if img[self.top + i, self.right-1] == 0:
                self.reference_pixel = (self.right - 1, self.top + i - 1)
                break

    def is_grounded(self, img):
        x, y = self.reference_pixel
        return img[y, x] == 255 and img[y+1, x] == 0

    def step(self, img):
        if self.score is not None:
            self.score.step(img)

        distances = [99999]
        for height in [self.top, self.top//2, 0]:
            for i in range(img.shape[1] - self.right - 1):
                if img[height-1, self.right + i] == 0:
                    distances.append(i)        
        distance = min(distances)

        if distance < 100 and self.is_grounded(img):
            self.jump(.3)      

    @threaded
    def jump(self, t=0):
        jumping = 1
        print(f"-> Jump {t} s")
        self.kb.press(Key.space)
        time.sleep(t)
        self.kb.release(Key.space)
    
    @threaded
    def crouch(self, t=0):
        self.kb.press(Key.down)
        time.sleep(t)
        self.kb.release(Key.down)
