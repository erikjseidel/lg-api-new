import configparser
import datetime
from netmiko import ConnectHandler

config = configparser.ConfigParser()
config.read(".napalmrc")


class vyosApi:

    vyos_router = {
        "device_type": "vyos",
        "host": None,
        "username": config.get("napalm", "username"),
        "password": config.get("napalm", "password"),
        "port": 22,
    }

    def ping(self, target, src_ip=None, count=5):

        if src_ip == None:
            command = "ping %s count %s" % (target, count)
        else:
            command = "ping %s source-address %s count %s" % (target, src_ip, count)

        return self.__runner(target, command)

    def traceroute(self, target):
        command = "traceroute %s" % target
        return self.__runner(target, command)

    def route4(self, target):
        command = "show bgp ipv4 %s" % target
        return self.__runner(target, command)

    def route6(self, target):
        command = "show bgp ipv6 %s" % target
        return self.__runner(target, command)

    def __runner(self, target, command):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        net_connect = ConnectHandler(**self.vyos_router)
        output = net_connect.send_command(command, read_timeout=120)

        return {
            "command": command,
            "timestamp": timestamp,
            "output": output,
        }

    def __init__(self, router):
        self.vyos_router['host'] = router
