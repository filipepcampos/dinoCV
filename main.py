import cv2
from screen import Screen
import numpy as np
import keyboard

def main():
    base_frame = None
    screen = Screen(2560, 1440)
    flip_colors = False

    while True:
        img = screen.get_screen()
        if base_frame is None:
            cv2.imshow("Computer Vision", img)
        else:
            if flip_colors:
                img = cv2.bitwise_not(img)
            T, thresh_img = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY)
            if cv2.countNonZero(thresh_img) == 0:
                flip_colors = not flip_colors
            cv2.imshow("Computer Vision", thresh_img)

        key = cv2.waitKey(25) & 0xFF
        if key == ord('q'):
            cv2.destroyAllWindows()
            break
        elif key == ord('t'):
            base_frame = img
        
        


if __name__ == "__main__":
    main()
