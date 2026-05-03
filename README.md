# 2 inch TFT Module 240×320 ST7789V GMT020-02-8P Display

Python scripts to drive a 2 inch TFT Module 240×320 ST7789V GMT020-02-8P display screen on Raspberry Pi 5 over SPI on Slackware Linux operating systems.

The scripts in this repository are using Python library **lgpio** to probe the Raspberry Pi 5's RP1 controller and will not work on previous Raspberry Pi versions.

All the python3 scripts in this repository will run on other Linux operating systems but may require some code adjustments.

Display images on the TFT display screen like this one:

![Slackpunk test Image](https://raw.githubusercontent.com/SAIRPi/st7789v-rpi/main/slackpunk.jpg "Slackpunk test Image")

## How to download this repository:

You should have git installed on your system. Then simply clone it:

```bash
    git clone https://github.com/SAIRPi/st7789v-gmt020-02-8p
```
To clone the repository into a directory of your choice:

```bash
    git clone https://github.com/SAIRPi/st7789v-gmt020-02-8p /path/to/your_directory_name
```

## The purpose of this repository

Many ST7789V TFT modules come with vague, incomplete, generic, or Arduino-only instructions and/or code examples that aren't directly usable on Raspberry Pi computers.

What this repository offers is a working solution for the 2 inch TFT Module 240×320 ST7789V GMT020-02-8P display running Slackware Linux on Raspberry Pi computers, including wiring instructions, python3 library dependencies, and example scripts.

The ST7789V GMT020-02-8P TFT (8-pin with backlight) module variant doesn't appear to have a dedicated product page on the manufacturer's [Golden Morning] website (https://goldenmorninglcd.com/tft-display-module/). Their GMT020-02 page only covers the 7-pin version. The GMT020-02-8P (8-pin) variant is not well documented or referenced online and Golden Morning don't seem to have published a dedicated page for it. 

## Overview

This repository contains Python scripts for a 2-inch 240x320 ST7789V GMT020-02-8P TFT module.

Included scripts:

- `st7789v_display.py` — display static images on the TFT screen
- `rpi_system_stats.py` - simple system status output, with user-configurable refresh rate and colours
- `matrix_digital_rain.py` — Matrix-style digital rain animation, with optional custom text and timestamp

**NB:** These scripts are now v2.1 which uses a two-stage search to find the correct GPIO interface, regardless of how the Linux system numbers them.

Test image:

- `slackpunk.jpg` - a 240x320 pixel JPG image used for testing the `st7789v_display.py` script

## Hardware

Target TFT module:

![2 inch TFT Module 240x320 ST7789V GMT020-02-8P](https://sairpi.penthux.net/img/jaffaworks/2-inch-TFT-Module-240x320-ST7789V-GMT020-02-8P.png "2 inch TFT Module 240x320 ST7789V GMT020-02-8P")

- **2 inch TFT module 240x320 ST7789V GMT020-02-8P**
- This is the **8-pin** version of the GMT020-02 TFT module with a separate BL (backlight) pin header connector. 

- **NB:** The variant **without** the separate BL pin is the GMT020-02-7P (example: https://goldenmorninglcd.com/tft-display-module/2-inch-240x320-st7789v-gmt020-02/).
- For all intents and purposes the only difference between the 7-pin and 8-pin variants is the backlight (header connector) on the 8-pin version, which can then be set ON/OFF via commands.

The python3 scripts in this repository may also work on other non-touch ST7789V-based TFT modules, but no guarantees! Try them and see for yourselves.

## TFT Module Wiring

ST7789V GMT020-02-8P TFT module wiring on the Raspberry Pi 40-pin GPIO header:

| TFT Pin | Raspberry Pi Pin | GPIO   |
|---------|------------------|--------|
| BL      | Pin 21           | GPIO9  |
| CS      | Pin 24           | GPIO8  |
| DC      | Pin 22           | GPIO25 |
| RST     | Pin 18           | GPIO24 |
| SDA     | Pin 19           | GPIO10 |
| SCL     | Pin 23           | GPIO11 |
| VCC     | Pin 17           | 3.3V   |
| GND     | Pin 20           | Ground |

## Requirements

Install python3 library dependencies:

```bash
    python3 -m pip install --upgrade pillow spidev numpy lgpio rpi-lgpio
```

## Usage

### Turn ON the TFT display backlight

```bash
    python3 -c "import lgpio; h=lgpio.gpiochip_open(0); lgpio.gpio_claim_output(h,9); lgpio.gpio_write(h,9,1); lgpio.gpiochip_close(h)"
```

### Turn OFF the TFT display backlight

```bash
    python3 -c "import lgpio; h=lgpio.gpiochip_open(0); lgpio.gpio_claim_output(h,9); lgpio.gpio_write(h,9,0); lgpio.gpiochip_close(h)"
```

### Display a static image

Prepare a 240x320 pixel image and run:

```bash
    python3 st7789v_display.py my_image.jpg
```
	
![Display static SlackPunk test image](https://sairpi.penthux.net/img/jaffaworks/maia_slackpunk_display.jpg "Display static SlackPunk test image")

### Display Raspberry Pi 5 system status on-the-fly

```bash
    python3 rpi_system_stats.py &
```
	
![RPi 5 System Stats Display](https://sairpi.penthux.net/img/jaffaworks/maia_system_stats_display.jpg "RPi 5 System Stats Display?v=2")

### Run Matrix-style digital rain generator script

```bash
    python3 matrix_digital_rain.py &
```

![Matrix-style Digital Rain](https://sairpi.penthux.net/img/jaffaworks/maia_matrix_digital_rain.jpg "Matrix-style Digital Rain")

## Script Notes

**NB:** Complete notes are in the script headers. The scripts are also well commented in the code to make it easy for editing and personal adjustments.

### st7789v_display.py

- loads an image from the command line
- resizes it to 240x320
- converts it to RGB565
- sends the image to the TFT module display buffer over SPI

### rpi_system_stats.py

- displays running system statistics
- stats include; hostname, system IP, uptime, load, SoC thermals, RAM and disk used/total percentages
- includes current rolling timestamp (YYYY-MM-DD hh:mm:ss format)
- includes configurable SPI speed
- includes configurable setting for how often the display refreshes (minimum 0.1 seconds)
- includes configurable background, text, and line separator colours
- includes configurable font setting

### matrix_digital_rain.py

- renders an animated Matrix-style digital rain effect
- supports optional text at top of screen (max 24 chars per line)
- supports optional timestamp display
- includes configurable colours, intensity, and FPS

## Configuration

All scripts are configured for:

- resolution: 240x320
- SPI bus: 0
- SPI device: 0
- DC pin: GPIO25
- RST pin: GPIO24

Default SPI speed:

    20000000 (20 MHz)

**NB:** If you see instability or image rendering issues/distortion, try lowering SPI speed.

## Run at Boot

The image used for testing the `st7789v_display.py` script: https://raw.githubusercontent.com/SAIRPi/st7789v-rpi/main/slackpunk.jpg

**NB:** use your own PATHs and images, of course.

Example entries in /etc/rc.d/rc.local:

```bash
    /usr/bin/python3 /root/tft/st7789v_display.py /root/tft/slackpunk.jpg &
	
	/usr/bin/python3 /root/tft/rpi_system_stats.py & 
	
    /usr/bin/python3 /root/tft/matrix_digital_rain.py &
```

Example entries in crontab:

```bash
    @reboot /usr/bin/python3 /root/tft/st7789v_display.py /root/tft/slackpunk.jpg &
	
	@reboot /usr/bin/python3 /root/tft/rpi_system_stats.py &
	
    @reboot /usr/bin/python3 /root/tft/matrix_digital_rain.py &
```

## Notes On ST7789V GMT020-02-8P display behaviour

### The `rpi_system_stats.py` script

The `rpi_system_stats.py` implementation is specifically optimised for Raspberry Pi 5 architecture running on arm-based Slackware Linux operating systems.

- Unlike previous models, the Raspberry Pi 5 uses the RP1 southbridge (I/O controller) to manage GPIO via a PCI Express link, and is not directly mapped to memory as in earlier versions. This means older direct register-access libraries won't work. The `rpi_system_stats.py` script uses the lgpio library to dynamically detect the correct hardware chip (typically gpiochip15), preventing the "Bad GPIO" errors common with older libraries such as RPi.GPIO.

- The code includes specific ST7789V controller initialisation offsets for the GMT020-02-8P TFT module to prevent image drifting or scrolling issues caused by internal memory byte misalignment.

- Default font paths are configured for traditional Slackware /usr/share/fonts/TTF/ locations.

### Static image uploads

When using `st7789v_display.py`, the image is sent to the ST7789V display framebuffer as a one-time data transfer.

After the image has been uploaded:

- it remains visible on the screen
- it is not continuously refreshed by the script
- it will stay displayed until another image is sent to the display, the display contents are changed by another program, or power is removed from the module

In other words, once the image has been written to the display, it will remain - even though the `st7789v_display.py` script exits cleanly.

It's possible to upload a blank image to make the screen appears as if it's not displaying anything. Or the TFT module backlight can be set to OFF, which will also make the screen appear as if no images are loaded into the memory buffer.

### Non-static image uploads

With `rpi_system_stats.py` and `matrix_digital_rain.py` scripts - these *are* static images, per se, but they are refreshed at a very rapid rate (approx. 16 FPS ceiling at 20 MHz) giving the illusion that it's *streaming video*. When these scripts are exited (i.e. CTRL+C) the screen will freeze but still display the last frame in the buffer - until the backlight is turned OFF or host system power is cut. The display will not continue to show updated content because the scripts are no longer driving that process. Both the `rpi_system_stats.py` and `matrix_digital_rain.py` scripts can be run as background processes, allowing you to keep your terminal free while ensuring the process continues uninterrupted.

### Important note on the ST7789V display's power status

The display backlight will automatically turn off once the host system is rebooted or poweroff/shutdown command is used. However, this is just the backlight. If the TFT module itself is still receiving power any image in the memory buffer will remain.

Only when all power to the display module is cut will images be purged from the TFT module memory buffer.

## License

Released under the MIT License.

## Credits

[SAIRPi Project](https://sairpi.penthux.net)

Featured Raspberry Pi cases are hand-made in the UK by [Ideas Universe](https://www.ebay.co.uk/usr/car_36724)
