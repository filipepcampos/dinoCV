import cv2
import numpy as np

class ImageConverter:
    def convert(self, img):
        """
        Convert an image into Binary array, includes color correction for night mode
        making sure the game colors are always consistent
        """
        img = np.array(img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        T, thresh_img = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)
        if cv2.countNonZero(thresh_img) <= 0.5 * img.shape[0] * img.shape[1]:
            img = cv2.bitwise_not(img)
            T, thresh_img = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)
        return thresh_img