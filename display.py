"""
Display subsystem for the Hello Pi project.

Provides a simple interface for rendering text on the ST7735S SPI display.
"""

from __future__ import annotations

import time

from gpiozero import LED
from PIL import ImageFont
from luma.core.interface.serial import spi
from luma.core.render import canvas
from luma.lcd.device import st7735

import config


class Display:
    """ST7735S display driver."""

    def __init__(self) -> None:

        # ---------------- Backlight ----------------

        # self._bl = LED(config.GPIO_DISPLAY_BL)
        # self._bl.on()

        # Give the panel time to power up
        time.sleep(0.10)

        # ---------------- SPI ----------------

        self._serial = spi(
            port=config.SPI_PORT,
            device=config.SPI_DEVICE,
            gpio_DC=config.GPIO_DISPLAY_DC,
            gpio_RST=config.GPIO_DISPLAY_RST, 
            bus_speed_hz=config.SPI_BUS_SPEED, # Keep this at your 16_000_000!
            transfer_size=64,
            gpio_LIGHT=None,
        )

        time.sleep(0.05)

        # ---------------- LCD ----------------

        self._device = st7735(
            self._serial,
            width=config.DISPLAY_WIDTH,
            height=config.DISPLAY_HEIGHT,
            rotate=config.DISPLAY_ROTATION,
            h_offset=config.DISPLAY_H_OFFSET,
            v_offset=config.DISPLAY_V_OFFSET,
            gpio_LIGHT=config.GPIO_DISPLAY_BL,
        )

        time.sleep(0.10)

        # ---------------- Fonts ----------------

        try:
            self._title_font = ImageFont.truetype(
                config.DISPLAY_FONT,
                config.DISPLAY_TITLE_SIZE,
            )

            self._subtitle_font = ImageFont.truetype(
                config.DISPLAY_FONT,
                config.DISPLAY_SUBTITLE_SIZE,
            )

        except OSError:
            self._title_font = ImageFont.load_default()
            self._subtitle_font = ImageFont.load_default()

        self.clear()

    def show(
        self,
        title: str,
        subtitle: str = "",
        background: str = config.COLOR_BACKGROUND,
    ) -> None:
        """Render a screen."""

        self._render(title, subtitle, background)

    def clear(self) -> None:
        """Clear the display."""

        self._render("", "", config.COLOR_BACKGROUND)

    def backlight(self, on: bool) -> None:
        """Enable or disable the backlight."""

        # if on:
        #     self._bl.on()
        # else:
        #     self._bl.off()

    def shutdown(self) -> None:
        """Shutdown the display."""

        try:
            self.clear()
        except Exception:
            pass

        # self._bl.off()
        # self._bl.close()

    def _render(
        self,
        title: str,
        subtitle: str,
        background: str,
    ) -> None:
        """Render one frame."""

        with canvas(self._device) as draw:

            draw.rectangle(
                self._device.bounding_box,
                fill=background,
            )

            if title:

                draw.text(
                    (
                        config.DISPLAY_MARGIN_X,
                        config.DISPLAY_TITLE_Y,
                    ),
                    title,
                    font=self._title_font,
                    fill=config.COLOR_TITLE,
                )

            if subtitle:

                draw.text(
                    (
                        config.DISPLAY_MARGIN_X,
                        config.DISPLAY_SUBTITLE_Y,
                    ),
                    subtitle,
                    font=self._subtitle_font,
                    fill=config.COLOR_SUBTITLE,
                )