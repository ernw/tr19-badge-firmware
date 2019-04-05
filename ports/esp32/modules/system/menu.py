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

class Menu:
    def __init__(self, display, entries=[], selected_index=None):
        """

        :param display:
        :param entries: {text:string, action:Action?}
        """
        self.display = display
        self.entries = entries
        self.index = selected_index if selected_index else 0
        self.top = max(0, self.index - self.display.lines + 1)

    def update(self):
        self.display.reset()
        self.display.fill(display.BACKGROUND)
        for i in range(self.top, min(len(self.entries), self.top + self.display.lines)):
            line = i - self.top
            y = line * self.display.fontSize[1]
            if i == self.index:
                self.display.fill_rect(0, y, self.display.width, y + self.display.fontSize[1], color=display.FOREGROUND, update=False)
                self.display.text(self.entries[i]["text"], 0, y=y, color=display.BACKGROUND, update=False)
            else:
                self.display.text(self.entries[i]["text"], 0, y=y, update=False)
        self.display.update()

    def up(self, update=True):
        if self.index == 0:
            self.index = len(self.entries) - 1
            self.top = max(0, len(self.entries) - self.display.lines)
        elif self.index == self.top:
            self.index -= 1
            self.top -= 1
        else:
            self.index -= 1
        if update:
            self.update()

    def down(self, update=True):
        if self.index == len(self.entries) - 1:
            self.index = 0
            self.top = 0
        elif self.index == self.top + self.display.lines - 1:
            self.index += 1
            self.top += 1
        else:
            self.index += 1
        if update:
            self.update()

    def current(self):
        return self.entries[self.index]
