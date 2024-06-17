import copy
import settings

#
#  Public list: Router addresses not shown.
#
lg_routers_pub = copy.deepcopy(settings.lg_routers)
for key in lg_routers_pub:
    lg_routers_pub[key].pop('address', None)


def get_routers():
    return settings.lg_routers


def get_routers_pub():
    return lg_routers_pub
