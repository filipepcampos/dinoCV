import cv2
from ScreenRecorder import ScreenRecorder
from Display import Display
from Logger import Logger
from Game import Game
from Agent import Agent
import numpy as np
import datetime
import time

SCREEN_RESOLUTION = (1920,1080)

def play_once(params, screen):
    """
    Play a single round until gameover
    """
    game, display, logger = Game(), Display(), Logger("log.txt")

    screen.locate_game()
    game.start(screen.get())

    params["dino_height"] = game.get_dinossaur_height()
    agent = Agent(params)

    logger.log_start(params)

    while True:
        img = screen.get()
        state = game.get_state(img)
        action, time = agent.step(state)
        game.act(action, time)
        display.show_image(img, game, state)

        if(game.gameover()):
            break

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'): # Quit
            cv2.destroyAllWindows()
            exit(0)
        elif key == ord('s'): # Relocate the game if any error occurs
            screen.locate_game()
    
    logger.log_score(game.score)


def main():
    screen_recorder = ScreenRecorder(SCREEN_RESOLUTION)
    cv2.imshow("Computer Vision", screen_recorder.get())
    print("Please keep the game window focused")
    print("Game will start in 5 seconds")
    wait_animation()

    game = Game()
    params = {"jump_dist": 100,
            "jump_dist_delta": 45,
            "jump_time": 0.2,
            "crouch_time": 1}
    agent = Agent(params)
    play_once(params, screen_recorder)
  

def wait_animation():
    for i in range(5):
        time.sleep(1)
        print(".", end="", flush=True)

if __name__ == "__main__":
    main()
