"""Example client script used to test the scalability of BFTList.

This script launches a configured amount of threads, each representing one
client. Each client sends a configured amount of requests to all nodes in
the system.
"""

import argparse
import asyncio
import time

from node import get_nodes
from comm import broadcast, build_payload, get_data_for_node

# setup argparse
parser = argparse.ArgumentParser(description='BFTList client script.')
parser.add_argument("ID", help="index of this client script instance",
                    type=int)
parser.add_argument("NBR_OF_CLIENTS", help="total number of clients",
                    type=int)
parser.add_argument("REQS_PER_CLIENT",
                    help="requests to be sent for each client", type=int)


async def req_applied(req, nodes):
    """Blocks until the supplied request is the last execed req on >= 1 nodes"""
    applied = False
    # arg = req["operation"]["args"]
    client_id = req["client_id"]
    while not applied:
        for n_id in nodes:
            n_data = get_data_for_node(nodes[n_id])
            last_req = n_data["REPLICATION_MODULE"]["last_req"]
            if len(last_req) < client_id or last_req[client_id] == -1:
                continue
            last_execed = last_req[client_id]["request"]["client_request"]
            if last_execed["timestamp"] == req["timestamp"]:
                applied = True
                break
    return


async def run_client(client_id, reqs_count, nodes):
    """Send reqs_count reqs to all nodes with specified client_id."""
    start_val = client_id * 100
    for r in range(start_val, start_val + reqs_count):
        req = build_payload(client_id, r)
        await broadcast(req)
        await req_applied(req, nodes)
    return


async def main():
    args = parser.parse_args()
    nodes = get_nodes()
    n = len(nodes)
    client_count = int(args.NBR_OF_CLIENTS / n)

    tasks = []
    start_time = time.time()
    for i in range(args.ID * 100, args.ID * 100 + client_count):
        t = run_client(i, args.REQS_PER_CLIENT, nodes)
        tasks.append(t)
    await asyncio.gather(*tasks)
    count = client_count * args.REQS_PER_CLIENT
    end_time = time.time()
    print(f"Process {args.ID}: {count} reqs injected by {client_count} " +
          f"clients in {end_time - start_time} s")

if __name__ == '__main__':
    asyncio.run(main())
