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
        router_ip = router_list[router]['address']
    else:
        raise BadRequest(error_msg.badRouter)

    return router_ip, target

def validate_ip(addr):
    try:
        ipaddress.IPv4Address(addr)
    except ValueError:
        try:
            ipaddress.IPv6Address(addr)
        except ValueError:
            raise BadRequest(error_msg.badTargetAddr) 

@app.errorhandler(BadRequest)
def handle_bad_request(error):
    payload = dict(error.payload or ())
    payload['status'] = error.status
    payload['message'] = error.message
    return jsonify(payload), 400

@app.route('/api/v1/routers', methods=['GET'])
def lg_routers():
    return jsonify(routers.get_routers_pub())

@app.route('/api/v1/route4', methods=['GET'])
def lg_route4():
    router_ip, target = get_input(request)

    try:
        ipaddress.IPv4Network(target)
    except ValueError:
        raise BadRequest(error_msg.badTarget4Net) 

    result = vyosApi(router_ip).route4(target)
    return jsonify(result)

@app.route('/api/v1/route6', methods=['GET'])
def lg_route6():
    router_ip, target = get_input(request)

    try:
        ipaddress.IPv6Network(target)
    except ValueError:
        raise BadRequest(error_msg.badTarget6Net) 

    result = vyosApi(router_ip).route6(target)
    return jsonify(result)

@app.route('/api/v1/ping', methods=['GET'])
def lg_ping():
    router_ip, target = get_input(request)

    validate_ip(target)

    result = vyosApi(router_ip).ping(target)
    return jsonify(result)

@app.route('/api/v1/traceroute', methods=['GET'])
def lg_traceroute():
    router_ip, target = get_input(request)

    validate_ip(target)

    result = vyosApi(router_ip).traceroute(target)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)
#    app.run(host='0.0.0.0', port=8081)
