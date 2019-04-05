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
from libs import PCA9539A, PCA9555
from system import Event
import utime
from machine import SPI, Pin, I2C


class Input:

    UP = 0
    DOWN = 1

    BTN_START = 0x01
    BTN_SELECT = 0x02
    BTN_UP = 0x03
    BTN_DOWN = 0x04
    BTN_LEFT = 0x05
    BTN_RIGHT = 0x06
    BTN_A = 0x07
    BTN_B = 0x08

    KEY_A = 0x10
    KEY_B = 0x11
    KEY_C = 0x12
    KEY_D = 0x13
    KEY_E = 0x14
    KEY_F = 0x15
    KEY_G = 0x16
    KEY_H = 0x17
    KEY_I = 0x18
    KEY_J = 0x19
    KEY_K = 0x1A
    KEY_L = 0x1B
    KEY_M = 0x1C
    KEY_N = 0x1D
    KEY_O = 0x1E
    KEY_P = 0x1F
    KEY_Q = 0x20
    KEY_R = 0x21
    KEY_S = 0x22
    KEY_T = 0x23
    KEY_U = 0x24
    KEY_V = 0x25
    KEY_W = 0x26
    KEY_X = 0x27
    KEY_Y = 0x28
    KEY_Z = 0x29
    KEY_SPACE = 0x2A

    KEY_FN = 0x30
    KEY_SHIFT = 0x31
    KEY_SHIELD = 0x32

    KEY_BACKSPACE = 0x40
    KEY_RETURN = 0x41

    MODE_DEFAULT = 0
    MODE_TEXT = 1

    NAME = {
        BTN_START: 'start',
        BTN_SELECT: 'select',
        BTN_UP: 'up',
        BTN_DOWN: 'down',
        BTN_LEFT: 'left',
        BTN_RIGHT: 'right',
        BTN_A: 'a',
        BTN_B: 'b',
        KEY_A: 'a',
        KEY_B: 'b',
        KEY_C: 'c',
        KEY_D: 'd',
        KEY_E: 'e',
        KEY_F: 'f',
        KEY_G: 'g',
        KEY_H: 'h',
        KEY_I: 'i',
        KEY_J: 'j',
        KEY_K: 'k',
        KEY_L: 'l',
        KEY_M: 'm',
        KEY_N: 'n',
        KEY_O: 'o',
        KEY_P: 'p',
        KEY_Q: 'q',
        KEY_R: 'r',
        KEY_S: 's',
        KEY_T: 't',
        KEY_U: 'u',
        KEY_V: 'v',
        KEY_W: 'w',
        KEY_X: 'x',
        KEY_Y: 'y',
        KEY_Z: 'z',
        KEY_SPACE: 'space',
        KEY_FN: 'fn',
        KEY_SHIFT: 'shift',
        KEY_SHIELD: 'shield',
        KEY_BACKSPACE: 'back',
        KEY_RETURN: 'return',
    }

    # Mappings (default, shift, shield, fn)
    MAPPING = {
        KEY_A: ('a', 'A', None, None),
        KEY_B: ('b', 'B', ',', '<'),
        KEY_C: ('c', 'C', '-', '_'),
        KEY_D: ('d', 'D', None, None),
        KEY_E: ('e', 'E', '3', '#'),
        KEY_F: ('f', 'F', None, None),
        KEY_G: ('g', 'G', ';', ':'),
        KEY_H: ('h', 'H', '\'', '"'),
        KEY_I: ('i', 'I', '8', '*'),
        KEY_J: ('j', 'J', '[', '{'),
        KEY_K: ('k', 'K', ']', '}'),
        KEY_L: ('l', 'L', '\\', '|'),
        KEY_M: ('m', 'M', '/', '?'),
        KEY_N: ('n', 'N', '.', '>'),
        KEY_O: ('o', 'O', '9', '('),
        KEY_P: ('p', 'P', '0', ')'),
        KEY_Q: ('q', 'Q', '1', '!'),
        KEY_R: ('r', 'R', '4', '$'),
        KEY_S: ('s', 'S', None, None),
        KEY_T: ('t', 'T', '5', '%'),
        KEY_U: ('u', 'U', '7', '&'),
        KEY_V: ('v', 'V', '=', '+'),
        KEY_W: ('w', 'W', '2', '@'),
        KEY_X: ('x', 'X', None, None),
        KEY_Y: ('y', 'Y', '6', '^'),
        KEY_Z: ('z', 'Z', None, None),
        KEY_SPACE: (' ', None, None, None),
        KEY_RETURN: ('\n', None, None, None),
    }

    MODIFIERS = {
        KEY_FN: False,
        KEY_SHIFT: False,
        KEY_SHIELD: False,
    }

    KONAMI_COUNTER = 0
    KONAMI_CODE = [
        BTN_UP,
        BTN_UP,
        BTN_DOWN,
        BTN_DOWN,
        BTN_LEFT,
        BTN_RIGHT,
        BTN_LEFT,
        BTN_RIGHT,
        BTN_B,
        BTN_A,
    ]

    HNZLMNN_COUNTER = 0
    HNZLMNN_CODE = [
        KEY_H,
        KEY_N,
        KEY_Z,
        KEY_L,
        KEY_M,
        KEY_N,
        KEY_N,
        KEY_RETURN,
    ]

    CYBAER_COUNTER = 0
    CYBAER_CODE = [
        BTN_LEFT,
        BTN_RIGHT,
        BTN_LEFT,
        BTN_RIGHT,
        BTN_B,
        BTN_B,
        BTN_START,
    ]

    NAHUEL_COUNTER = 0
    NAHUEL_CODE = [
        KEY_N,
        KEY_A,
        KEY_H,
        KEY_U,
        KEY_E,
        KEY_L,
    ]


    def __init__(self, kernel):
        self.kernel = kernel
        self.events = kernel.events
        self.screen = None
        self._mode = self.MODE_DEFAULT
        self.i2c = I2C(scl=Pin(5), sda=Pin(4), freq=400000)
        self.ioConsole = PCA9539A(self, self.i2c, 0x77, [
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            Input.BTN_START, Input.BTN_B, Input.BTN_A, Input.BTN_SELECT, Input.BTN_UP, Input.BTN_RIGHT, Input.BTN_LEFT, Input.BTN_DOWN,
        ], Pin(39), self.on_input, wakeup=True)
        try:
            self.ioConsole.init()
        except OSError:
            kernel.logger.error('I2C Expander 1 Error')
            kernel.lights.set((255, 0, 0), 0)
        self.ioKeyboard0 = PCA9555(self, self.i2c, 0x25, [
            Input.KEY_G, Input.KEY_B, Input.KEY_H, Input.KEY_RETURN, Input.KEY_M, Input.KEY_N, Input.KEY_SHIFT, Input.KEY_BACKSPACE,
            Input.KEY_J, Input.KEY_K, Input.KEY_L, Input.KEY_Y, Input.KEY_U, Input.KEY_I, Input.KEY_O, Input.KEY_P,
        ], Pin(35), self.on_input)
        try:
            self.ioKeyboard0.init()
        except OSError:
            kernel.logger.error('I2C Expander 2 Error')
            kernel.lights.set((255, 0, 0), 1)
        self.ioKeyboard1 = PCA9555(self, self.i2c, 0x24, [
            Input.KEY_Q, Input.KEY_A, Input.KEY_Z, Input.KEY_SHIELD, Input.KEY_W, Input.KEY_S, Input.KEY_X, Input.KEY_FN,
            Input.KEY_T, Input.KEY_V, Input.KEY_F, Input.KEY_R, Input.KEY_SPACE, Input.KEY_C, Input.KEY_D, Input.KEY_E,
        ], Pin(34), self.on_input)
        try:
            self.ioKeyboard1.init()
        except OSError:
            kernel.logger.error('I2C Expander 3 Error')
            kernel.lights.set((255, 0, 0), 2)
        self.caps = False
        self.text = None
        self.context = None
        self.title = ''
        self.title_wrap = False
        self.max_len = None

    def resolve_key(self, key):
        if self.KEY_A <= key <= self.KEY_SPACE or key is self.KEY_RETURN:
            i = 0
            if self.MODIFIERS[self.KEY_SHIFT]:
                # i += 1
                i = 1
            if self.MODIFIERS[self.KEY_SHIELD]:
                # i += 2
                i = 2
            if self.MODIFIERS[self.KEY_FN]:
                i = 3
            mapping = self.MAPPING[key][i]
            if mapping is None:
                return self.MAPPING[key][0]
            return mapping
        return key

    @staticmethod
    def key_name(key):
        if key < Input.KEY_A:
            prefix = 'console'
        elif key < Input.KEY_FN:
            prefix = 'char'
        elif key < Input.KEY_BACKSPACE:
            prefix = 'mod'
        else:
            prefix = 'ctrl'
        name = Input.NAME.get(key, None)
        if name is None:
            return None
        return '{}.{}'.format(prefix, name)

    def mode(self, mode=None):
        if mode is not None:
            if mode is not self._mode:
                for key in self.MODIFIERS.keys():
                    self.MODIFIERS[key] = False
            self._mode = mode
        return self._mode

    def update_lights(self):
        if self.mode() is not self.MODE_TEXT:
            return
        self.kernel.lights.off([0, 1, 5])
        if self.MODIFIERS[self.KEY_FN]:
            self.kernel.lights.set((0, 0, 255), 1)
        if self.MODIFIERS[self.KEY_SHIFT]:
            self.kernel.lights.set((0, 0, 255), 5)
        if self.MODIFIERS[self.KEY_SHIELD]:
            self.kernel.lights.set((0, 0, 255), 0)

    def on_input(self, type, key):
        if self.KEY_FN <= key <= self.KEY_SHIELD:
            self.MODIFIERS[key] = False if type is self.UP else True
            if self.KEY_FN < key:
                # If fn is pressed while we experience a 'up' on another modifier key don't unset it
                if self.MODIFIERS[self.KEY_FN] and type is self.UP:
                    self.MODIFIERS[key] = True
            self.update_lights()
        # TODO: Should modifier keys trigger an event?
        name = self.key_name(key)
        if name is None:
            return
        if self.mode() is self.MODE_TEXT:
            if type is self.DOWN:
                return
            if key is self.BTN_B:
                self.mode(self.MODE_DEFAULT)
                return self.events.emit(Event('input.text', data=dict(context=self.context, value=None)))
            if key is self.BTN_A:
                self.mode(self.MODE_DEFAULT)
                return self.events.emit(Event('input.text', data=dict(context=self.context, value=self.text)))
            self.events.emit(Event('input.char', data=dict(
                type=type,
                code=key,
                key=self.resolve_key(key),
                ctrl=self.MODIFIERS[self.KEY_FN],
                shift=self.MODIFIERS[self.KEY_SHIFT],
                shield=self.MODIFIERS[self.KEY_SHIELD],
            )))
        else:
            self.events.emit(Event(
                'input.{}.{}'.format('up' if type is self.UP else 'down', name),
                data=dict(
                    type=type,
                    code=key,
                    key=self.resolve_key(key),
                    ctrl=self.MODIFIERS[self.KEY_FN],
                    shift=self.MODIFIERS[self.KEY_SHIFT],
                    shield=self.MODIFIERS[self.KEY_SHIELD],
                ),
            ))
        if type is self.UP:
            if key is self.KONAMI_CODE[self.KONAMI_COUNTER]:
                self.KONAMI_COUNTER += 1
            else:
                self.KONAMI_COUNTER = 0
            if self.KONAMI_COUNTER is len(self.KONAMI_CODE):
                self.events.emit(Event("input.konami"))
                self.KONAMI_COUNTER = 0
            if key is self.CYBAER_CODE[self.CYBAER_COUNTER]:
                self.CYBAER_COUNTER += 1
            else:
                self.CYBAER_COUNTER = 0
            if self.CYBAER_COUNTER is len(self.CYBAER_CODE):
                self.events.emit(Event("input.cybaer"))
                self.CYBAER_COUNTER = 0
            if key is self.NAHUEL_CODE[self.NAHUEL_COUNTER]:
                self.NAHUEL_COUNTER += 1
            else:
                self.NAHUEL_COUNTER = 0
            if self.NAHUEL_COUNTER is len(self.NAHUEL_CODE):
                self.events.emit(Event("input.nahuel"))
                self.NAHUEL_COUNTER = 0
            if self.MODIFIERS[Input.KEY_SHIELD]:
                if key is self.HNZLMNN_CODE[self.HNZLMNN_COUNTER]:
                    self.HNZLMNN_COUNTER += 1
                else:
                    self.HNZLMNN_COUNTER = 0
                if self.HNZLMNN_COUNTER is len(self.HNZLMNN_CODE):
                    self.events.emit(Event("input.hnzlmnn"))
                    self.HNZLMNN_COUNTER = 0


    def on_char(self, event):
        if event.code is self.KEY_BACKSPACE:
            self.text = self.text[:-1]
        elif self.KEY_A <= event.code <= self.KEY_SPACE or event.code is self.KEY_RETURN:
            self.text += event.key
        if self.max_len:
            self.text = self.text[:self.max_len]
        self.update_display()

    def update_display(self):
        # TODO: draw modifiers
        if not self.screen:
            return
        self.screen.display.fill(display.BACKGROUND)
        y = 0
        if self.title:
            y += self.screen.display.text(self.title, 0, y=y, wrap=self.title_wrap)['height']
        self.screen.display.hline(0, y, self.screen.display.width)
        y += 2
        self.screen.display.text(self.text.encode('ascii') + b'\x7F', 0, y=y, wrap=display.WRAP_INDENT)
        self.screen.display.update()

    def get_user_input(self, screen, context, value='', title=None, title_wrap=display.NO_WRAP, max_len=None):
        self.screen = screen
        self.context = context
        self.title = title
        self.title_wrap = title_wrap
        if not value:
            value = ''
        self.text = value
        self.max_len = max_len
        self.mode(self.MODE_TEXT)
        self.update_display()

    def is_pressed(self, code):
        if self.ioConsole.is_pressed(code):
            return True
        if self.ioKeyboard0.is_pressed(code):
            return True
        if self.ioKeyboard1.is_pressed(code):
            return True
        return False

    def close(self):
        self.ioConsole.close()
        self.ioKeyboard0.close()
        self.ioKeyboard1.close()

