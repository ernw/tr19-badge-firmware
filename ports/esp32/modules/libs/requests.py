# Copyright Paul Sokolovsky
# Licensed under MIT
# https://github.com/micropython/micropython-lib/tree/master/urequests/
# Added support for cert pinning
import usocket
import ussl
import ujson


class Response:

    def __init__(self, f, headers={}):
        self.raw = f
        self.status_code = 0
        self.reason = ''
        self.encoding = 'utf-8'
        self.headers = headers
        self._cached = None

    def close(self):
        if self.raw:
            self.raw.close()
            self.raw = None
        self._cached = None

    @property
    def content(self):
        if self._cached is None:
            try:
                self._cached = self.raw.read()
            except OSError:
                self._cached = b''
            finally:
                self.raw.close()
                self.raw = None
        return self._cached

    @property
    def text(self):
        return str(self.content, self.encoding)

    def json(self):
        try:
            return ujson.loads(self.content)
        except ValueError:
            return None

def _do_request(kernel, method, url, data, headers, certs, timeout, no_exception):
    if certs:
        if type(certs) is not list:
            certs = [certs]
    if not kernel.wifi(10000):
        if no_exception:
            return None
        raise RuntimeError('Unable to connect to wifi')
    try:
        proto, dummy, host, path = url.split('/', 3)
    except ValueError:
        proto, dummy, host = url.split('/', 2)
        path = ''
    if proto == 'http:':
        port = 80
    elif proto == 'https:':
        port = 443
    else:
        if no_exception:
            return None
        raise ValueError('Unsupported protocol: ' + proto)

    if ":" in host:
        host, port = host.split(":", 1)
        port = int(port)

    ai = usocket.getaddrinfo(host, port, 0, usocket.SOCK_STREAM)
    if len(ai) is 0:
        if no_exception:
            return None
        raise ValueError('Could not resolve host: ' + host)
    ai = ai[0]

    s = usocket.socket(ai[0], ai[1], ai[2])
    s.settimeout(timeout)
    received_headers = {}
    try:
        s.connect(ai[-1])
        if proto == 'https:':
            # TODO: CPU clock adjustment
            s = ussl.wrap_socket(s, server_hostname=host)
            # TODO: CPU clock adjustment
            if certs:
                valid = False
                for cert in certs:
                    if s.getpeercert(True) == cert:
                        valid = True
                        break
                if not valid:
                    if no_exception:
                        return None
                    raise ValueError('Peer certificate invalid!')
        s.write(b'%s /%s HTTP/1.0\r\n' % (method, path))
        if 'Host' not in headers:
            s.write(b'Host: %s\r\n' % host)
        # Iterate over keys to avoid tuple alloc
        for k in headers:
            s.write(k)
            s.write(b': ')
            s.write(headers[k])
            s.write(b'\r\n')
        if data:
            s.write(b'Content-Length: %d\r\n' % len(data))
        s.write(b'\r\n')
        if data:
            s.write(data)
        l = s.readline()
        l = l.split(None, 2)
        status = int(l[1])
        reason = ''
        if len(l) > 2:
            reason = l[2].rstrip()
        while True:
            l = s.readline()
            if not l or l == b'\r\n':
                break
            colon = l.find(b': ')
            if colon > 0:
                received_headers[l[:colon]] = l[colon + 2:].decode('utf8')
            if l.startswith(b'Transfer-Encoding:'):
                if b'chunked' in l:
                    if no_exception:
                        return None
                    raise ValueError('Unsupported ' + l)
            elif l.startswith(b'Location:') and not 200 <= status <= 299:
                if no_exception:
                    return None
                raise NotImplementedError('Redirects not yet supported')
            elif l.startswith(b'X-Time:'):
                dt = received_headers[b'X-Time'].split('-')
                if len(dt) >= 8:
                    kernel.RTC.init([int(t) for t in dt[:8]])
    except OSError as e:
        s.close()
        if no_exception:
            return None
        raise
    resp = Response(s, received_headers)
    resp.status_code = status
    resp.reason = reason
    return resp

def request(kernel, method, url, data=None, headers={}, certs=None, timeout=5, no_exception=True, raw=False):
    wifi_status = kernel.wifi_connected()
    try:
        result = _do_request(kernel, method, url, data, headers, certs, timeout, no_exception)
        if not raw:
            try:
                result.content
            except:
                pass
    except:
        if not raw and not wifi_status:
            kernel.wifi_off()
        raise
    if not raw and not wifi_status:
        kernel.wifi_off()
    return result



def head(url, **kwargs):
    return request('HEAD', url, **kwargs)


def get(url, **kwargs):
    return request('GET', url, **kwargs)


def post(url, **kwargs):
    return request('POST', url, **kwargs)


def put(url, **kwargs):
    return request('PUT', url, **kwargs)


def patch(url, **kwargs):
    return request('PATCH', url, **kwargs)


def delete(url, **kwargs):
    return request('DELETE', url, **kwargs)
