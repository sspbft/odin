"""Functions related to PlanetLab node health"""

from threading import Thread
from conf import conf
import api.pl as api
import logging

logger = logging.getLogger(__name__)

healthy_nodes = []
faulty_nodes = []


def check_node(node):
    """Checks a node to see if it is healthy."""
    hostname = node["hostname"]
    node_id = node["node_id"]
    logger.info(f"Checking node {hostname} to see if it is healthy")
    n_str = f"{node_id},{hostname}"
    if api.is_node_healthy(node):
        healthy_nodes.append(n_str)
    else:
        faulty_nodes.append(n_str)


def find_healthy_nodes():
    """Helper function that can be used to find healthy nodes on PlanetLab."""
    slc = conf.get_slice()
    old_nodes = api.get_node_ids_for_slice(slc)
    logger.info(f"Old nodes for {slc}: {old_nodes}")
    logger.info(f"Attaching all nodes to slice temporarily")
    all_nodes = api.get_all_nodes()
    node_ids = list(map(lambda n: n["node_id"], all_nodes))
    api.set_nodes_for_slice(node_ids)
    count = api.get_node_ids_for_slice(slc)
    logger.info(f"{conf.get_slice()} node has {count} nodes attached [temp]")

    threads = []
    logger.info(f"Checking {len(all_nodes)} nodes to see if they're healthy")
    for n in all_nodes:
        t = Thread(target=check_node, args=(n,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()

    logger.info("All nodes checked, writing result files in etc/")

    with open("etc/healthy_nodes.txt", "w+") as f:
        for n in healthy_nodes:
            f.write(f"{n}\n")

    with open("etc/faulty_nodes.txt", "w+") as f:
        for n in faulty_nodes:
            f.write(f"{n}\n")
    logger.info(f"Healthy node discovery done!")

    api.set_nodes_for_slice(old_nodes)
    logger.info(f"Nodes for slice reset to {old_nodes}")
