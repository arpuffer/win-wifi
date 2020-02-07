"""Wrapper commands for Windows netsh wlan utility

Copyright (c) 2020 Alex Puffer. All rights reserved.

This work is licensed under the terms of the MIT license.
For a copy, see <https://opensource.org/licenses/MIT>.
"""
import logging
import os
import re
import subprocess
from typing import List, NamedTuple, Union

NETSH_WLAN = "netsh wlan {}"
SHOW = NETSH_WLAN.format("show {}")
SHOW_NETWORKS = SHOW.format("networks")
SHOW_PROFILE = SHOW.format('profile "{}"')
SHOW_INTERFACES = SHOW.format("interface")
DISCONNECT = NETSH_WLAN.format("disconnect")
CONNECT = NETSH_WLAN.format('connect "{}"')
ADD_PROFILE = NETSH_WLAN.format('add profile filename="{}"')
DEL_PROFILE = NETSH_WLAN.format('delete profile "{}"')

PATH = os.path.realpath(os.path.dirname(__file__))
XML_PROFILE = os.path.join(PATH, "{}.xml")
XML_TEMPLATE = XML_PROFILE.format("profile_template")

logger = logging.getLogger(__name__)


class WiFiError(Exception):
    """Error for WiFi commands"""


class Interface:
    def __init__(self, **kwargs):
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
        self.receive_rate = None
        self.transmit_rate = None
        self.signal = None
        self.profile = None
        self.__dict__.update(kwargs)


class Network(NamedTuple):
    ssid: str
    type_: str
    authentication: str
    encryption: str


class Profile:
    """Connection Profile info and creation"""

    def __init__(self, ssid, name=None, authentication="", encryption="", password=""):
        self.ssid = ssid
        if name is None:
            self.name = ssid
        else:
            self.name = name
        self.authentication = authentication
        self.encryption = encryption
        self.password = password
        self._path = None

    def to_xml(self, filename=None):
        if filename is None:
            filename = self.name
        with open(XML_TEMPLATE, "r") as infile:
            template = infile.read()
            output = template.format(
                name=self.name,
                ssid=self.ssid,
                authentication=self.authentication,
                encryption=self.encryption,
                password=self.password,
            )
        self._path = XML_PROFILE.format(filename)
        with open(self._path, "w") as outfile:
            outfile.write(output)
        return self._path

    def _clear_xml(self):
        os.remove(self._path)
        self._path = None


class Wifi:
    """Wifi state and commands"""

    @property
    def interface(self) -> Interface:
        """Return first interface reported by 'netsh wlan show interface'.
        Typically, only 1 is reported.  If the system has multiple interfaces,
        only the first in the report is returned here.

        Returns:
            Interface:
        """
        output = self._call(SHOW_INTERFACES)
        iface = self._parse_interfaces(output)
        return Interface(**iface)

    @staticmethod
    def _call(cmd: str) -> str:
        """Makes a generic command line call with attention to the
        errors reported by netsh

        Args:
            cmd (str): full command string
            ('netsh wlan show interface', 'netsh wlan delete profile MYPROFILE')

        Raises:
            WiFiError: On any error generated by subprocess call
            WiFiError: For any netsh-specific error (parsed out of stdout)

        Returns:
            str: stdout from subprocess call
        """
        proc = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        logger.debug(cmd)
        output, error = proc.communicate()
        logger.debug(output.decode())
        if b"error" in output.lower() and b":" in output:
            raise WiFiError(output)
        if error:
            raise WiFiError(error)
        return output.decode()

    @property
    def connected(self) -> bool:
        """Report connection state

        Returns:
            bool: True if connected to a network, False otherwise
        """
        if self.interface.state == "connected":
            return True
        return False

    def _parse_interfaces(self, interface_result: str) -> dict:
        """
        Args:
            interface_result (str): [description]

        Returns:
            dict: [description]
        """
        # TODO: if no cards? if 2+ cards?
        output = {}
        result = interface_result.replace("(Mbps)", "").split("\r\n\r\n")[1].split("\r\n")
        result = [[x.strip() for x in y.split(" : ")] for y in result]
        for i, line in enumerate(result):
            if len(line) == 2:
                key, val = [x.strip() for x in line]
                output[key] = val.strip()
            elif len(line) == 1:
                output[result[i - 1][0]] += ", " + line[0].strip()
        output = {k.replace(" ", "_").lower(): v for k, v in output.items()}
        return output

    @property
    def profiles(self):
        cmd = SHOW_PROFILE.format("")
        output = self._call(cmd)
        return self._parse_profiles(output)

    def networks(self) -> List[Network]:
        """List all visible networks

        Returns:
            List[Network]
        """
        output = self._call(SHOW_NETWORKS)
        return self._parse_networks(output)

    def _parse_networks(self, networks_result: str):
        regex = r"ssid.*:\s(.*)\n.*type.*:\s(.*)\s\n.*authentication.*:\s(.*)\s\n.*encryption.*:\s(.*)\s\n"
        results = re.findall(regex, networks_result, re.IGNORECASE)  # List[tuple]
        return [Network(*x) for x in results]

    def disconnect(self):
        """Disconnect from any connected network"""
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
        """Remove profile from netsh (permanent)

        Args:
            profile (Union[Profile, str]): Profile obj or
                str file path of .xml profile
        """
        if isinstance(profile, Profile):
            profile = profile.name
        if profile in self.profiles:
            self._call(DEL_PROFILE.format(profile))

    def _parse_profiles(self, profile_result: str):
        result = re.findall(" : (.*\n)", profile_result)
        return [x.strip() for x in result]
