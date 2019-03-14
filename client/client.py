"""Example client script used to test the scalability of BFTList.

This script launches a configured amount of threads, each representing one
client. Each client sends a configured amount of requests to all nodes in
the system.
"""

import argparse
import asyncio

import comm
from node import get_nodes

# setup argparse
parser = argparse.ArgumentParser(description='BFTList client script.')
parser.add_argument("ID", help="index of this client script instance",
                    type=int)
parser.add_argument("NBR_OF_CLIENTS", help="total number of clients",
                    type=int)
parser.add_argument("REQS_PER_CLIENT",
                    help="requests to be sent for each client", type=int)


async def send_reqs_to_node(node_id, reqs):
    print(f"Sending {len(reqs)} reqs to node {node_id}")
    for req in reqs:
        await send_req(node_id, req)
    return

async def send_req(node_id, payload):
    print(f"Sending req {payload} to {node_id}")
    await comm.send_to_node(node_id, payload)
    print("Here")

    # wait for request to be applied before returning
    applied = False
    while not applied:
        state = comm.get_state_for_node(node_id)
        print(payload["operation"]["args"], state)
        if payload["operation"]["args"] in state:
            print(f"Req {payload} applied on node {node_id}")
            applied = True
        else:
            await asyncio.sleep(0.25)



async def launch_client(client_id, nbr_of_reqs_to_send, nodes):
    """TODO write me."""
    print(f"Launching client with ID {client_id}")

    # one queue for each node
    reqs = {n_id: [] for n_id in nodes}

    # add all requests to corresponding queue for each node
    for i in range(0, nbr_of_reqs_to_send):
        payload = comm.build_payload(client_id, "APPEND", client_id + i)
        for n_id in reqs:
            reqs[n_id].append(payload)

    tasks = []
    for n_id in reqs:
        tasks.append(send_reqs_to_node(n_id, reqs[n_id]))
    await asyncio.gather(*tasks)
    print("All requests are sent")
    return


async def main():
    args = parser.parse_args()
    nodes = get_nodes()
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
