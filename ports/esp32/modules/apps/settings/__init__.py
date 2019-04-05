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

from system import app, screen, Kernel
import display

class SettingsScreen(screen.Screen):

    ACTION_WIFI = 0
    ACTION_URL = 1
    ACTION_NAME = 2
    ACTION_IMAGE = 3
    ACTION_INFO = 4
    ACTION_RESET = 5

    CONTEXT_URL = 0
    CONTEXT_NAME = 1
    CONTEXT_RESET = 2

    MENU_ITEMS = [
        {'text': 'Badge ID', 'action': ACTION_INFO},
        {'text': 'WiFi', 'action': ACTION_WIFI},
        {'text': 'OTA Url', 'action': ACTION_URL},
        {'text': 'Change name', 'action': ACTION_NAME},
        {'text': 'Change Image', 'action': ACTION_IMAGE},
        {'text': 'Factory reset', 'action': ACTION_RESET},
    ]

    def register(self):
        self.events.on('input.hnzlmnn', self.hnzlmnn)

    def on_menu_selection(self, item):
        if item['action'] == self.ACTION_WIFI:
            return Kernel.ACTION_LOAD_SCREEN, 1
        if item['action'] == self.ACTION_URL:
            self.input.get_user_input(self, self.CONTEXT_URL, self.storage.OTA_SERVER, 'Provisioning server url', max_len=120)
        if item['action'] == self.ACTION_IMAGE:
            return Kernel.ACTION_LOAD_SCREEN, 2
        if item['action'] == self.ACTION_NAME:
            self.input.get_user_input(self, self.CONTEXT_NAME, self.storage.NAME, 'Set your name', max_len=51)
        if item['action'] == self.ACTION_INFO:
            return Kernel.ACTION_LOAD_SCREEN, 3
        if item['action'] == self.ACTION_RESET:
            self.input.get_user_input(self, self.CONTEXT_RESET, '', 'Type \'yes\' to reset the badge', max_len=3)

    def on_text(self, event):
        if not event.value:
            return
        if event.context is self.CONTEXT_URL:
            self.storage['OTA_SERVER'] = event.value
        elif event.context is self.CONTEXT_NAME:
            self.storage['NAME'] = event.value
            self.display.fill(display.BACKGROUND)
            self.display.text('Saving name to the cloud...', 0, y=0, wrap=display.WRAP_INDENT, update=True)
            self.display.fill(display.BACKGROUND)
            self.storage.sync()
            if self.kernel.reason is Kernel.START_NAME:
                self.kernel.safe_reset()
        elif event.context is self.CONTEXT_RESET:
            if event.value.lower() == 'yes':
                self.display.fill(display.BACKGROUND)
                self.display.text('Resetting badge...', 0, y=0, wrap=display.WRAP_INDENT, update=True)
                self.kernel.factory()

    def back(self, event):
        return Kernel.ACTION_LOAD_APP, Kernel.DEFAULT_APP

    def hnzlmnn(self, event):
        self.display.rotation(display.ROTATE_270)
        return Kernel.ACTION_RELOAD


class WiFiScreen(screen.Screen):

    ACTION_SSID = 0
    ACTION_PSK = 1

    CONTEXT_SSID = 0
    CONTEXT_PSK = 1

    MENU_ITEMS = [
        {'text': 'SSID', 'action': ACTION_SSID},
        {'text': 'PSK', 'action': ACTION_PSK},
    ]

    def on_menu_selection(self, item):
        if item['action'] == self.ACTION_SSID:
            self.input.get_user_input(self, self.CONTEXT_SSID, self.storage.SSID, item['text'], max_len=64)
        if item['action'] == self.ACTION_PSK:
            self.input.get_user_input(self, self.CONTEXT_PSK, self.storage.PSK, item['text'], max_len=64)

    def on_text(self, event):
        if event.context is self.CONTEXT_SSID:
            self.storage['SSID'] = event.value
        if event.context is self.CONTEXT_PSK:
            self.storage['PSK'] = event.value

    def back(self, event):
        return Kernel.ACTION_LOAD_SCREEN, 0


class ImageScreen(screen.Screen):

    def update(self, delta=0):
        self.display.fill(display.BACKGROUND)
        self.display.text('Go to https://badge.troopers.de/name', 0, y=0, wrap=display.WRAP_INDENT, update=True)

    def back(self, event):
        return Kernel.ACTION_LOAD_SCREEN, 0


class InfoScreen(screen.Screen):

    def update(self, delta=0):
        id = self.kernel.id()
        self.display.font(display.FONT_DEJAVU_42)
        space = 16
        size = self.display.text(id, x=space, y=0, max_width=self.display.width - 2 * space, wrap=display.WRAP_INDENT)
        self.display.fill(display.BACKGROUND)
        x = self.display.width // 2 - size['width'] // 2
        y = self.display.height // 2 - size['height'] // 2
        self.display.text(id, x=x, y=y, max_width=self.display.width - 2 * space, wrap=display.WRAP_INDENT, update=True)

    def back(self, event):
        return Kernel.ACTION_LOAD_SCREEN, 0


class App(app.App):

    VERSION = 1

    screens = [
        SettingsScreen(),
        WiFiScreen(),
        ImageScreen(),
        InfoScreen(),
    ]

    def __init__(self, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)



