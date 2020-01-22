class auth():
    OPEN = "open"  # Open 802.11
    SHARED = "shared"  # Shared 802.11
    WPA = "WPA"  # WPA-Enterprise 802.11
    WPAPSK = "WPAPSK"  # WPA-Personal 802.11
    WPA2 = "WPA2"  # WPA2-Enterprise 802.11
    WPA2PSK = 'WPA2PSK'  # WPA2-Personal 802.11


class encryption():
    NONE = 'none'
    WEP = 'WEP'
    TKIP = 'TKIP'
    AES = 'AES'

DEFAULT_AUTH = auth.WPA2PSK
DEFAULT_ENCRYPTION = encryption.AES
