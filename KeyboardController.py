from pynput.keyboard import Key, Controller
import time
import threading

def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper

class KeyboardController:
    controller = Controller()

    @threaded
    def _press_key(self, key, hold_duration):
        self.controller.press(key)
        time.sleep(hold_duration)
        self.controller.release(key)

    def jump(self, t=0):
        self._press_key(Key.space, t)
    
    def crouch(self, t=0):
        self._press_key(Key.down, t)
