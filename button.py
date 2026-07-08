import threading
import time

import RPi.GPIO as GPIO

import config


class Button:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(config.GPIO_BUTTON, GPIO.IN)

        self._pressed = GPIO.input(config.GPIO_BUTTON)
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
        GPIO.cleanup(config.GPIO_BUTTON)

    def _loop(self):
        while self._running:
            state = GPIO.input(config.GPIO_BUTTON)

            if state != self._pressed:
                self._pressed = state

                if state:
                    if self._on_press:
                        self._on_press()
                else:
                    if self._on_release:
                        self._on_release()

            time.sleep(0.01)