import threading
import time
from gpiozero import Button as GPIOButton
import config


class Button:
    def __init__(self):
        self._button = GPIOButton(
            config.GPIO_BUTTON,
            pull_up=False,
        )

        self._pressed = self._button.is_pressed

        self._on_press = None
        self._on_release = None

        self._running = True

        self._thread = threading.Thread(
            target=self._loop,
            daemon=True,
        )
        self._thread.start()

    def register_press_callback(self, callback):
        self._on_press = callback

    def register_release_callback(self, callback):
        self._on_release = callback

    def is_pressed(self):
        return self._pressed

    def shutdown(self):
        self._running = False
        self._thread.join()
        self._button.close()

    def _loop(self):
        while self._running:
            state = self._button.is_pressed

            if state != self._pressed:
                self._pressed = state

                if state:
                    if self._on_press:
                        self._on_press()
                else:
                    if self._on_release:
                        self._on_release()

            time.sleep(config.BUTTON_POLL_INTERVAL)