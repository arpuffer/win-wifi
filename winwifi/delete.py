from winwifi import Wifi


wifi = Wifi()

networks = wifi.networks()
print(networks)
