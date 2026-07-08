import subprocess

import config


class Audio:
    def __init__(self):
        self._arecord = None
        self._aplay = None

    def start(self):
        if self.running():
            return

        self._arecord = subprocess.Popen(
            [
                config.ARECORD,
                "-D", config.CAPTURE_DEVICE,
                "-f", config.AUDIO_FORMAT,
                "-r", str(config.AUDIO_RATE),
                "-c", str(config.AUDIO_CHANNELS),
                "--buffer-size", str(config.AUDIO_BUFFER_SIZE),
                "--period-size", str(config.AUDIO_PERIOD_SIZE),
                "-t", "raw",
            ],
            stdout=subprocess.PIPE,
        )

        self._aplay = subprocess.Popen(
            [
                config.APLAY,
                "-D", config.PLAYBACK_DEVICE,
                "-f", config.AUDIO_FORMAT,
                "-r", str(config.AUDIO_RATE),
                "-c", str(config.AUDIO_CHANNELS),
                "--buffer-size", str(config.AUDIO_BUFFER_SIZE),
                "--period-size", str(config.AUDIO_PERIOD_SIZE),
                "-t", "raw",
            ],
            stdin=self._arecord.stdout,
        )

        self._arecord.stdout.close()

    def stop(self):
        for proc in (self._aplay, self._arecord):
            if proc and proc.poll() is None:
                proc.terminate()
                try:
                    proc.wait(timeout=config.AUDIO_TERMINATE_TIMEOUT)
                except subprocess.TimeoutExpired:
                    proc.kill()
                    proc.wait()

        self._arecord = None
        self._aplay = None

    def shutdown(self):
        self.stop()

    def running(self):
        return (
            self._arecord is not None
            and self._aplay is not None
            and self._arecord.poll() is None
            and self._aplay.poll() is None
        )