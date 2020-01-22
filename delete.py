from winwifi import Wifi


wifi = Wifi()

networks = wifi.networks()
print(networks)

interface = wifi.interface
print(interface)
