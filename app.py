"""
Main Application Orchestrator for Hello Pi.
Ties together the Display, Audio, and Button subsystems.
"""

import time
import sys

from audio import Audio
from button import Button
from display import Display


def main():
    print("Initializing hardware subsystems...")
    
    # 1. Instantiate the hardware
    display = Display()
    audio = Audio()
    button = Button()

    # 2. Define the state behaviors
    def mute():
        """Triggered when the button is pressed."""
        print("State: MUTED")
        audio.stop()
        display.show(
            title="MUTED",
            subtitle="Audio stopped",
            background="red",
        )

    def live():
        """Triggered when the button is released."""
        print("State: LIVE")
        audio.start()
        display.show(
            title="LIVE",
            subtitle="Audio running",
            background="green",
        )

    # 3. Wire the button callbacks to the behaviors
    button.register_press_callback(mute)
    button.register_release_callback(live)

    # 4. Main Application Loop
    try:
        # Show a quick boot screen
        display.show(
            title="Hello Pi",
            subtitle="System Ready",
            background="blue",
        )
        time.sleep(1.5) 
        
        # Drop into the default live state
        live()

        print("\nSystem running! Press the button to mute.")
        print("Press Ctrl+C to exit.\n")
        
        # The main thread just idles. 
        # The button thread and ALSA subprocesses handle all the heavy lifting.
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nCaught Ctrl+C! Initiating graceful shutdown...")

    finally:
        # 5. The Holy Trinity of Clean Exits
        # This guarantees your pins and pipes are released no matter how the app crashes.
        print("Cleaning up hardware states...")
        button.shutdown()
        audio.shutdown()
        display.shutdown()
        print("Shutdown complete.")
        sys.exit(0)


if __name__ == "__main__":
    main()