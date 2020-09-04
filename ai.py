import numpy as np
from score import Score

class AI:
    score = None
    right = 0
    top = 0

    def __init__(self, img):
        self.score = Score(img)
        self.right = np.argmax(img.sum(axis=0) == 255 * img.shape[0])
        self.top = img.shape[0] - np.argmax(img[::-1].sum(axis=1) == 255 * img.shape[1]) # TODO: Limit image to self.right
        print(f"right:{self.right}  top:{self.top}")

    def step(self, img):
        if self.score is not None:
            self.score.step(img)
        