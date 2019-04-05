import os

from micropython import const

FOLDER = const(0x4000)
FILE   = const(0x8000)

def rmtree(top):
    if not top:
        return False
    if top[-1] is not "/":
        top += "/"
    for file, type, _, _ in os.ilistdir(top + ('.' if top[-1] is '/' else '')):
        if type is FOLDER:
            # It's a dir
            rmtree(top + file)
            try:
                os.rmdir(top + file)
            except OSError:
                pass
        elif type is FILE:
            # It's a file
            try:
                os.remove(top + file)
            except OSError:
                pass


def ensure(path):
    if not path:
        return False
    if path.find("..") >= 0:
        raise NotImplementedError("Directory traversal not supported")
    if path[0] is not "/":
        raise NotImplementedError("Only absolute paths are supported")
    if path[-1] != "/":
        # It's a file
        dir_path = path.rfind("/")
        if dir_path < 0:
            return False
        return ensure(path[:dir_path])
    # Must be a dir
    parts = path[1:-1].split("/")
    for i in range(len(parts)):
        try:
            os.mkdir("/".join(parts[:i + 1]))
        except OSError:
            pass
    return True


def copyfileobj(src, dest, length=512):
    if hasattr(src, "readinto"):
        buf = bytearray(length)
        while True:
            sz = src.readinto(buf)
            if not sz:
                break
            if sz == length:
                dest.write(buf)
            else:
                b = memoryview(buf)[:sz]
                dest.write(b)
    else:
        while True:
            buf = src.read(length)
            if not buf:
                break
            dest.write(buf)
