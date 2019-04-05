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
import gc
import sys
import os
import machine
import network
import ujson as json
import ubinascii as binascii
import utime as time
import display

from system import EventLoop, Storage, Input, Accelerometer
from libs import Display, HTTP, TarFile, DIRTYPE, REGTYPE, rmtree, ensure, Light


class Kernel:

    MENU_APP = 'main'
    SETTINGS_APP = 'settings'
    NAME_APP = 'name'
    AUTH_APP = 'auth'
    FUCSS_APP = 'fucss'
    REGISTRATION_APP = 'registration'
    SPECIAL_APP = 'special'
    DEFAULT_APP = NAME_APP

    START_NORMAL = 0
    START_WIFI = 1
    START_BACKEND = 2
    START_NAME = 3
    START_REGISTRATION = 4
    START_SPECIAL = 5
    START_SLEEP = 6

    REASON_EXIT_SYSTEM = 0
    REASON_EXIT_APP = 1

    ACTION_EXIT = 0
    ACTION_LOAD_APP = 1
    ACTION_LOAD_SCREEN = 2
    ACTION_RELOAD = 3

    RTC = machine.RTC()

    def __init__(self, logger):
        self.reason = self.START_NORMAL
        self.wifi_connection = network.WLAN(network.STA_IF)
        try:
            os.mkdir("apps/")
        except:
            pass
        self.secret = None
        # TODO: Save in encryption module
        self.secret_file = 'registration.key'
        self.client = None
        self.app = None
        self.task = None
        self.logger = logger
        self.display = Display()
        self.events = EventLoop()
        self.lights = Light()
        self.input = Input(self)
        self.accel = Accelerometer(self)
        self.storage = Storage(self, 'config.json', dict(
            SSID="trp-badge",
            PSK="5EILZYY-kAGxzLhFrLjln3ThO6qLUd",
            OTA=True,
            OTA_SERVER="https://badge.troopers.de/api",
            RESTART=False,
            NAME=None,
            CERT='MIIFWjCCBEKgAwIBAgISA9L5Owq6Upc+NcvoCeynwoT0MA0GCSqGSIb3DQEBCwUAMEoxCzAJBgNVBAYTAlVTMRYwFAYDVQQKEw1MZXQncyBFbmNyeXB0MSMwIQYDVQQDExpMZXQncyBFbmNyeXB0IEF1dGhvcml0eSBYMzAeFw0xOTAzMDYwODA5NTVaFw0xOTA2MDQwODA5NTVaMBwxGjAYBgNVBAMTEWJhZGdlLnRyb29wZXJzLmRlMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAvNvI/t5eu6G/lkWTAsAXq8PeJAAg/K9gPH9EJTv2h321NvqPIu5qHD1c9GXL77AgNh8q3H6kDAKrLwnucRVXPEkG9tjd/OJ+UrTrxgIVvEdpXszpNg4p5KYFZ3XD6u5bXmUIX8luFfW5mU6Iq3kqFZj3Zeo0vakV9eUWsEV/sFd75A68on/Y84Sr8TIEyqF0qd4GC22bHkcmhJp6iWixiC6J6nW4B7c/9EvtAUZY4kguVL1Oofck197bQMHtGQ70/CeUtBsVIE7BdErCxXFD7tJjWTCTC1WujNUx/JXx21IzuxedAN1YcnnOCXZRWgysbFBIG+kcUsZCmU3LpBT96wIDAQABo4ICZjCCAmIwDgYDVR0PAQH/BAQDAgWgMB0GA1UdJQQWMBQGCCsGAQUFBwMBBggrBgEFBQcDAjAMBgNVHRMBAf8EAjAAMB0GA1UdDgQWBBSlLdWBLw0Wp4RxN2A33VmwScN70zAfBgNVHSMEGDAWgBSoSmpjBH3duubRObemRWXv86jsoTBvBggrBgEFBQcBAQRjMGEwLgYIKwYBBQUHMAGGImh0dHA6Ly9vY3NwLmludC14My5sZXRzZW5jcnlwdC5vcmcwLwYIKwYBBQUHMAKGI2h0dHA6Ly9jZXJ0LmludC14My5sZXRzZW5jcnlwdC5vcmcvMBwGA1UdEQQVMBOCEWJhZGdlLnRyb29wZXJzLmRlMEwGA1UdIARFMEMwCAYGZ4EMAQIBMDcGCysGAQQBgt8TAQEBMCgwJgYIKwYBBQUHAgEWGmh0dHA6Ly9jcHMubGV0c2VuY3J5cHQub3JnMIIBBAYKKwYBBAHWeQIEAgSB9QSB8gDwAHcAdH7agzGtMxCRIZzOJU9CcMK//V5CIAjGNzV55hB7zFYAAAFpUkQy9AAABAMASDBGAiEAu5gK0sMgJZO89ckeIbLRWqpGwnqrw1VrJDi+7RCwcfECIQC7BlUjBvqGnCHXsPvJ6Kbn36FM7jB6n5jFN43JuljeqgB1AGPy283oO8wszwtyhCdXazOkjWF3j711pjixx2hUS9iNAAABaVJEMzwAAAQDAEYwRAIgNDGWmYMu8LCLizzPvyaqY3esHD8kAQEb+8s6SeRP5MACIFAVCGA8MqITaiklniVi02qPYMN7C133K92NeyV9fs7+MA0GCSqGSIb3DQEBCwUAA4IBAQBDhPs8li57LHsMm1heI96Z9D/7lYgco2n7XGk/JWbiQ2AKa+guyExu6OTKci7D3+EnyAF9R4rVnR4O6g8vpBjoIrqXMODvveX5rAMOGJ+hOerA7EbpMnShhHsWe5FGlAdfqZ7K0220WNQlWBFkGHaH2lViO6f3Dgp2WEX8NhLwDrLWfJaYcPQin/3qJn3HDoCySY6NsJyaSldX6OCMDCPp9JhiRrfp/kaoMgti+2x9QUaRJLJsoLSXJ0bIwt5xM0z48H+vsrT6CZVyq345ZcFOFlkgl0ptWATkUFhbH6xuvUtcoTldbKH2tVpKauK40PzEW1hew/wPIXzc9FEqh9+3',
        ))
        self.http = HTTP(self, self.storage.OTA_SERVER, self.id())
        self.registration()
        try:
            import apps.main
            apps.main.MenuScreen.app_infos(self)
        except:
            pass
        gc.collect()

    def safe_reset(self):
        # if machine.reset_cause() is not machine.SOFT_RESET:
        # sleep 1 second to allow KeyBoardInterrupts
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            return
        machine.reset()

    def wifi(self, timeout=None):
        """
        Tries to connect to wifi
        :param timeout: Timeout in ms
        :return: True if connected, False if no connection could be established
        """
        if self.wifi_connected():
            return True
        if self.storage.SSID and self.storage.PSK:
            self.display.text("Connecting to WiFi...", 0, line=0, update=True)
            self.wifi_connection = network.WLAN(network.STA_IF)
            if not self.wifi_connection.active():
                self.wifi_connection.active(True)
            if not self.wifi_connection.isconnected():
                self.wifi_connection.connect(self.storage.SSID, self.storage.PSK)
                if not timeout:
                    while not self.wifi_connection.isconnected():
                        machine.idle()
                else:
                    start = time.ticks_ms()
                    while not self.wifi_connection.isconnected() and time.ticks_ms() - start < timeout:
                        machine.idle()
            if not self.wifi_connection.isconnected():
                self.wifi_off()
                self.logger.error("WiFi connection could not be established!")
                return False
        else:
            self.wifi_off()
            self.logger.error("No WiFi configuration available!")
            return False
        return True

    def wifi_off(self):
        if self.wifi_connection and self.wifi_connection.active():
            self.wifi_connection.active(False)

    def wifi_connected(self):
        return self.wifi_connection and self.wifi_connection.isconnected()

    def ensure_registration(self):
        if not self.registration():
            ret = self.register()
            if ret > 0:
                return ret + 1
        if not self.registration():
            self.display.text("No registration!", 0, line=1, update=True)
            self.logger.error("Device misses registration!")
            return 1
        return 0

    def start(self, reason=None):
        if reason is None:
            reason = self.START_NORMAL
        self.reason = reason
        try:
            if reason is self.START_SLEEP:
                self.load(self.MENU_APP)
            else:
                self.lights.off()
                print('Starting!', reason)
                self.display.text("Starting...", 0, line=2, update=True)
                self.display.clear()
                # Turn off wifi before every app load
                self.wifi_off()
                if reason is self.START_NORMAL:
                    self.load()
                elif reason is self.START_WIFI:
                    self.load(self.SETTINGS_APP, 1)
                elif reason is self.START_BACKEND:
                    self.load(self.SETTINGS_APP, 0, selected_index=2)
                elif reason is self.START_NAME:
                    self.load(self.SETTINGS_APP, 0, selected_index=3)
                elif reason is self.START_REGISTRATION:
                    self.load(self.REGISTRATION_APP)
                elif reason is self.START_SPECIAL:
                    self.load(self.SPECIAL_APP)
            while self.task:
                result = self.task.run()
                if result is None:
                    # Load default app
                    # self.task = self.load(self.DEFAULT_APP)
                    continue
                action, extra = result
                if type(extra) is not dict:
                    extra = dict(app=extra)
                if action == self.ACTION_EXIT:
                    break
                elif action == self.ACTION_LOAD_APP:
                    if reason is not self.START_NORMAL and reason is not self.START_SLEEP:
                        self.safe_reset()
                    self.load(**extra)
                else:
                    raise ValueError("Invalid action {}".format(action))
        except KeyboardInterrupt:
            self.exit()
        except Exception as e:
            try:
                self.display.reset()
                self.display.fill(display.BACKGROUND)
                self.display.text("Crashed!", 0, line=0, update=True)
                self.display.text("Reset please!", 0, line=1, update=True)
                self.logger.exception(e)
                # Be careful!
                if self.storage.RESTART:
                    machine.reset()
            except Exception as e:
                print("Fatal error!")
                print(e)
                sys.exit(1)
        return self.ACTION_EXIT, None

    def load(self, app=None, screen=0, **kwargs):
        if not app:
            app = self.DEFAULT_APP
        if self.app == app:
            return self.task
        try:
            exec("import apps.{}".format(app), {})
        except (ImportError, AttributeError, IndentationError, SyntaxError) as e:
            self.logger.exception(e)
            self.logger.error("Can't import app '{}'. Not switching!".format(app))
            return self.task
        if self.app and self.task:
            self.logger.debug('Closing app', self.app)
            self.task.exit(self.REASON_EXIT_SYSTEM)
            self.task = None
            # Important to allow app to simply register listeners without checking for duplicates
            self.events.clear()
            del sys.modules["apps.{}".format(self.app)]
            gc.collect()
        try:
            self.logger.debug('Starting app', app)
            self.app = app
            self.task = sys.modules["apps.{}".format(app)].App(self, screen, **kwargs)
        except Exception as e:
            self.logger.exception(e)
            self.display.reset()
            self.display.fill(display.BACKGROUND)
            self.display.text('Failed to load app. Please reset.', 0, y=0, update=True)
            self.task = None
            return None
        return self.task

    def name(self, app, info=None):
        if not info:
            info = self.app_info(app)
        try:
            return info['name']
        except (TypeError, KeyError):
            return app[:1].upper() + app[1:]

    def version(self, app, info=None):
        if not info:
            info = self.app_info(app)
        try:
            return info['version']
        except (TypeError, KeyError):
            return -1

    def title(self, app, info=None):
        if not info:
            info = self.app_info(app)
        try:
            return info['title']
        except (TypeError, KeyError):
            return self.name(app)

    def app_info(self, app=None):
        if not app:
            return None
        try:
            with open('/apps/{}/info.json'.format(app)) as f:
                info = json.load(f)
        except Exception:
            return None
        return info

    def active(self, app):
        if app == self.app:
            return self.task.NAME, self.task.is_active, self.task.version()
        try:
            exec("import apps.{}".format(app), {})
        except (ImportError, AttributeError, IndentationError, SyntaxError) as e:
            self.logger.exception(e)
            return True
        try:
            task = sys.modules["apps.{}".format(app)].App(self)
            active = task.is_active
            del sys.modules["apps.{}".format(app)]
            gc.collect()
        except Exception:
            return True
        return active

    def id(self):
        return binascii.hexlify(machine.unique_id())

    def mac(self):

        return binascii.hexlify(self.wifi_connection.config('mac'))

    def auth_code(self):
        if not self.wifi(10000):
            return None
        r = self.http.get('/auth')
        if r is None:
            self.wifi_off()
            return None
        if r.status_code is not 200:
            self.wifi_off()
            return None
        json = r.json()
        self.wifi_off()
        if json is None:
            return None
        try:
            return json['response']['token']
        except KeyError:
            return None


    def register(self):
        try:
            r = self.http.post('/register', json={
                'id': self.id(),
                'mac': self.mac(),
            })
            if not r:
                self.logger.info("Provisioning server unreachable!")
                return 2
            # Already registered
            if r.status_code is 401:
                self.logger.info("Already registered!")
                return 1
            elif r.status_code is 200:
                if len(r.content) == 0:
                    return 2
                registration = r.json()
                with open(self.secret_file, 'w') as f:
                    f.write(registration['response']['secret'])
                self.secret = registration['response']['secret']
                self.http.set_key(registration['response']['secret'])
        except (OSError, ValueError) as e:
            self.logger.exception(e)
            return 2
        return 0

    def registration(self):
        if not self.secret:
            try:
                with open(self.secret_file, 'r') as f:
                    self.secret = f.read()
                    self.http.set_key(self.secret)
            except Exception as e:
                pass
        return self.secret

    def factory(self):
        self.storage.wipe()
        rmtree('/apps')
        self.safe_reset()

    def wipe(self):
        self.secret = None
        try:
            os.remove(self.secret_file)
        except:
            pass

    def ota(self, try_register=True):
        """
        Checks for updates available and if any are, installs them
        :param try_register: Should the kernel try to register the badge to the server if not already registered
        :return: bool If True, indicates that the badge needs to restart
        """
        if not self.storage.OTA or not self.storage.OTA_SERVER:
            return False
        self.display.text("Looking for updates...", 0, line=1, update=True)
        versions = {}
        try:
            for app in os.listdir('/apps'):
                versions[app] = self.version(app)
        except OSError:
            try:
                os.mkdir('/apps')
            except OSError:
                pass
        try:
            update = self.http.post('/update', json=dict(versions=versions), raw=True)
            if update is None:
                self.logger.error("Update server unreachable!")
                return False
            if update.status_code is 200:
                self.logger.info("Update available!")
                self.display.text('Installing update...', 0, line=2, update=True)
                # TODO: Extract file
                # TODO: Check signature?
                tar = TarFile(fileobj=update.raw)
                for file in tar:
                    path = "/apps/" + file.name
                    ensure(path)
                    if file.type is DIRTYPE:
                        # Delete old app files
                        rmtree(path)
                    elif file.type is REGTYPE:
                        src = tar.extractfile(file)
                        with open(path, "wb") as dest:
                            while True:
                                buf = src.read(512)
                                if not buf:
                                    break
                                dest.write(buf)
                        # copyfileobj(tar.extractfile(file), open(path, "wb"))
                self.logger.info("Update installed!")
                return True
            elif update.status_code is 204:
                self.logger.info("No update available!")
            elif update.status_code is 404:
                # Badge not registered
                if not try_register:
                    return False
                self.wipe()
                self.register()
                if not self.registration():
                    self.logger.error("Can't register device!")
                    sys.exit(1)
                return self.ota(False)
            else:
                self.logger.error("Failed to retrieve update status!")
        except Exception as e:
            self.logger.exception(e)
        return False

    def update(self):
        if self.wifi(10):
            return self.storage.update()
        return False

    def skip_checks(self):
        return self.input.is_pressed(Input.BTN_START)

    def boot_special(self):
        return self.input.is_pressed(Input.BTN_B)

    def draw_kernel(self, screen):
        """
        This method may be used to draw elements above all screens (clock, menu, input mode)
        :param screen: The screen instance that called this method
        :return: None
        """
        # TODO: Implement clock display
        pass

    def exit(self):
        """
        Do all the clean-up work
        """
        self.wifi_off()
        self.display.close()
        self.input.close()
