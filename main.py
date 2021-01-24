import cv2
from ScreenRecorder import ScreenRecorder
from Display import Display
from AI import AI
import numpy as np
import datetime
import time

SCREEN_RESOLUTION = (1920,1080)

def play_once(params, screen):
    """
    Play a single round until gameover
    """
    ai = AI(params)
    screen.locate_game()
    ai.start(screen.get())
    display = Display()

    with open("log.txt", "a") as file:
        now = datetime.datetime.now()
        file.write("\n")
        file.write(now.strftime("%Y-%m-%d %H:%M:%S"))
        file.write(f"\n params: {params}\n")

    while True:
        img = screen.get()
        distance, height = ai.step(img)
        display.show_image(img, ai, distance, height)

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
    screen_recorder = ScreenRecorder(SCREEN_RESOLUTION)
    cv2.imshow("Computer Vision", screen_recorder.get())
    print("Please keep the game window focused")
    print("Game will start in 5 seconds")
    wait_animation()

    params = {"jump_dist": 100,
            "jump_dist_delta": 45,
            "jump_time": 0.2,
            "crouch_time": 1}
    play_once(params, screen_recorder)
  

def wait_animation():
    for i in range(5):
        time.sleep(1)
        print(".", end="", flush=True)

if __name__ == "__main__":
    main()
