"""Example client script used to test the scalability of BFTList.

This script launches a configured amount of threads, each representing one
client. Each client sends a configured amount of requests to all nodes in
the system.
"""

import argparse
import asyncio

from threading import Thread
from comm import build_payload, broadcast
from node import get_nodes

# setup argparse
parser = argparse.ArgumentParser(description='BFTList client script.')
parser.add_argument("ID", help="index of this client script instance",
                    type=int)
parser.add_argument("NBR_OF_CLIENTS", help="total number of clients",
                    type=int)
parser.add_argument("REQS_PER_CLIENT",
                    help="requests to be sent for each client", type=int)
parser.add_argument("HOSTS_PATH", help="path to PlanetLab hosts file")


async def launch_client(client_id, reqs_to_send, nodes):
    """TODO write me."""
    print(f"Launching client {client_id}")

    for i in range(0, reqs_to_send):
        payload = build_payload(client_id, "APPEND", client_id + i)
        await broadcast(payload, nodes)
    return


async def main():
    args = parser.parse_args()
    nodes = get_nodes(args.HOSTS_PATH)
    n = len(nodes)
    client_count = int(args.NBR_OF_CLIENTS / n)
    i = args.ID * client_count

    tasks = []
    for i in range(i, i + client_count):
        t = launch_client(i * 100, args.REQS_PER_CLIENT, nodes)
        tasks.append(t)

    await asyncio.gather(*tasks)
    total_reqs = client_count * args.REQS_PER_CLIENT
    print(f"{total_reqs} reqs sent by {client_count} clients")

if __name__ == '__main__':
    asyncio.run(main())
