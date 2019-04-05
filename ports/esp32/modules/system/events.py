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

import machine
import time


class Event:

    def __init__(self, name, sender=None, data={}):
        if isinstance(name, str):
            name = EventLoop.keypath(name)
        self.path = name
        self.sender = sender
        self.data = data

    @property
    def name(self):
        return '.'.join(self.path)

    def __getattr__(self, item):
        return self.data.get(item, None)

    def __str__(self):
        return 'Event {} {}'.format(self.name, self.data)


class EventLoop:
    SIMULATE = None

    def __init__(self):
        self.listeners = {}
        self.listener_count = 0
        self.listener_count_base = 0
        self.result = None

    def finish_base(self):
        self.listener_count_base = self.listener_count

    @staticmethod
    def keypath(key):
        while key.find('..') >= 0:
            key = key.replace('..', '.')
        return key.strip('.').split('.')

    def get(self, path, parents=False):
        if isinstance(path, str):
            path = EventLoop.keypath(path)
        if not isinstance(path, list):
            raise ValueError("Must provide a list a keypath (see EventLoop.keypath()).")
        listeners = self.listeners
        all_listeners = []
        for key in path:
            if key == '_':
                raise ValueError("A listener name cannot be '_'.")
            if parents and '_' in listeners:
                all_listeners.extend(listeners['_'])
            listeners = listeners.setdefault(key, {})
        if parents and '_' in listeners:
            all_listeners.extend(listeners['_'])
        if parents:
            return all_listeners
        return listeners

    def on(self, name, listener, single=False):
        if not name:
            name = ''
        if not listener:
            raise ValueError("No listener specified.")
        self.listener_count += 1
        listeners = self.get(name)
        listeners.setdefault('_', [])
        listeners['_'].append((listener, single))

    def emit(self, event):
        if event is None:
            return
        if not isinstance(event, Event):
            raise ValueError("Only events can be emitted.")
        if self.result is not None:
            return self.result
        listeners = self.get(event.path, True)
        for i, (listener, single) in enumerate(listeners):
            try:
                result = listener(event, self)
            except TypeError:
                result = listener(event)
            if single:
                self.listener_count -= 1
                listeners.pop(i)
            if result is not None:
                self.result = result
                break
        return self.result

    def clear(self):
        self.listeners = {}
        self.listener_count = 0
        self.listener_count_base = 0
        self.result = None

    def active(self):
        return self.listener_count > self.listener_count_base

    def has_result(self):
        if self.result is not None:
            return self.result
        if self.SIMULATE:
            time.sleep(2)
            self.result = self.SIMULATE(self)

    def keep_listening(self):
        try:
            while self.active() and self.result is None:
                machine.idle()
                if self.SIMULATE:
                    time.sleep(2)
                    self.result = self.SIMULATE(self)
            return self.result
        except KeyboardInterrupt:
            raise
