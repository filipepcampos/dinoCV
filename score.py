import numpy as np
import math

class Score:
    initialized = False
    score_location = ()
    score = 0
    blink_count = 0
    was_white = False

    def __init__(self, img):
        end = img.shape[1] - 1
        start = np.argmax(img[0, :] == 0)
        for i in range(img.shape[1]):
            if img[0, -i] == 0:
                end = img.shape[1] - i
                break
        self.score_location = (start, end)
        self.initialized = True

    def step(self, img):
        if self.initialized:
            start, end = self.score_location       
            score_sum = np.sum(img[0, start:end])
            if score_sum == (end-start)*255:
                if not self.was_white:
                    self.blink_count += 1
                    self.score = math.ceil(self.blink_count / 4)
                self.was_white = True
            else:
                self.was_white = False

    def __str__(self):
        return str(self.score)