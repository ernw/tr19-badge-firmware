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

import ujson as json
import os


class Storage:

    def __init__(self, kernel, file, defaults={}):
        self.kernel = kernel
        self._file = file
        self._data = defaults
        try:
            with open(self._file, 'r') as f:
                data = json.load(f)
                if not isinstance(data, dict):
                    raise ValueError("Only dicts can be loaded")
                self._data.update(data)
        except:
            pass
        self._data.setdefault('_settings', {})

    def update(self):
        result = self.kernel.http.post('/settings/update')
        import gc
        gc.collect()
        if result is None:
            return False
        if result.status_code is not 200:
            return False
        json = result.json()
        if type(json) is not dict:
            return False
        json = json['response']
        if type(json) is not dict:
            return False
        name = json.get('name', None)
        if name:
            self._data['NAME'] = name
        image = json.get('image', None)
        if image:
            self._data['IMAGE'] = image
        schedule = json.get('schedule', None)
        if schedule:
            self._data['SCHEDULE'] = schedule
        settings = json.get('settings', {})
        for k, v in [(key, settings[key]) for key in settings.keys()]:
            self._data['_settings'][k] = v
        self._save()
        return True

    def _save(self, remote=True):
        with open(self._file, 'w') as f:
            json.dump(self._data, f)

    def __getattr__(self, item):
        return self._data.get(item, None)

    def __getitem__(self, item):
        return self._data.get(item, None)

    def __setitem__(self, key, value):
        self._data[key] = value
        self._save()

    def get(self, item, default=None):
        if not item.startswith(self.kernel.app + '.'):
            return default
        return self._data['_settings'].get(item, default)

    def set(self, key, value):
        result = self.kernel.http.post('/settings/set', json={key: value})
        if result is not None and result.status_code is 204:
            self._data['_settings'][key] = value

    def sync(self):
        if self.kernel.ensure_registration() > 0:
            return
        result = self.kernel.http.post('/name', json={'name': self.NAME})

    def wipe(self):
        try:
            os.remove(self._file)
        except:
            pass




