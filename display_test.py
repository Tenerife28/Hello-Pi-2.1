from time import sleep

from display import Display


def main() -> None:
    display = Display()

    try:
        print("Testing display...")

        display.show(
            title="Hello Pi",
            subtitle="Initializing",
            background="blue",
        )
        sleep(2)

        display.show(
            title="Display",
            subtitle="Green screen",
            background="green",
        )
        sleep(2)

        display.show(
            title="Display",
            subtitle="Red screen",
            background="red",
        )
        sleep(2)

        display.show(
            title="Backlight",
            subtitle="Turning OFF",
            background="black",
        )
        sleep(1)

        display.backlight(False)
        sleep(2)

        display.backlight(True)

        display.show(
            title="Success!",
            subtitle="Driver OK",
            background="black",
        )

        input("\nPress ENTER to exit...")

    finally:
        display.shutdown()


if __name__ == "__main__":
    main()
    