'''Wrapper commands for Windows netsh wlan utility'''

import subprocess
from .utils import flatten_kwargs

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
        self._networks = None
        self._profiles = None

    @property
    def networks(self):
        if self._networks is None:
            self._load_networks()
        return self._networks

    @property
    def profiles(self):
        if self._profiles is None:
            self._load_profiles()
        return self._profiles

    @staticmethod
    def _netsh_wlan(cmd: str):
        p = subprocess.Popen(cmd, shell=True,
                             stderr=subprocess.PIPE,
                             stdout=subprocess.PIPE)
        output, error = p.communicate()
        if error:
            raise WiFiError(error)
        return output

    def _load_interface(self):
        output = self._netsh_wlan(SHOW_INTERFACES)
        # parse output here
        return output

    def _load_profiles(self):
        cmd = SHOW_PROFILE.format('')
        output = self._netsh_wlan(cmd)
        # parse output here
        self._profiles = output

    def _load_networks(self):
        output = self._netsh_wlan(SHOW_NETWORKS)
        # parse output here
        self._networks = output

    def disconnect(self):
        self._netsh_wlan(DISCONNECT)

    def connect(self, **kwargs):
        if kwargs.keys() not in ('name', 'ssid', 'interface'):
            raise KeyError
        args = flatten_kwargs(kwargs)
        self._netsh_wlan(CONNECT.format(args))

