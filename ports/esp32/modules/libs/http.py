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

import libs.requests as requests
import uhashlib
import ubinascii
import ujson
import gc


class HTTP:

    def __init__(self, kernel, server, id, key=None):
        self.kernel = kernel
        self.server = server
        self.id = id
        self.certs = []
        if not key:
            # Probably not provisioned yet
            self.key = b'\x00'*32
        else:
            self.set_key(key)
        if self.kernel.storage.CERT:
            self.certs.append(ubinascii.a2b_base64(self.kernel.storage.CERT))
        try:
            with open('server.crt') as f:
                lines = f.readlines()
                if len(lines) > 0:
                    lines[0] = lines[0].replace('-----BEGIN CERTIFICATE-----', '')
                    lines[-1] = lines[-1].replace('-----END CERTIFICATE-----', '')
                    self.certs.append(ubinascii.a2b_base64(''.join(lines)))
            gc.collect()
        except OSError:
            pass

    def set_key(self, key):
        self.key = ubinascii.unhexlify(bytearray(key))

    def set_server(self, server):
        if not server:
            return
        self.server = server

    def sign(self, method, url, data):
        try:
            path = '/' + url.split('/', 3)[3]
        except ValueError:
            path = '/'
        hash = uhashlib.sha256(self.key)
        hash.update(method.encode('ascii') if method else b'')
        hash.update(path.encode('ascii') if url else b'')
        if not data:
            data = b''
        try:
            hash.update(data.encode('ascii'))
        except AttributeError:
            hash.update(data)
        return ubinascii.hexlify(hash.digest())

    def request(self, method, url, json=None, **kwargs):
        """
        Requests a resource using the given HTTP method
        :parameter method The HTTP method to use
        :param method string
        :parameter url The url to request
        :param url string
        :parameter json Optionally converts dict to string and sets correct content type
        :param json dict
        :returns An Response object or None if no connection could be established
        :return Response | None
        """
        kwargs.setdefault('headers', {})
        if kwargs.get('data', None) is not None:
            kwargs['headers']['Content-Type'] = 'application/x-www-form-urlencoded'
        if json:
            kwargs['data'] = ujson.dumps(json)
            kwargs['headers']['Content-Type'] = 'application/json'
        kwargs['headers']['X-Id'] = self.id
        kwargs['headers']['X-Signature'] = self.sign(method, self.server + url, kwargs.get('data', None))
        kwargs.setdefault('certs', [])
        if type(kwargs['certs']) is not list:
            kwargs['certs'] = []
        for cert in self.certs:
            kwargs['certs'].append(cert)
        return requests.request(self.kernel, method, self.server + url, **kwargs)

    def head(self, url, **kwargs):
        return self.request("HEAD", url, **kwargs)

    def get(self, url, **kwargs):
        return self.request("GET", url, **kwargs)

    def post(self, url, **kwargs):
        return self.request("POST", url, **kwargs)

    def put(self, url, **kwargs):
        return self.request("PUT", url, **kwargs)

    def patch(self, url, **kwargs):
        return self.request("PATCH", url, **kwargs)

    def delete(self, url, **kwargs):
        return self.request("DELETE", url, **kwargs)

