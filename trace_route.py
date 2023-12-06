from flask import Flask, request, jsonify
import socket
from scapy.all import *
import threading

app = Flask(__name__)

def traceroute(destination, max_hops=30, timeout=2):
    destination_ip = socket.gethostbyname(destination)
    port = 33434
    ttl = 1
    results = []

    while True:
        ip_packet = IP(dst=destination, ttl=ttl)
        udp_packet = UDP(dport=port)
        packet = ip_packet / udp_packet

        reply = sr1(packet, timeout=timeout, verbose=0)

        if reply is None:
            results.append({"ttl": ttl, "ip": "*"})
        elif reply.type == 3:
            results.append({"ttl": ttl, "ip": reply.src})
            break
        else:
            results.append({"ttl": ttl, "ip": reply.src})

        ttl += 1

        if ttl > max_hops:
            break

    return {destination: results}

@app.route('/traceroute', methods=['POST'])
def perform_traceroute():
    data = request.get_json()

    if 'destinations' not in data:
        return jsonify({"error": "Destinations parameter is required"}), 400

    destinations = data['destinations']
    max_hops = data.get('max_hops', 30)
    timeout = data.get('timeout', 2)

    threads = []
    results = []

    def run_traceroute(destination):
        result = traceroute(destination, max_hops=max_hops, timeout=timeout)
        results.append(result)

    for destination in destinations:
        thread = threading.Thread(target=run_traceroute, args=(destination,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return jsonify({"results": results})

if __name__ == '__main__':
    app.run(debug=True)


#   curl -X POST -H "Content-Type: application/json" -d "@payload.json" http://127.0.0.1:5000/traceroute
