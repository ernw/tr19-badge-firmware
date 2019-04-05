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

from machine import Pin
import neopixel
from esp import neopixel_write


class Light:
    np = None

    def __init__(self, count=6, bpp=3, brightness=.1, pin=Pin(22)):
        self.count = count
        self.pin = pin
        self.bpp = bpp
        self._brightness = brightness
        self.init(self.count)

    def init(self, count):
        self.np = neopixel.NeoPixel(self.pin, count, bpp=self.bpp)
        self.pin.init(Pin.OPEN_DRAIN)

    def update(self):
        neopixel_write(self.np.pin, self.buf, self.np.timing)

    @property
    def buf(self):
        return bytearray([int(i * self._brightness) for i in self.np.buf])

    def brightness(self, brightness=None, update=True):
        if brightness is not None:
            self._brightness = min(1, max(0, brightness))
            if update:
                self.update()
        return self._brightness

    def set(self, color=None, lights=None, update=True):
        if lights is None:
            lights = list(range(self.count))
        if type(lights) is not list:
            lights = [lights]
        default = (0,) * self.bpp
        if not color:
            color = default
        if type(color) is not tuple:
            color = default
        if len(color) < self.bpp:
            color = default
        color = color[:self.bpp]
        for i in lights:
            i = max(0, min(self.count - 1, int(i)))
            self.np[i] = tuple([int(c) for c in color[:self.bpp]])
        if update:
            self.update()

    def off(self, lights=None, update=True):
        if lights is None:
            lights = list(range(self.count))
        self.set((0,) * self.bpp, lights, update)

    def white(self, lights=None, update=True):
        if lights is None:
            lights = list(range(self.count))
        self.set((255,) * self.bpp, lights, update)

    def troopers(self, lights=None, update=True):
        if lights is None:
            lights = list(range(self.count))
        brightness = self.brightness()
        self.brightness(.2, update=False)
        self.set((214, 113, 12), lights, update)
        self.brightness(brightness, update=False)

    def wheel(self, pos):
        """Generate rainbow colors across 0-255 positions."""
        if pos < 85:
            return pos * 3, 255 - pos * 3, 0
        elif pos < 170:
            pos -= 85
            return 255 - pos * 3, 0, pos * 3
        else:
            pos -= 170
            return 0, pos * 3, 255 - pos * 3

    def rainbow(self, state=None, direction=None):
        if state is None:
            state = (0, 1) # Marks the start of the LED
        if direction is not None:
            state = (state[0], int(direction))
        for i in range(self.count):
            self.set(self.wheel(int(i * 256 / self.count)), lights=(i + state[0]) % self.count)
        return (state[0] + state[1]) % self.count, state[1]


