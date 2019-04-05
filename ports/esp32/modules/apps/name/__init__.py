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
import machine
import time

from system import app, screen, Input, Kernel

class RainbowScreen(screen.Screen):

    HIDE_KERNEL = True
    rainbow = None

    def update(self, delta=0):
        pass

    def render(self):
        self.rainbow = self.lights.rainbow(self.rainbow)
        time.sleep_ms(120)

    def back(self, event):
        return Kernel.ACTION_LOAD_SCREEN, 0

class NameScreen(screen.Screen):

    HIDE_KERNEL = True

    def register(self):
        self.events.on('input.konami', lambda event: (Kernel.ACTION_LOAD_SCREEN, 1))
        self.events.on('input.cybaer', self.cybaer)
        self.events.on('input.up.{}'.format(Input.key_name(Input.BTN_B)), self.check_back)
        self.events.on('input.up.{}'.format(Input.key_name(Input.BTN_START)), self.check_back)

    def cybaer(self, event):
        self.display.fill(display.BACKGROUND)
        self.display.image(
            'AwAAAAAAAAAAAAAAAAAAAADAB4AAAAAAAAAAAAAAAAAAAAHgD4AAAAAAAAAAAAAAAAAAAAXwP8gAAAAAAAAAAAAAAAAAAAP8f+AAAAAAAAAAAAAAAAAAACf+//EAAAAAAAAAAAAAAAAAAI////gAAAAAAAAAAAAAAAAAAR////wgAAAAAAAAAAAAAAAABD//f/4AAAAAAAAAAAAAAAAAAH/+f/8EAAAAAAAAAAAAAAAAIP/+f/+AAAAAAAAAAAAAAAAAAf/+f/+AgAAAAAAAAAAAAAABAf/+f//AAAAAAAAAAAAAAAAAA//+f//gEAAAAAAAAAAAAAAIB//+P//wAAAAAAAAAAAAAAAAD//8P//4AgAAAAAAAAAAAABAH//8P//8AAAAAAAAAAAAAAAAP//8P//+AEAAAAAAAAAAAAIAf//8P///AAAAAAAAAAAAAAAA///8P///gAgAAAAAAAAAABAB///8H///wA8AAAAAAAAAAPAD///4H///wA/AAAAAAAAAA/AD///4H///4AfwAAAAAAAAD+AH///4H///8Af8AAAAAAAAP+AP///4H///+Af/gAAAAAAB/+Af///4H////AP/4AAAAAAH/8A////4D////gP/+AAAAAAf/8B////4D////gH//wAAAAB//4B////wD////gH//8AAAAP//4B////wD////wH///AAAA///4D////wD////wD///wAAD///wD////wD////wD///+AAf///wH////wD////4D////gB////wH////wB////4B////4H////gH////gB////8B//////////gP////gB////8A//////////AP////gB////8A//////////AP////gB////+A//f////+//Af////gB////+Af/n////5/+Af////gA////+Af/x////h/+Af////AA/////Af/wf//+D/8A/////AA/////AP/4H//4H/8A/////AA/////AP/8B//gP/8B/////AA/////gP/+Af+Af/8B/////AA/////gP//AP8Af/8B/////AAf////wf//AP8A//+D////+AAf////wf//gP8B//+D////+AAf////w///wH8D///D////+AAf////4///4H4D///H////+AAf////4///8H4H///H////+AAf////5///8H4P///n////+AAP////9///+D4f///v////8AAP/////////D4f///v////8AAP/////////jw/////////8AAP/////////zx/////////8AAP/////////xz/////////8AAH/////////5z/////////4AAH/////////93/////////4AAD/+P///////v/////////wAAB/8P/////////////////gAAB/4P/////////////////gAAA/wP/////////////////AAAA/gP/////////////////AAAAfgP/j//////////5///+AAAAfAf/wf/////////D///+AAAAPA//4D////////wH///8AAAAPD//4Af//////+AP///8AAAAHD//8AD//////wAP///4AAAAHD//+AA//////AAf///4AAAADD///AAf////+AA////wAAAADD///AAP////8AB////wAAAABB///gAH////4AB////gAAAABCA//wAD////wAD////gAAAAABAAf4AB////gAH////AAAAAAAgAAcAA////AAf///+AAAAAAAfAAAAAf//+AB////+AAAAAAAP/AAAAH//8AD////8AAAAAAAP//AAAB//4AP////8AAAAAAAP///gAA//wD/////8AAAAAAIP////wAf////////8AAAAAAMP///////////////8AAAAAAMP///////////////8AAAAAAOP///////////////8AAAAAAP////////////////8AAAAAAP////////////////8AAAAAAP////////////////8AAAAAAP////////////////8AAAAAAP////////////////8AAAAAAP////////////////8AAAAAAP////////////////8AAAAAAP////////////////8AAAAAAP////////////////8AAAAAAP////////////////8AAAAAAP////////////////8AAAAAAP////////////////8AAAAAAH////////////////8AAAAAAL////////////////8AAAAAAN////////////////8AAAAAAO////////////////8AAAAAAPf///////////////8AAAAAAfv///////////////+AAAAAAf3///////////////+AAAAAAf7///////////////+AAAAAAf9///////////////+AAAAAAf+///////////////+AAAAAAf/f//////////////+AAAAAAf/v//////////////+AAAAAAf/3//////////////+AAAAAAf/7//////////////+AAAAAAH/9/////8H///////4AAAAAAB/+/////AA///////gAAAAAAAf/f////AA//////+AAAAAAAAH/v////AAf/////4AAAAAAAAB/3////AAf/////gAAAAAAAAAf4////AA/////+AAAAAAAAAAH/D///wB/////4AAAAAAAAAAB/4P//4D/////gAAAAAAAAAAAP/g//+P////8AAAAAAAAAAAAA/+H///////gAAAAAAAAAAAAAH/4f/////4AAAAAAAAAAAAAAAf/gD///+AAAAAAAAAAAAAAAAD/8Af//wAAAAAAAAAAAAAAAAAP+AP/8AAAAAAAAAAAAAAAAAAA+AP/gAAAAAAAAAAAAAAAAAAAH4f4AAAAAAAAAAAAAAAAAAAAD//wAAAAAAAAAAAAAAAAAAAAB//gAAAAAAAAAAAAAAAAAAAAA//AAAAAAAAAAA',
            76, 0, 144, 128, update=True)

    def check_back(self, event):
        if event.code is Input.BTN_B:
            if self.input.KONAMI_COUNTER is 8:
                return
            if self.input.CYBAER_COUNTER is 4 or self.input.CYBAER_COUNTER is 5:
                return
        if event.code is Input.BTN_START and self.input.CYBAER_COUNTER is 6:
            return
        return self.back(event)

    def update(self, delta=0):
        self.display.fill(display.BACKGROUND)
        if self.storage.NAME == 'HOWDOITURNTHISON':
            self.display.image(
                'AAAAAAAAAAAAAAAAAADAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD8AAAAAf////wAAAAAAAAAAAAAAAAAAAAAAAAAAPwAAAAB/////AAAAAAAAAAAAAH////wAAAAAAAD/AAf///+Gf////AAAAAAAAAAAf////AAAAAAAAP8AB////4Z////8AAAAAAAAAAf/h////////AAB////////////////wAAAAAAAB/+H///////8AAH////////////////AAAAAAAB///////////6/9/////////////////+AAAAAAH///////////////////////////////8AAAAAH////+AAf/g//////////+AAf/gP4P////AAAAAf////4AB/+D//////////4AB/+A/g////8AAAAH4f+H/////////////////////////////8AAAAfh/4f/////////////////////////////wAAAHgH////////////////////////////////wAAAeAf////////////////////////////////AAAHAB/////////////////////////////////AAAcAH////////////////////////////////8AAHgAf////////////////////////////////wAAeAB/////////////////////////////////AAB4AH//////////z/////////////////////8AAHgf///////////P/////////////////////8AAaB//////////////////////////////////wAHgf//////////////////4AHg////////////wAeH///////////z////5//////////////////AB4f///////////P////n/////////////////8AeH/7/////////z///////////////////////wB4f/n/////////P///////////////////////AHh/+f////////////////////////////////9AeH/5/////////////////////////////////8B4f/v/////////////////////////////////wf/////////////////////////////////////Bh3/5////////+P////+///////+//////////8EAAAB+AAAAAAAA/////wAAAAAAAAf/////8AAAwQAAAH4AAAAAAAD/////AAAAAAAAB//////wAADMAAAAeAAAAAAAA/////wAAAAAAAAH//////AAAMwAAAB4AAAAAAAD/////AAAAAAAAAf/////8AAAzAAAAGAAAAAAAAP////8AAAAAAAAB//////wAADMAAAAYAAAAAAAD/////gAAAAAAAAH//////AAAMwAAABgAAAAAAAP////8AAAAAAAAAf/////8AAAzAAAAAAAAAAAAA/////wAAAAAAAAB//////wAADMAAAAAAAAAAAAD/////AAAAAAAAAB//////AAAMwAAAAAAAAAAAAP////+AAAAAAAAAH/////8AAAzAAAAAAAAAAAAA/////8AAAAAAAAAf/////wAAA8AAAAAAAAAAAAD/////wAAAAAAAAB//////AAADwAAAAAAAAAAAA//////AAAAAAAAAH/////8AAAPAAAAAAAAAAAAD/////8AAAAAAAAAf/////wAAA8AAAAAAAAAAAAP/////AAAAAAAAAB//////AAADwAAAAAAAAAAAA/////+AAAAAAAAAH/////8AAAPAAAAAAAAAAAAD/////wAAAAAAAAAf/////wAAA8AAAAAAAAAAAAf/////AAAAAAAAAB//////AAAD//+f//////////////8//////////////////////5///////////////z//////////////////////n///////////////P///////////////////7/+f//////////////8////////////////////AAAAAAAAAAAAD/////4AAAAAAAAAf/////wAAA8AAAAAAAAAAAAP/////AAAAAAAAAB//////AAADwAAAAAAAAAAAA/////8AAAAAAAAAH/////8AAAPAAAAAAAAAAAAD/////4AAAAAAAAAf/////wAAA8AAAAAAAAAAAAP/////wAAAAAAAAB//////AAADwAAAAAAAAAAAA//////AAAAAAAAAH/////8AAAPAAAAAAAAAAAAA/////8AAAAAAAAAf/////wAAA8AAAAAAAAAAAAD/////wAAAAAAAAB//////AAADwAAAAAAAAAAAAP////+AAAAAAAAAH/////8AAAzAAAAAAAAAAAAA/////wAAAAAAAAAf/////wAADMAAAAYAAAAAAAD/////gAAAAAAAAH//////AAAMwAAABgAAAAAAAP////+AAAAAAAAAf/////8AAAzAAAAGAAAAAAAAP////8AAAAAAAAB//////wAADMAAAAYAAAAAAAA/////wAAAAAAAAH//////AAAMwAAAB4AAAAAAAD/////AAAAAAAAAf/////8AAAzAAAAHgAAAAAAAP////8AAAAAAAAB//////wAADBAAAAfgAAAAAAAP////8AAAAAAAAH//////AAAMEAAAB+AAAAAAAA/////wAAAAAAAAf/////8AAAwf/////////////////////////////////////B/////////////////////////////////////8B4f/n/////////////////////////////////wHh/+f/////////////////////////////////AeH/5/////////z///////////////////////wB4f/n/////////P///////////////////////AB4/////////////////n/////////////////8AHh///////////8////+f/////////////////wAeB///////////3////7//gAeH////////////AB4H//////////////////+AB4f///////////8AHgf///////////////////AH/////////////gAfgf///////////P/////////////////////8AAeAB/////////////////////////////////AAB4AH////////////////////////////////8AABwAf////////////////////////////////wAAHAB/////////////////////////////////AAAHAH////////////////////////////////wAAAeAf////////////////////////////////AAAAYB/4f/////////////////////////////wAAAB+H/h//////////////////////////////AAAAB4f+P/0AH/8f///////////////3/X////wAAAAH////+AAf/g//////////+AAf/gP4P////AAAAAf////4AB//D//////////4AB/+B/g////8AAAAAH///////////////////////////////8AAAAAAB/+H///////8AAH////////////////AAAAAAAAH/4P///////wAAf///////////////8AAAAAAAAB////8AAAAAAAA/wAH////j3////wAAAAAAAAAAH////wAAAAAAAD/AAf///+Gf////AAAAAAAAAAAAAAAAAAAAAAAAD8AAAAAf////wAAAAAAAAAAAAAAAAAAAAAAAAAAPwAAAAB/////AAAAAAAAAAAAAAAAAAAAAAAAAAAOAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAA=',
                32, 11, 232, 106
            )
        elif self.storage.IMAGE and len(self.storage.IMAGE) > 0:
            self.display.image(self.storage.IMAGE)
        else:
            name = self.storage.NAME
            if name is None or name == '':
                name = 'Anonymous\n Trooper'
            self.display.font(display.FONT_DEJAVU_42)
            if len(name) > 22:
                self.display.font(display.FONT_DEJAVU_24)
            space = 32
            size = self.display.text(name, x=space, y=0, max_width=self.display.width - 2 * space, wrap=display.WRAP_INDENT)
            self.display.fill(display.BACKGROUND)
            x = self.display.width // 2 - size['width'] // 2
            y = self.display.height // 2 - size['height'] // 2
            self.display.text(name, x=x, y=y, max_width=self.display.width - 2 * space, wrap=display.WRAP_INDENT)
        self.display.update()
        machine.sleep()

    def back(self, event):
        return Kernel.ACTION_LOAD_APP, Kernel.MENU_APP


class App(app.App):

    VERSION = 1
    CYBAER = False

    screens = [
        NameScreen(disable_back=True),
        RainbowScreen(continuous_rendering=True),
    ]



