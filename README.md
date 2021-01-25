# dinoCV

DinoCV is an computer vision implementation to record, analyze and act upon chrome's offline dinosaur game.

![](https://media.giphy.com/media/yISQ99Ru1zu6IPLf82/giphy.gif)

## Agent

Currently dinoCV uses a simple naive agent which decides when to jump/crouch based on some simple parameters. In the future this will be swapped for something better.

For example:
```python
params = {"jump_dist": 100,
          "jump_dist_delta": 25,
          "jump_time": 0.2,
          "crouch_time": 1.2}
```


## Usage
Currently there isn't an automatic monitor resolution detection, so you may need to adjust the value of `SCREEN_RESOLUTION` in `main.py` (Currently set to 1920x1080)

To open the game, just type `chrome://dino` on an chromium-based browser

After the game is open run `python3 main.py` and select the game area, it should at the very least include the dinosaur and score counters while not including any browser border

Five seconds after the selection, the game will start. In order to send input to the game, the game window must be focused.

![](https://media.giphy.com/media/ggW3YOFTvrz1KSBa4j/giphy.gif)

## Dependencies

* cv2
* numpy
* pynput
* mss
