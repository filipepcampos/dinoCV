import cv2
from screen import Screen
from ai import AI
import numpy as np

SCREEN_RESOLUTION = (2560, 1440)

def show_image(img, ai):
    cv2.putText(img, str(ai.score), 
            org=(img.shape[0] // 2, 80), 
            fontFace=cv2.FONT_HERSHEY_SIMPLEX, 
            fontScale=1, color=0, thickness=3)
    cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    cv2.rectangle(img, (ai.right, ai.top), (ai.right, img.shape[0]-1), (0,255,255))
    cv2.imshow("Computer Vision", img)

def main():
    screen = Screen(SCREEN_RESOLUTION)
    ai = AI(screen.get())
    while True:
        img = screen.get()
        ai.step(img)
        show_image(img, ai)

        key = cv2.waitKey(50) & 0xFF
        if key == ord('q'):
            cv2.destroyAllWindows()
            break
        elif key == ord('s'):
            screen.locate_game()
            ai = AI(screen.get())
        

if __name__ == "__main__":
    main()
