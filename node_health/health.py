from threading import Thread
import api.pl as api
import logging

logger = logging.getLogger(__name__)

healthy_nodes = []
faulty_nodes = []


def check_node(node):
    hostname = node["hostname"]
    node_id = node["node_id"]
    logger.info(f"Checking node {hostname} to see if it is healthy")
    n_str = f"{node_id},{hostname}"
    if api.is_node_healthy(node):
        healthy_nodes.append(n_str)
    else:
        faulty_nodes.append(n_str)


def find_healthy_nodes():
    nodes = api.get_all_nodes()

    threads = []
    logger.info(f"Checking {len(nodes)} nodes to see if they're healthy")
    for n in nodes:
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
