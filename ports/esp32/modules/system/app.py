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

import gc

from system.menu import Menu
from system import Kernel


class App:
    VERSION = 0
    NAME = None
    screens = []

    def __init__(self, kernel, screen=0, **kwargs):
        """
        system needs to be set.
        :param kernel:
        """
        self.kernel = kernel
        self.screen = None
        self.initial_screen = screen
        try:
            self.screens[self.initial_screen].init(**kwargs)
        except IndexError:
            self.initial_screen = 0

    @property
    def display(self):
        return self.kernel.display

    @property
    def input(self):
        return self.kernel.input

    @property
    def http(self):
        return self.kernel.http

    @property
    def events(self):
        return self.kernel.events

    @property
    def storage(self):
        return self.kernel.storage

    @property
    def lights(self):
        return self.kernel.lights

    @property
    def accel(self):
        return self.kernel.accel

    @property
    def is_active(self):
        return True

    def menu(self, entries, selected_index=None):
        return Menu(self.display, entries, selected_index)

    def run(self):
        if not self.screens:
            raise NotImplementedError("All apps must define at least one screen")
        try:
            self.screen = self.load(self.initial_screen)
            while self.screen:
                gc.collect()
                result = self.screen.run(self)
                if result is None:
                    result = self.events.keep_listening()
                while result is Kernel.ACTION_RELOAD:
                    gc.collect()
                    # self.display.reset()
                    # self.events.clear()
                    # self.screen.register()
                    result = self.screen.do_render()
                    if result is None:
                        self.events.result = None
                        result = self.events.keep_listening()
                if result is None:
                    # Load default app
                    return Kernel.ACTION_LOAD_APP, Kernel.DEFAULT_APP
                if not isinstance(result, tuple) or not len(result) is 2:
                    # TODO: Maybe log wrong return value
                    return Kernel.ACTION_LOAD_APP, Kernel.DEFAULT_APP
                action, extra = result
                if action == Kernel.ACTION_EXIT:
                    break
                elif action == Kernel.ACTION_LOAD_APP:
                    return action, extra
                elif action == Kernel.ACTION_LOAD_SCREEN:
                    self.screen = self.load(extra)
                else:
                    raise ValueError("Invalid action {}".format(action))
        except KeyboardInterrupt:
            raise
        return Kernel.ACTION_EXIT, None

    def load(self, screen=0):
        if screen < 0 or screen >= len(self.screens):
            raise ValueError("Screen {} does not exist".format(screen))
        self.display.reset()
        self.events.clear()
        self.lights.off()
        return self.screens[screen]

    def exit(self, reason=None):
        # Do not call system again if exit was called from system
        if reason is Kernel.REASON_EXIT_SYSTEM:
            return
        # Check if we triggered the exit
        if reason is Kernel.REASON_EXIT_APP:
            return
        self.kernel.load(None)

    def version(self):
        if self.VERSION < 1:
            raise NotImplementedError("All apps must specify their version >=1!")
        return self.VERSION


