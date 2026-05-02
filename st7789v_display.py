#!/usr/bin/env python3
#
# Python script for TFT module 240x320 ST7789V GMT020-02-8P display
#
# Display a static image on TFT display
#
# Exaga - 2026-04-19 - SAIRPi Project - https://sairpi.penthux.net
#
# This scripts uses Python library **lgpio** to probe the Raspberry Pi 5's RP1
# controller and will not work on previous Raspberry Pi versions.
#
# v2.1 uses a two-stage search to find the correct GPIO interface, 
# regardless of how the Linux system numbers them.
#
###
#
# TFT MODULE CONFIG:
# This script is intended for 2 inch TFT module 240x320 ST7789V GMT020-02-8P 
# 8-pin variant (with separate backlight header connector):
# https://goldenmorninglcd.com/tft-display-module/2-inch-240x320-st7789v-gmt020-02/
#
# It may work on other non-touch TFT modules, but no guarantees!
#
# ST7789V module wiring on Raspberry Pi 40-pin GPIO header:
#
# BL  - pin 21 (GPIO9)
# CS  - pin 24 (GPIO8)
# DC  - pin 22 (GPIO25)
# RST - pin 18 (GPIO24)
# SDA - pin 19 (GPIO10)
# SCL - pin 23 (GPIO11)
# VCC - pin 17 (3v3)
# GND - pin 20 (Ground)
#
###
#
# USAGE:
# First install the required Python libraries:
#
#   python3 -m pip install --upgrade pillow spidev numpy lgpio rpi-lgpio
#
# Then run this script while referencing the image:
#
#   python3 /root/.tft/st7789v_display.py /root/.tft/jaffaworks_logo.png
#
# NB: Use your own PATHs, of course.
#
# To turn ON the TFT display BACKLIGHT:
#
#    python3 -c "import lgpio; h=lgpio.gpiochip_open(0); \
#    lgpio.gpio_claim_output(h,9); lgpio.gpio_write(h,9,1); \
#    lgpio.gpiochip_close(h)"
#
# To turn OFF the TFT display BACKLIGHT:
#
#    python3 -c "import lgpio; h=lgpio.gpiochip_open(0); \ 
#    lgpio.gpio_claim_output(h,9); lgpio.gpio_write(h,9,0); \
#    lgpio.gpiochip_close(h)" 
#
###
#
# LICENCE:
# This script is released under the MIT License.
# You are free to use, copy, modify, merge, publish, distribute, sublicense, 
# and/or sell copies of this software, subject to the terms of the MIT License.
# If you reuse this work, retain the original copyright notice and license text.
#
# Copyright (c) 2026 sairpi.penthux.net
#
# Permission is hereby granted, free of charge, to any person obtaining a 
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation 
# the rights to use, copy, modify, merge, publish, distribute, sublicense, 
# and/or sell copies of the Software, and to permit persons to whom the 
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in 
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL 
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING 
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#
###


import sys
import time
import os
import spidev
import lgpio
from PIL import Image

# Display resolution
WIDTH = 240
HEIGHT = 320

# GPIO pin assignments (BCM numbering)
DC = 25
RST = 24
BL = 9

# SPI config - Bus 0, Device 0, SPI Speed
SPI_BUS = 0
SPI_DEV = 0
SPI_SPEED = 20000000  # 40 MHz SPI speed (lower this if you have issues)

def get_gpio_handle():
    # 1. Find RP1 chip by label
    sys_path = '/sys/class/gpio'
    if os.path.exists(sys_path):
        for chip in os.listdir(sys_path):
            if chip.startswith('chip'):
                try:
                    with open(f"{sys_path}/{chip}/label", "r") as f:
                        if "rp1" in f.read().lower():
                            idx = int(chip.replace('chip', ''))
                            return lgpio.gpiochip_open(idx), idx
                except:
                    continue

    # 2. Fallback: brute force /dev/gpiochip nodes
    test_range = list(range(16)) + [569]
    for idx in reversed(test_range):
        dev_node = f"/dev/gpiochip{idx}"
        if os.path.exists(dev_node):
            try:
                handle = lgpio.gpiochip_open(idx)
                return handle, idx
            except:
                continue

    return None, None

# Attempt to get a valid hardware handle
h, CHIP_ID = get_gpio_handle()

if h is None:
    print("CRITICAL ERROR: No functional GPIO chip found in /dev/ or /sys/.")
    sys.exit(1)

def gpio_out(pin, value):
    lgpio.gpio_write(h, pin, value)

# Claim Pins
claimed = False
for attempt in range(10):
    try:
        lgpio.gpio_claim_output(h, DC)
        lgpio.gpio_claim_output(h, RST)
        lgpio.gpio_claim_output(h, BL)
        claimed = True
        break
    except Exception as e:
        last_error = e
        try: lgpio.gpio_free(h, DC)
        except: pass
        try: lgpio.gpio_free(h, RST)
        except: pass
        try: lgpio.gpio_free(h, BL)
        except: pass
        if attempt < 9:
            time.sleep(0.2)
if not claimed:
    print(f"CRITICAL ERROR: Pins {DC}/{RST}/{BL} busy on chip {CHIP_ID}. {last_error}")
    lgpio.gpiochip_close(h)
    sys.exit(1)

def cmd(spi, value):
    gpio_out(DC, 0)
    spi.writebytes([value & 0xFF])

def data(spi, values):
    gpio_out(DC, 1)
    if isinstance(values, int):
        spi.writebytes([values & 0xFF])
    else:
        chunk = 4096
        for i in range(0, len(values), chunk):
            spi.writebytes(values[i:i+chunk])

def reset():
    gpio_out(RST, 1)
    time.sleep(0.05)
    gpio_out(RST, 0)
    time.sleep(0.05)
    gpio_out(RST, 1)
    time.sleep(0.15)

def set_window(spi, x0, y0, x1, y1):
    cmd(spi, 0x2A)
    data(spi, [x0 >> 8, x0 & 0xFF, x1 >> 8, x1 & 0xFF])
    cmd(spi, 0x2B)
    data(spi, [y0 >> 8, y0 & 0xFF, y1 >> 8, y1 & 0xFF])
    cmd(spi, 0x2C)

def init_display(spi):
    reset()
    cmd(spi, 0x36); data(spi, 0x00)
    cmd(spi, 0x3A); data(spi, 0x05)
    cmd(spi, 0x21)
    cmd(spi, 0x11)
    time.sleep(0.12)
    cmd(spi, 0x29)
    time.sleep(0.05)

def image_to_rgb565_bytes(img):
    img = img.convert("RGB")
    out = bytearray()
    
    # Convert image to RGB565 byte format
    pixels = list(img.getdata()) # NB: will be deprecated in pillow 14!
    # pixels = list(img.get_flattened_data()) # use this instead on latest pillow version 
    
    for r, g, b in pixels:
        # Convert 24-bit RGB to 16-bit RGB565
        value = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
        out.append((value >> 8) & 0xFF)
        out.append(value & 0xFF)

    return out

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} IMAGE")
        sys.exit(1)

    spi = spidev.SpiDev()
    spi.open(SPI_BUS, SPI_DEV)
    spi.max_speed_hz = SPI_SPEED
    spi.mode = 0

    try:
        init_display(spi)
        gpio_out(BL, 1)
        img_path = sys.argv[1]
        if not os.path.exists(img_path):
            print(f"Error: {img_path} not found.")
            sys.exit(1)

        img = Image.open(img_path).resize((WIDTH, HEIGHT))
        fb = image_to_rgb565_bytes(img)
        set_window(spi, 0, 0, WIDTH - 1, HEIGHT - 1)
        data(spi, fb)
        print(f"Success: TFT display updated using /dev/gpiochip{CHIP_ID}")

    except Exception as e:
        print(f"Runtime Error: {e}")
    finally:
        spi.close()
        lgpio.gpiochip_close(h)

if __name__ == "__main__":
    main()

# EOF<*>
