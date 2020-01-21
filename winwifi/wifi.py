'''Wrapper commands for Windows netsh wlan utility

Copyright (c) 2020 Alex Puffer. All rights reserved.

This work is licensed under the terms of the MIT license.  
For a copy, see <https://opensource.org/licenses/MIT>.
'''

import os
import re
import subprocess
from typing import NamedTuple, Union

NETSH_WLAN = 'netsh wlan {}'
SHOW = NETSH_WLAN.format('show {}')
SHOW_NETWORKS = SHOW.format('networks')
SHOW_PROFILE = SHOW.format('profile {}')
SHOW_INTERFACES = SHOW.format('interface')
DISCONNECT = NETSH_WLAN.format('disconnect')
CONNECT = NETSH_WLAN.format('connect {}')
ADD_PROFILE = NETSH_WLAN.format('add profile filename={}')
DEL_PROFILE = NETSH_WLAN.format('delete profile {}')

PATH = os.path.realpath(os.path.dirname(__file__))
XML_PROFILE = os.path.join(PATH, '{}.xml')
XML_TEMPLATE = XML_PROFILE.format('wlan_profile_template.xml')


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


class Network(NamedTuple):
    ssid: str
    type_: str
    authentication: str
    encryption: str

class Profile():
    """Connection Profile info and creation"""
    def __init__(self, ssid,
                 authentication='', encryption='', password=''):
        self.ssid = ssid
        self.authentication = authentication
        self.encryption = encryption
        self.password = password
        self._path = None

    def to_xml(self, filename=None):
        if filename is None:
            filename = self.ssid
        with open(XML_TEMPLATE, 'r') as infile:
            template = infile.read()
            output = template.format(ssid=self.ssid,
                                     authentication=self.authentication,
                                     encryption=self.encryption,
                                     password=self.password)
        self.path = XML_PROFILE.format(filename)
        with open(self._path, 'w') as outfile:
            outfile.write(output)
        return self._path

    def _clear_xml(self):
        os.remove(self._path)
        self._path = None


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
        return output.decode()

    def connected(self):
        ssid = self.interface.get('SSID')
        if ssid:
            return True
        return False

    def _load_interface(self):
        output = self._call(SHOW_INTERFACES)
        return self._parse_interfaces(output)
        return output

    def _parse_interfaces(self, interface_result: str):
        # TODO: if no cards? if 2+ cards?
        result = interface_result.split('\r\n\r\n')[1].split('\n')
        result = [x.split(' : ') for x in result]
        return {k.strip(): v.strip() for k, v in result}

    def profiles(self):
        cmd = SHOW_PROFILE.format('')
        output = self._call(cmd)
        return self._parse_profiles(output)

    def networks(self):
        output = self._call(SHOW_NETWORKS)
        # parse output here
        return self._parse_networks(output)

    def _parse_networks(self, networks_result: str):
        regex = r'ssid.*:\s(.*)\n.*type.*:\s(.*)\s\n.*authentication.*:\s(.*)\s\n.*encryption.*:\s(.*)\s\n'
        results = re.findall(regex, networks_result, re.IGNORECASE)  # list of tuples
        return [Network(*x) for x in results]

    def disconnect(self):
        self._call(DISCONNECT)

    def connect(self, profile: Union[Profile, str]):
        """Connect to network

        Args:
            profile (Union[Profile, str]): str profile name if already loaded
                                           Profile if not already loaded
        """
        if isinstance(profile, str):
            self._call(CONNECT.format(profile))
        elif isinstance(profile, Profile):
            self.add_profile(profile)
            self._call(CONNECT.format(profile.ssid))
        else:
            raise TypeError("profile must be Profile or str")

    def add_profile(self, profile: Union[Profile, str]):
        """Add profile to netsh (permanent)

        Args:
            profile (Union[Profile, str]): Profile obj or
                str file path of .xml profile
        """
        if isinstance(profile, str):
            self._call(ADD_PROFILE.format(profile))
        elif isinstance(profile, Profile):
            filename = profile.to_xml()
            self._call(ADD_PROFILE.format(filename))
            profile._clear_xml()

    def delete_profile(self, profile: Union[Profile, str]):
        if isinstance(profile, Profile):
            profile = profile.name
        if profile not in self.profiles:
            self._call(DEL_PROFILE.format(profile)

    def _parse_profiles(self, profile_result: str):
        return re.findall(' : (.*\n)', profile_result)
