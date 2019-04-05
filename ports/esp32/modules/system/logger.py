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

import sys
import json
import io


class JSONLogger:
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50
    levelnames = {
        10: 'DEBUG',
        20: 'INFO',
        30: 'WARNING',
        40: 'ERROR',
        50: 'CRITICAL',
    }

    def __init__(self, file, level=WARNING, max_entries=20, do_print=False):
        self.file = file
        self.level = level
        self.max_entries = max_entries
        self.do_print = do_print
        try:
            with open(self.file, 'r') as f:
                self.json = json.load(f)
        except Exception as e:
            sys.print_exception(e)
            self.json = []

    def save(self):
        with open(self.file, 'w+') as f:
            json.dump(self.json[-self.max_entries:], f)

    def log(self, *args, **kwargs):
        level = kwargs.get('level', JSONLogger.DEBUG)
        traceback = kwargs.get('traceback', None)
        msg = ' '.join(str(arg) for arg in args)
        if level < self.level:
            return
        try:
            self.json.append(dict(
                level=self.levelnames[level],
                message=msg,
                traceback=traceback,
            ))
            self.json = self.json[-self.max_entries:]
            if self.do_print:
                print(msg)
                if traceback:
                    print(traceback)
            self.save()
        except Exception as e:
            print('Could not log message!')
            sys.print_exception(e)
            sys.exit(1)

    def debug(self, *args):
        self.log(*args, level=JSONLogger.DEBUG)

    def info(self, *args):
        self.log(*args, level=JSONLogger.INFO)

    def warning(self, *args):
        self.log(*args, level=JSONLogger.WARNING)

    def error(self, *args):
        self.log(*args, level=JSONLogger.ERROR)

    def critical(self, *args):
        self.log(*args, level=JSONLogger.CRITICAL)

    def exception(self, e):
        traceback = io.StringIO()
        sys.print_exception(e, traceback)
        self.log(str(e), level=JSONLogger.ERROR, traceback=traceback.getvalue())
        traceback.close()
