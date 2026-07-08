"""
Simple test for button.py
"""

from time import sleep

from button import Button


def on_press():
    print("Pressed")


def on_release():
    print("Released")


def main():
    button = Button()

    button.register_press_callback(on_press)
    button.register_release_callback(on_release)

    print("Button test")
    print("Touch the sensor...")
    print("Press Ctrl+C to exit.\n")

    try:
        while True:
            sleep(0.1)

            # Optional: show current state
            # print(button.is_pressed())

    except KeyboardInterrupt:
        print("\nStopping...")

    finally:
        button.shutdown()


if __name__ == "__main__":
    main()