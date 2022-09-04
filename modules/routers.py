import copy

#
#  Currently only VyOS routers + API available
#
lg_routers = {
        "dfw": { "address": "23.181.64.227", "v4-source": "23.181.64.227", "v6-source": "2620:136:a009:af00::227", "type": "VyOS", "description": "Dallas, TX"},
        "mci": { "address": "23.181.64.228", "v4-source": "23.181.64.228", "v6-source": "2620:136:a009:af00::228", "type": "VyOS", "description": "Kansas City, MO"},
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
