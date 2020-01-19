'''Wrapper commands for Windows netsh wlan utility

Copyright (c) 2020 Alex Puffer. All rights reserved.

This work is licensed under the terms of the MIT license.  
For a copy, see <https://opensource.org/licenses/MIT>.
'''

import subprocess
from .utils import _flatten_kwargs

NETSH_WLAN = 'netsh wlan {}'
SHOW = NETSH_WLAN.format('show {}')
SHOW_NETWORKS = SHOW.format('networks')
SHOW_PROFILE = SHOW.format('profile {}')
SHOW_INTERFACES = SHOW.format('interface')
DISCONNECT = NETSH_WLAN.format('disconnect')
CONNECT = 'connect {}'


class WiFiError(Exception):
    """Error for WiFi commands"""


class Interface():
    def __init__(self):
        self.name = None
        self.description = None
        self.guid = None
        self.physical_address = None
        self.state = None
        self.ssid = None
        self.bssid = None
        self.network_type = None
        self.radio_type = None
        self.authentication = None
        self.cipher = None
        self.connection_mode = None
        self.channel = None
        self.rx_rate = None
        self.tx_rate = None
        self.signal = None
        self.profile = None


class Profile():
    """Connection Profile info and creation"""


class Wifi():
    """Wifi state and commands"""
    def __init__(self):
        self.interface = self._load_interface()

    @staticmethod
    def _call(cmd: str):
        p = subprocess.Popen(cmd, shell=True,
                             stderr=subprocess.PIPE,
                             stdout=subprocess.PIPE)
        output, error = p.communicate()
        if error:
            raise WiFiError(error)
        return output

    def _load_interface(self):
        output = self._call(SHOW_INTERFACES)
        # parse output here
        return output

    def profiles(self):
        cmd = SHOW_PROFILE.format('')
        output = self._call(cmd)
        # parse output here
        self._profiles = output

    def networks(self):
        output = self._call(SHOW_NETWORKS)
        # parse output here
        self._networks = output

    def disconnect(self):
        self._call(DISCONNECT)

    def connect(self, **kwargs):
        if kwargs.keys() not in ('name', 'ssid', 'interface'):
            raise KeyError
        args = _flatten_kwargs(kwargs)
        self._call(CONNECT.format(args))

