import cv2
from screen import Screen
from ai import AI
import numpy as np
import datetime
import time

SCREEN_RESOLUTION = (2560, 1440)

def show_image(img, ai, distance, height):
    """
    Show an visual representation of the AI's vision
    """
    cv2.putText(img, str(ai.score), 
            org=(img.shape[0] // 2, 80), 
            fontFace=cv2.FONT_HERSHEY_SIMPLEX, 
            fontScale=1, color=0, thickness=3)
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    cv2.rectangle(img, (ai.right, ai.top), (ai.right, img.shape[0]-1), (0,0,255), 1)
    cv2.rectangle(img, ai.reference_pixels[0], ai.reference_pixels[1], (255,0,0), 1)
    if(height):
        cv2.rectangle(img, (ai.right, height), (ai.right + distance, height), (0, 255, 0), 3)
    cv2.imshow("Computer Vision", img)

def play_once(params, screen):
    """
    Play a single round until gameover
    """
    ai = AI(params)
    screen.locate_game()
    ai.start(screen.get())

    with open("log.txt", "a") as file:
        now = datetime.datetime.now()
        file.write("\n")
        file.write(now.strftime("%Y-%m-%d %H:%M:%S"))
        file.write(f"\n params: {params}\n")

    while True:
        img = screen.get()
        distance, height = ai.step(img)
        show_image(img, ai, distance, height)

        if(ai.gameover()):
            break

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            cv2.destroyAllWindows()
            exit(0)
        elif key == ord('s'):
            screen.locate_game()
    
    with open("log.txt", "a") as file:
        file.write(f" final_score: {ai.score}\n")


def main():
    screen = Screen(SCREEN_RESOLUTION)
    cv2.imshow("Computer Vision", screen.get())
    print("Please keep the game window focused")
    print("Game will start in 5 seconds")
    for i in range(5):
        time.sleep(1)
        print(".", end="", flush=True)

    params = {"jump_dist": 100,
            "jump_dist_delta": 45,
            "jump_time": 0.2,
            "crouch_time": 1}
    play_once(params, screen)
  

if __name__ == "__main__":
    main()
