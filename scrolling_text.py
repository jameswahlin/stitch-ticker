#!/usr/bin/env python

import colorsys
import signal
import time
from sys import exit

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    exit("This script requires the pillow module\nInstall with: sudo pip install pillow")

import unicornhathd

def display_text(lines, colors):

    # Use `fc-list` to show a list of installed fonts on your system,
    # or `ls /usr/share/fonts/` and explore.

    FONT = ("/usr/share/fonts/truetype/freefont/FreeSansBold.ttf", 12)

    # sudo apt install fonts-droid
    #FONT = ("/usr/share/fonts/truetype/droid/DroidSans.ttf", 12)

    # sudo apt install fonts-roboto
    #FONT = ("/usr/share/fonts/truetype/roboto/Roboto-Bold.ttf", 10)

    unicornhathd.rotation(0)
    unicornhathd.brightness(1.0)


    width, height = unicornhathd.get_shape()

    text_x = width
    text_y = 2


    font_file, font_size = FONT

    font = ImageFont.truetype(font_file, font_size)

    text_width, text_height = width, 0

    for line in lines:
        w, h = font.getsize(line)
        text_width += w + width
        text_height = max(text_height,h)

    text_width += width + text_x + 1

    image = Image.new("RGB", (text_width,max(16, text_height)), (0,0,0))
    draw = ImageDraw.Draw(image)

    offset_left = 0

    for index, line in enumerate(lines):
        draw.text((text_x + offset_left, text_y), line, colors[index], font=font)

        offset_left += font.getsize(line)[0] + width

    for scroll in range(text_width - width):
        for x in range(width):
            for y in range(height):
                pixel = image.getpixel((x+scroll, y))
                r, g, b = [int(n) for n in pixel]
                unicornhathd.set_pixel(width-1-x, y, r, g, b)

        unicornhathd.show()
        time.sleep(0.02)

    unicornhathd.off()

# lines = ["NASDAQ:MDB", "32.11", "20999"]

# colors = [(255, 255, 255), (0, 255, 0), (255, 255, 255)]

# display_text(lines, colors)

