# 🎤 Hello Pi 2.1

A lightweight voice assistant platform built on the Raspberry Pi.

Hello Pi combines a microphone, speaker, display and touch button into a simple, modular Python project that can be expanded into a complete voice assistant.

## Features

- 🎙️ Live I²S microphone passthrough
- 🔊 3.5 mm audio output
- 📺 ST7735 SPI TFT display
- 👆 Capacitive touch mute button
- 🧩 Modular Python architecture

## Hardware

| Component | Model |
|----------|-------|
| SBC | Raspberry Pi 4B |
| Display | ST7735S 160×128 TFT |
| Microphone | INMP441 |
| Button | Capacitive Touch Sensor |

## Wiring

### Display

| TFT | Raspberry Pi |
|-----|---------------|
| VCC | 3.3V |
| GND | GND |
| SCL | GPIO11 (SPI CLK) |
| SDA | GPIO10 (SPI MOSI) |
| CS | GPIO8 (CE0) |
| DC | GPIO17 |
| RST | GPIO25 |
| BL | GPIO22 |

### Microphone (INMP441)

| INMP441 | Raspberry Pi |
|----------|--------------|
| VCC | 3.3V |
| GND | GND |
| SCK | GPIO18 (I²S BCLK) |
| WS | GPIO19 (I²S LRCLK) |
| SD | GPIO20 (I²S DIN) |

### Button

| Button | Raspberry Pi |
|--------|---------------|
| VCC | 3.3V |
| GND | GND |
| OUT | GPIO26 |

## Project

```
Hello Pi 2.1
├── audio.py
├── button.py
├── display.py
├── config.py
├── main.py
└── requirements.txt
```

## Installation

```bash
git clone https://github.com/Tenerife28/Hello-Pi-2.1.git
cd Hello-Pi-2.1

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

## Run

```bash
python3 main.py
```

## Roadmap

- ✅ Audio
- ✅ Display
- ✅ Touch button
- ⏳ Wake word
- ⏳ Speech recognition
- ⏳ Voice assistant

---

Built with ❤️ for Raspberry Pi.