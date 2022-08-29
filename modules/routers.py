import copy

#
#  Currently only VyOS routers + API available
#
lg_routers = {
        "lhr": { "address": "192.0.2.1", "type": "VyOS", "description": "London, UK"},
        "ewr": { "address": "192.0.2.2", "type": "VyOS", "description": "New York, NY"},
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
