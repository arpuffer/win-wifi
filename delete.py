from winwifi import Wifi, WiFiError


def test():
    a = Wifi()
    print(a.interface)


if __name__ == '__main__':
    test()
