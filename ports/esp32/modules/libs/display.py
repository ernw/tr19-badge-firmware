# This file is part of the Troopers 19 Badge project, https://troopers.de/troopers19/
#
# The BSD 3-Clause License
#
# Copyright (c) 2019 "Malte Heinzelmann" <malte@hnzlmnn.de>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import display
import utime

from machine import Pin, SPI
from micropython import const

EPD_WIDTH  = const(128)
EPD_HEIGHT = const(296)

class Display:

    # 0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~
    default_rotation = display.ROTATE_90
    default_font = display.FONT_DEJAVU_12
    default_inverted = True

    def __init__(self):
        self.spi = SPI(1, baudrate=20000000, bits=8, polarity=0, phase=0, sck=Pin(18), mosi=Pin(23), miso=Pin(5))
        self.spi.init()
        cs = Pin(25)
        dc = Pin(27)
        rst = Pin(0)
        busy = Pin(13)

        cs.init(cs.OUT, value=1)
        dc.init(dc.OUT, value=0)
        rst.init(rst.OUT, value=0)
        busy.init(busy.IN)

        self.buffer = bytearray(EPD_WIDTH // 8 * EPD_HEIGHT)
        self.display = display.Display(self.buffer, self.spi, 128, 296,
                            rst=rst,
                            dc=dc,
                            cs=cs,
                            busy=busy,
                            rotation=self.default_rotation,
                            partial=True,
                            invert=self.default_inverted,
                            font=self.default_font,
        )

        self.display.init()

    def close(self):
        self.spi.deinit()

    @property
    def width(self):
        if self.display.rotation() in [display.ROTATE_90, display.ROTATE_270]:
            return EPD_HEIGHT
        return EPD_WIDTH

    @property
    def height(self):
        if self.display.rotation() in [display.ROTATE_90, display.ROTATE_270]:
            return EPD_WIDTH
        return EPD_HEIGHT

    @property
    def fontSize(self):
        size = display.fontSize(self.display.font())
        return (0, 0) if size is None else size

    @property
    def lines(self):
        return self.height // self.fontSize[1]

    @property
    def chars(self):
        return self.width // self.fontSize[0]

    def test(self):
        self.fill(display.BACKGROUND)
        y = 0
        # y += self.text('Hello World', 0, 0)[0]
        # self.update()
        # self.line(0, 0, self.width, self.height)
        # self.update()
        # self.hline(self.width // 4, self.height // 2, self.width // 2)
        # self.update()
        # self.vline(self.width // 2, self.height // 4, self.height // 2)
        # self.update()
        # self.rect(self.width - 40, self.height - 40, self.width, self.height)
        # self.update()
        # self.fill_rect(self.width - 40, 0, self.width, 40)
        # self.update()
        # self.pixel(self.width - 20, 20, display.BACKGROUND)
        # self.update()
        for font in [
            display.FONT_DEJAVU_8,
            display.FONT_DEJAVU_12,
            display.FONT_DEJAVU_16,
            display.FONT_DEJAVUEMOJI_16,
        ]:
            self.font(font)
            y += self.text(b'Test \x81\x82\x84\x85', 0, y=y)['height']
        self.update()
        # c = -8 * self.fontSize[0]
        # for char in range(32, 127):
        #     line = (char - 32) % (self.lines - 1)
        #     if line is 0:
        #         c += 8 * self.fontSize[0]
        #     self.text("0x{0:02X} {1}".format(char, chr(char)), c, line=line + 1)
        self.font(display.FONT_DEJAVU_12)
        y += self.text("This is a new\nline test", 50, y=y, wrap=display.WRAP_INDENT)['height']
        self.font(display.FONT_LOGOS_32)
        self.text("ABCDE", 128, y=0)
        self.update()

        utime.sleep(2)

    def clear(self):
        self.display.clear(display.BACKGROUND)

    def reset(self):
        self.display.font(self.default_font)
        self.display.inverted(self.default_inverted)
        self.display.inverted(self.default_rotation)

    def update(self):
        self.display.update()

    def font(self, font=None):
        if font is None:
            return self.display.font()
        self.display.font(font)

    def rotation(self, rotation=None, update=False):
        if rotation is None:
            return self.display.rotation()
        self.display.rotation(rotation)
        if update:
            self.update()

    def inverted(self, inverted=None, update=False):
        if inverted is None:
            return self.display.inverted()
        self.display.inverted(inverted)
        if update:
            self.update()

    def invert(self, update=False):
        self.display.invert()
        if update:
            self.update()

    def pixel(self, x=0, y=0, color=None, update=False):
        if color is None:
            self.display.pixel(x, y)
        else:
            self.display.pixel(x, y, color)
        if update:
            self.update()

    def fill(self, color=None, update=False):
        if color is None:
            self.display.fill()
        else:
            self.display.fill(color)

        if update:
            self.update()

    def text(self, text, x, line=None, y=None, color=None, wrap=display.NO_WRAP, max_width=0, update=False):
        if not text:
            return {
                'width': 0,
                'columns': 0,
                'height': 0,
                'rows': 0,
            }
        if line is not None:
            y = line * self.fontSize[1]
        if y is None:
            return {
                'width': 0,
                'columns': 0,
                'height': 0,
                'rows': 0,
            }
        if color is None:
            color = display.BLACK
        if wrap not in [display.NO_WRAP, display.WRAP_INDENT, display.WRAP_LINE_START]:
            wrap = display.NO_WRAP
        w, h = self.display.text(x, y, text, color, wrap, max_width)
        if update:
            self.update()
        return {
            'width': w,
            'columns': w // self.fontSize[0],
            'height': h,
            'rows': h // self.fontSize[1],
        }

    def line(self, x0, y0, x1, y1, color=None, update=False):
        self.display.line(x0, y0, x1, y1, color)
        if update:
            self.update()

    def hline(self, x, y, width, color=None, update=False):
        self.display.hline(x, y, width, color)
        if update:
            self.update()

    def vline(self, x, y, height, color=None, update=False):
        self.display.vline(x, y, height, color)
        if update:
            self.update()

    def rect(self, x0, y0, x1, y1, color=None, update=False):
        self.display.rect(x0, y0, x1, y1, color)
        if update:
            self.update()

    def fill_rect(self, x0, y0, x1, y1, color=None, update=False):
        self.display.fill_rect(x0, y0, x1, y1, color)
        if update:
            self.update()

    def circ(self, x, y, radius, color=None, update=False):
        self.display.circ(x, y, radius, color)
        if update:
            self.update()

    def fill_circ(self, x, y, radius, color=None, update=False):
        self.display.fill_circ(x, y, radius, color)
        if update:
            self.update()

    def arc(self, x, y, radius, start=None, end=None, border=None, color=None, update=False):
        self.display.arc(x, y, start, end, radius, border, color)
        if update:
            self.update()

    def fill_arc(self, x, y, radius, start=None, end=None, color=None, update=False):
        self.display.fill_arc(x, y, radius, start, end, color)
        if update:
            self.update()

    def image(self, buffer, x=0, y=0, width=None, height=None, update=False):
        if not width:
            width = self.width
        if not height:
            height = self.height
        if type(buffer) is str:
            self.display.fill_b64(buffer, x, y, width, height)
        else:
            self.display.fill_bytes(buffer, x, y, width, height)
        if update:
            self.update()

