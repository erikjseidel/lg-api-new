import copy

#
#  Currently only VyOS routers + API available
#
lg_routers = {
        "ewr": { "address": "192.0.2.1", "v4-source": "192.0.2.22", "v6-source": "2001:db8::22", "type": "VyOS", "description": "Dallas, TX"},
        "lhr": { "address": "192.0.2.2", "v4-source": "192.0.2.20", "v6-source": "2001:db8::20", "type": "VyOS", "description": "Kansas City, MO"},
}

#
#  Public list: Router addresses not shown.
#
lg_routers_pub = copy.deepcopy(lg_routers)
for key in lg_routers_pub:
    lg_routers_pub[key].pop('address', None)

def get_routers():
    return lg_routers

def get_routers_pub():
    return lg_routers_pub
