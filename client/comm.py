"""Methods related to communication with BFTList nodes."""

# standard
import http.client
import requests
import json
import time
import asyncio
# from threading import Thread

# local
from node import get_nodes

nodes = get_nodes()


def build_payload(client_id, op, args):
    """Builds a request object to be sent to all BFTList nodes."""
    return {
        "client_id": client_id,
        "timestamp": int(time.time()),
        "operation": {
            "type": op,
            "args": args
        }
    }


async def send_to_node(node_id, payload):
    """
    Sends the given payload as a POST request to a Node.

    Tries to send the request up to 5 times with 1 second interval, will
    quit if 5 failed attempts is reached.
    """
    # if type(node_id) == "Node":
    #     node_id = node_id.id
    if type(node_id) == int:
        node = nodes[node_id]
    else:
        node = node_id
    url = f"http://{node.ip}:{node.api_port}/inject-client-req"
    requests.post(url, json=payload)
    return


async def broadcast(payload, nodes=get_nodes("../hosts.txt")):
    """Broadcast the request to all running BFTList nodes."""
    tasks = []
    for _, node in nodes.items():
        tasks.append(send_to_node(node, payload))
    await asyncio.gather(*tasks)
    return


def get_state_for_node(node_id):
    data = requests.get(f"http://localhost:400{node_id}/data").json()
    return data["REPLICATION_MODULE"]["rep_state"]
