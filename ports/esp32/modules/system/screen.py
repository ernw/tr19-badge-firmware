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

from system import Kernel, Input
import utime


class Screen:

    HIDE_KERNEL = False
    MENU_ITEMS = []

    def __init__(self, app=None, continuous_rendering=False, disable_back=False, selected_index=None):
        self.app = app
        self.continuous_rendering = continuous_rendering
        self.disable_back=disable_back
        self.running = False
        self.menu = None
        self.selected_index = selected_index

    def __getattr__(self, item):
        try:
            return getattr(self.app, item)
        except AttributeError:
            raise AttributeError("Attribute '{}' does not exist on the current screen!".format(item))

    def run(self, app=None):
        if app:
            self.app = app
        # Allow input to receive char inputs
        self.events.on("input.char", self.input.on_char)
        # Setup back key
        self.events.on("input.up.{}".format(Input.key_name(Input.BTN_B)), self.on_back)
        self.events.on("input.up.{}".format(Input.key_name(Input.BTN_START)), self.on_back)
        self.running = True
        self.init()
        self.register()
        if self.continuous_rendering:
            last = None
            while self.running:
                now = utime.ticks_ms()
                result = self.update(0 if not last else now - last)
                if result is not None:
                    return result
                self.do_render()
                result = self.events.has_result()
                if result is not None:
                    return result
                last = now
        else:
            # TODO: Check whether applicable to continuous rendering screens
            # Handle default event
            self.events.on("input.up", self.on_key_up)
            self.events.on("input.down", self.on_key_down)
            self.events.on("input.text", self._event_handler)
            # Handle automatic menu creation
            if self.MENU_ITEMS:
                self.menu = self.app.menu(self.MENU_ITEMS, self.selected_index)
            if self.menu:
                self.events.on('input.up.{}'.format(Input.key_name(Input.BTN_UP)), self._event_handler)
                self.events.on('input.up.{}'.format(Input.key_name(Input.BTN_DOWN)), self._event_handler)
                self.events.on('input.up.{}'.format(Input.key_name(Input.BTN_A)), self._event_handler)
                self.events.on('input.up.{}'.format(Input.key_name(Input.BTN_SELECT)), self._event_handler)
                if self.selected_index:
                    return self.on_menu_selection(self.menu.current())
            self.do_render()
            return self.events.keep_listening()
        return Kernel.ACTION_EXIT, None

    def exit(self, reason=None):
        self.running = False
        self.app.exit(reason)

    def on_back(self, event):
        # Disable back key handling for text input mode as this key is used to return to calling screen
        if not self.disable_back and self.input.mode() is not Input.MODE_TEXT:
            return self.back(event)

    def do_render(self):
        if self.continuous_rendering:
            result = self.render()
        else:
            if self.menu:
                self.menu.update()
            result = self.update()
        if not self.HIDE_KERNEL:
            self.kernel.draw_kernel(self)
        return result

    def back(self, event):
        """
        Called when user hits back key. Override to implement custom back
        """
        return Kernel.ACTION_LOAD_APP, Kernel.DEFAULT_APP

    def init(self, **kwargs):
        """
        Override to implement event listeners for continuous rendering.
        """
        selected_index = kwargs.get('selected_index', None)
        if selected_index:
            self.selected_index = selected_index

    def register(self):
        """
        Allow to register any event listeners
        """
        pass

    def update(self, delta=0):
        """
        For non continuous rendering this method is called once. For continuous rendering this method is called every frame.
        """
        if self.continuous_rendering:
            raise NotImplementedError("The update method of a Screen needs to be implemented!")

    def render(self):
        """
        This method should be used to update the screen content for continuous rendering screens.
        """
        pass

    def on_menu_selection(self, item):
        """
        This method is called when a menu entry is selected by the user
        """
        pass

    def on_key_down(self, event):
        """
        Called when a key down event is registered
        """
        pass

    def on_key_up(self, event):
        """
        Called when a key up event is registered
        """
        pass

    def on_text(self, event):
        """
        Called when a value is returned from Input.get_user_input()
        """
        pass

    def _event_handler(self, event):
        if self.menu and event.code is Input.BTN_UP:
            self.menu.up()
        elif self.menu and event.code is Input.BTN_DOWN:
            self.menu.down()
        elif self.menu and self.input.mode() is not Input.MODE_TEXT and (event.code is Input.BTN_A or event.code is Input.BTN_SELECT):
            return self.on_menu_selection(self.menu.current())
        elif event.name == 'input.text':
            self.input.mode(Input.MODE_DEFAULT)
            if event.value is not None:
                result = self.on_text(event)
                if result is not None:
                    return result
            return self.do_render()


