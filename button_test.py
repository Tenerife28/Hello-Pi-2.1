import time

import RPi.GPIO as GPIO

BUTTON_PIN = 26

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(BUTTON_PIN, GPIO.IN)

print("Touch the sensor (Ctrl+C to exit)\n")

last = None

try:
    while True:
        state = GPIO.input(BUTTON_PIN)

        if state != last:
            print(f"GPIO26 = {state}")
            last = state

        time.sleep(0.01)

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()