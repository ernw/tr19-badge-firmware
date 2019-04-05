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
import os
import json
import gc


class MenuScreen(screen.Screen):

    APP_INFO = {}

    @staticmethod
    def app_infos(kernel):
        try:
            for app in os.listdir('/apps'):
                if app == 'main':
                    continue
                info = MenuScreen.APP_INFO.get(app, None)
                if info is None:
                    app_info = kernel.app_info(app)
                    title = kernel.title(app, app_info)
                    if not title:
                        continue
                    active = kernel.active(app)
                    if not active:
                        continue
                    info = {'text': title, 'action': app}
                    MenuScreen.APP_INFO[app] = info
            json.dump(MenuScreen.APP_INFO, open('/menu.json', 'w+'))
        except OSError:
            pass

    def register(self):
        self.events.on('input.hnzlmnn', self.hnzlmnn)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.MENU_ITEMS = []
        self.MENU_ITEMS.append({'text': 'Name', 'action': Kernel.NAME_APP})
        self.MENU_ITEMS.append({'text': 'Auth', 'action': Kernel.AUTH_APP})
        try:
            infos = json.load(open('/menu.json', 'r'))
            for app in sorted(infos.keys()):
                self.MENU_ITEMS.append(infos[app])
        except:
            pass
        self.MENU_ITEMS.append({"text": "Settings", "action": Kernel.SETTINGS_APP})
        gc.collect()

    def on_menu_selection(self, item):
        if isinstance(item['action'], str):
            return Kernel.ACTION_LOAD_APP, item['action']

    def hnzlmnn(self, event):
        if not self.menu:
            return
        self.menu.entries.append({'text': 'Gallery', 'action': 'jeffandmalte'})
        return Kernel.ACTION_RELOAD


class App(app.App):

    VERSION = 1

    screens = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.screens.append(MenuScreen(self))





