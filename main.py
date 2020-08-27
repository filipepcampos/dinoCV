import cv2
from screen import Screen
import numpy as np
import keyboard

def main():
    base_frame = None
    screen = Screen(1920, 1080)

    while True:
        img = screen.get_screen()    
        screen.get_score()
        T, thresh_img = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)
        if cv2.countNonZero(thresh_img) == 0:
            img = cv2.bitwise_not(img)
            T, thresh_color = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)
        cv2.imshow("Computer Vision", thresh_img)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
        


if __name__ == "__main__":
    main()
