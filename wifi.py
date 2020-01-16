import subprocess
from utils import flatten_kwargs

NETSH_WLAN = 'netsh wlan {}'
SHOW_PROFILE = 'show profile {}'
DISCONNECT = 'disconnect {}'
CONNECT = 'connect {}'

class Interface():
    pass

class Profile():
    pass


class Wifi():
    def __init__(self):
        self.interfaces = []
        self.connections = []
        self.networks = []

    def profiles(self):

    def disconnect(self, arg=''):
        _netsh_wlan(DISCONNECT.format(arg))

    def connect(self, **kwargs):
        if kwargs.keys() not in ('name', 'ssid', 'interface'):
            raise KeyError
        args = flatten_kwargs(kwargs)
        _netsh_wlan(CONNECT.format(args))
