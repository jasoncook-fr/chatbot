import network
import utime as time

ssid = ["ssid_1","ssid_2"]
password = ["password_1","password_2"]
networks = [ssid,password]

def connect():
    #connect to local wireless network
    station = network.WLAN(network.STA_IF)
    def __conn__(ssid, password):
        if not station.isconnected():
            print("Attempting connection to '%s'..." % ssid)
            # Connect
            station.connect(ssid, password)
            # Wait till connection is established
            for i in range(10):
                if station.isconnected():
                    #wlan.ifconfig(ipaddress, netmask, gateway, dns)
                    break
                time.sleep_ms(500)
            else:
                return None

            print("Now connected to '%s'." % ssid)
        else:
            print('Already Connected.')

        return station

    print("length of networks is: ", len(networks[0]))
    for x in range(len(networks[0])):
        station.active(True)
        #disconnect in case we are already connected
        station.disconnect()
        wlan = __conn__(networks[0][x],networks[1][x])
        if wlan:
            ipData = station.ifconfig()
            print(ipData)
            return ipData[0], ipData[2]
            break
    else:
        print("No network found.")
