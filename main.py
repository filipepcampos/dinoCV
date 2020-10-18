import cv2
from screen import Screen
from ai import AI
import numpy as np
import datetime

SCREEN_RESOLUTION = (2560, 1440)

def show_image(img, ai, distance, height):
    cv2.putText(img, str(ai.score), 
            org=(img.shape[0] // 2, 80), 
            fontFace=cv2.FONT_HERSHEY_SIMPLEX, 
            fontScale=1, color=0, thickness=3)
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    cv2.rectangle(img, (ai.right, ai.top), (ai.right, img.shape[0]-1), (0,0,255), 1)
    cv2.rectangle(img, ai.reference_pixels[0], ai.reference_pixels[1], (255,0,0), 1)
    cv2.rectangle(img, (ai.right, height), (ai.right + distance, height), (0, 255, 0), 3)
    cv2.imshow("Computer Vision", img)

def main():
    screen = Screen(SCREEN_RESOLUTION)
    with open("log.txt", "a") as file:
        now = datetime.datetime.now()
        file.write(now.strftime("%Y-%m-%d %H:%M:%S"))
        file.write(f"\n res: {SCREEN_RESOLUTION}\n")
    ai = AI(screen.get())
    while True:
        img = screen.get()
        distance, height = ai.step(img)
        show_image(img, ai, distance, height)

        key = cv2.waitKey(50) & 0xFF
        if key == ord('q'):
            cv2.destroyAllWindows()
            break
        elif key == ord('s'):
            screen.locate_game()
            ai = AI(screen.get())
        

if __name__ == "__main__":
    main()
