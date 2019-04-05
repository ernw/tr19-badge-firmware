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
from system import app, screen, Input, Kernel


class TestScreen(screen.Screen):

    TO_TEST = [
        # Input
        Input.BTN_START,
        Input.BTN_UP,
        Input.KEY_P,
        Input.KEY_Q,
        # Lights
        ((0, 1, 2), ((255, 0, 0), (0, 255, 0), (0, 0, 255))),
        ((3, 4, 5), ((255, 0, 0), (0, 255, 0), (0, 0, 255))),
        # Accelerometer
        0x19,
    ]
    CURRENT_TEST = 0
    TESTS_INPUT = 4
    TESTS_LIGHT = TESTS_INPUT + 2
    TESTS_ACCEL = TESTS_LIGHT + 1

    def _color(self, color):
        if color == (255, 0, 0):
            return 'red'
        if color == (0, 255, 0):
            return 'green'
        if color == (0, 0, 255):
            return 'blue'
        return str(color)

    def register(self):
        self.events.on('input', self.test_input)
        self.display.font(display.FONT_DEJAVU_12)
        self.display.fill(display.BACKGROUND)

    def update(self, delta=0):
        # This screen should be used to test all functions of the badge
        if self.CURRENT_TEST < self.TESTS_INPUT:
            self.display.text("Enter {}".format(Input.key_name(self.TO_TEST[self.CURRENT_TEST])), 0, line=self.CURRENT_TEST,
                              wrap=display.WRAP_INDENT)
        elif self.CURRENT_TEST < self.TESTS_LIGHT:
            for i in range(len(self.TO_TEST[self.CURRENT_TEST][0])):
                self.lights.set(self.TO_TEST[self.CURRENT_TEST][1][i], lights=self.TO_TEST[self.CURRENT_TEST][0][i])
            self.display.text("LEDs {} colors {}?".format(
                ', '.join(str(i + 1) for i in self.TO_TEST[self.CURRENT_TEST][0]),
                ', '.join(self._color(c) for c in self.TO_TEST[self.CURRENT_TEST][1]),
            ), 0, line=self.CURRENT_TEST, wrap=display.WRAP_INDENT)
        elif self.CURRENT_TEST < self.TESTS_ACCEL:
            a = self.accel.acceleration
            self.display.text("Accelerometer ok? x={0:.2f} y={1:.2f} z={2:.2f}".format(a.x, a.y, a.z), 0, line=self.CURRENT_TEST, wrap=display.WRAP_INDENT)
        else:
            self.display.text("Done!\nPlease switch off the badge using\nthe power switch on the back...", 0, line=self.CURRENT_TEST, wrap=display.WRAP_INDENT)
        self.display.update()
        return None

    def test_input(self, event):
        if self.CURRENT_TEST < self.TESTS_INPUT:
            if event.type is Input.UP and event.code is self.TO_TEST[self.CURRENT_TEST]:
                print('Test ok')
                self.display.text("ok", self.display.width - 2 * self.display.fontSize[0],
                                  line=self.CURRENT_TEST, wrap=display.WRAP_INDENT, update=True)
                self.CURRENT_TEST += 1
                return Kernel.ACTION_RELOAD
            print('Wrong input detected')
        elif self.CURRENT_TEST < self.TESTS_LIGHT:
            if event.type is Input.UP and event.code is Input.BTN_A:
                print('Test ok')
                self.display.text("ok", self.display.width - 2 * self.display.fontSize[0],
                                  line=self.CURRENT_TEST, wrap=display.WRAP_INDENT, update=True)
                self.CURRENT_TEST += 1
                return Kernel.ACTION_RELOAD
        elif self.CURRENT_TEST < self.TESTS_ACCEL:
            if event.type is Input.UP and event.code is Input.BTN_A:
                print('Test ok')
                self.display.text("ok", self.display.width - 2 * self.display.fontSize[0],
                                  line=self.CURRENT_TEST, wrap=display.WRAP_INDENT, update=True)
                self.CURRENT_TEST += 1
                return Kernel.ACTION_RELOAD
            return Kernel.ACTION_RELOAD



class App(app.App):

    VERSION = 1

    screens = [
        TestScreen(disable_back=True),
    ]




