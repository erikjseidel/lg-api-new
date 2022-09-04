import flask
import ipaddress
import copy
from flask import Flask, request, jsonify
from modules import routers, error_msg
from modules.vyos_api import vyosApi

app = Flask(__name__)

class BadRequest(Exception):
    def __init__(self, message, status=400, payload=None):
        self.message = message
        self.status = status
        self.payload = payload

def get_input(request):
    if 'target' in request.args:
        target = request.args['target']
    else:
        raise BadRequest(error_msg.noTarget)

    if 'router' in request.args:
        router = request.args['router']
    else:
        raise BadRequest(error_msg.noRouter)

    router_list = routers.get_routers()
    if router in router_list:
        router_entry = router_list[router]
    else:
        raise BadRequest(error_msg.badRouter)

    return router_entry, target

def is_ipv4(addr):
    try:
        ipaddress.IPv4Address(addr)
    except ValueError:
        return False
    return True

def is_ipv6(addr):
    try:
        ipaddress.IPv6Address(addr)
    except ValueError:
        return False
    return True

def is_ipv4net(addr):
    try:
        ipaddress.IPv4Network(addr)
    except ValueError:
        return False
    return True

def is_ipv6net(addr):
    try:
        ipaddress.IPv6Network(addr)
    except ValueError:
        return False
    return True

@app.errorhandler(BadRequest)
def handle_bad_request(error):
    payload = dict(error.payload or ())
    payload['status'] = error.status
    payload['message'] = error.message
    return jsonify(payload), 400

@app.route('/api/v1/routers', methods=['GET'])
def lg_routers():
    return jsonify(routers.get_routers_pub())

@app.route('/api/v1/route', methods=['GET'])
def lg_route():
    router_entry, target = get_input(request)

    if is_ipv6net(target):
        result = vyosApi(router_entry['address']).route6(target)
        return jsonify(result)
    elif is_ipv4net(target):
        result = vyosApi(router_entry['address']).route4(target)
        return jsonify(result)
    else:
        raise BadRequest(error_msg.badTargetNet)

@app.route('/api/v1/ping', methods=['GET'])
def lg_ping():
    router_entry, target = get_input(request)

    if is_ipv6(target):
        result = vyosApi(router_entry['address']).ping(target, router_entry['v6-source'])
        return jsonify(result)
    elif is_ipv4(target):
        result = vyosApi(router_entry['address']).ping(target, router_entry['v4-source'])
        return jsonify(result)
    else:
        raise BadRequest(error_msg.badTargetAddr)


@app.route('/api/v1/traceroute', methods=['GET'])
def lg_traceroute():
    router_entry, target = get_input(request)

    if is_ipv6(target) or is_ipv4(target):
        result = vyosApi(router_entry['address']).traceroute(target)
        return jsonify(result)
    else:
        raise BadRequest(error_msg.badTargetAddr)
