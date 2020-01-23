import os
from winwifi import Wifi, WiFiError, Interface, Profile

import pytest

DIR = os.path.dirname(__file__)
TEST_XML = os.path.join(DIR, 'test_profile.xml')


def test_wifi_interface():
    """Basic __init__ behvaior"""
    wifi = Wifi()
    interface = wifi.interface
    assert isinstance(interface, Interface)


def test_call_error():
    """Call resulting in error raises WifiError"""
    with pytest.raises(WiFiError):
        Wifi._call('foobarCall')


def test_call_no_error():
    assert isinstance(Wifi._call('netsh wlan ?'), str)


def test_interface():
    wifi = Wifi()
    for attr in ('name', 'description', 'guid', 'physical_address', 'state'):
        assert wifi.interface.__dict__.get(attr)


def test_interface_init():
    wifi = Wifi()
    for attr in ('name', 'description', 'guid', 'physical_address', 'state'):
        assert wifi.interface.__dict__.get(attr)


def test_profile():
    '''Profile class constructors'''
    name = "test network"
    ssid = 'test_ssid_01'
    authentication = "WPA2PSK"
    encryption = "AES"
    password = "testpassphrase"
    profile = Profile(name=name, ssid=ssid, authentication=authentication,
                      encryption=encryption, password=password)
    assert profile.name == name
    assert profile.ssid == ssid
    assert profile.authentication == authentication
    assert profile.encryption == encryption
    assert profile.password == password
    # Test name defaults to ssid value if not provided
    profile = Profile(ssid=ssid, authentication=authentication,
                      encryption=encryption, password=password)
    assert profile.name == ssid


def test_profile_to_xml():
    with open(TEST_XML, 'r') as infile:
        test_profile_xml = infile.read()
    profile = Profile(name='TEST NAME',
                      ssid='TEST SSID',
                      authentication='WPA2PSK',
                      encryption='AES',
                      password='testpassphrase')
    output_xml = profile.to_xml()
    with open(output_xml, 'r') as infile:
        output_profile_xml = infile.read()
    assert test_profile_xml == output_profile_xml  # Generated profile as expected


def test_add_del_profile():
    wifi = Wifi()
    profile = Profile(name='TEST NAME',
                      ssid='TEST SSID',
                      authentication='WPA2PSK',
                      encryption='AES',
                      password='testpassphrase')
    wifi.add_profile(profile)
    assert profile.name in wifi.profiles  # Profile added

    wifi.delete_profile(profile)  # Delete with Profile instance
    assert profile.name not in wifi.profiles

def test_add_del_profile_str():
    wifi = Wifi()
    profile = Profile(ssid='TEST NAME',
                    authentication='WPA2PSK',
                    encryption='AES',
                    password='testpassphrase')
    xml_profile = profile.to_xml()
    wifi.add_profile(xml_profile)
    assert profile.name in wifi.profiles  # Profile added

    wifi.delete_profile(profile.name)  # Delete with str name
    assert profile.name not in wifi.profiles
