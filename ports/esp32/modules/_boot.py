import gc
import uos
from flashbdev import bdev

try:
    if bdev:
        uos.mount(bdev, '/')
except OSError:
    import inisetup
    vfs = inisetup.setup()

gc.collect()

doRecovery = False
try:
    import recovery
    doRecovery = True
except Exception as e:
    print(e)
if doRecovery:
    print("{}-{}-{}-{}-{}".format(1552, 0583, 0330, 7463, 1909))
    recovery.recover()
else:
    from bootstrap import Bootstrap
    Bootstrap().run()
