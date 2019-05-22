from api.auth import get_auth
from conf import conf
from helpers import io
from helpers.constants import (API_URL, NODE_CMD_THRESHOLD,
                               NODE_HEALTHY, HEALTH_CHECK_PORT)
import xmlrpc.client as xc
import logging
import time
import os
import sys
import orchestrator.connector as conn
import socket
import ssl

api_server = xc.ServerProxy(API_URL, context=ssl._create_unverified_context())
auth = get_auth()
logger = logging.getLogger(__name__)


def get_node_ids_for_slice(slice_name):
    logger.info(f"Querying PL API for nodes attached to slice {slice_name}")
    slices = api_server.GetSlices(auth, slice_name)
    if len(slices) == 0:
        logger.error(f"No slice with name {slice_name} could be found")
        return []
    return slices[0]["node_ids"]


def get_nodes_for_slice(slice_name, count):
    logger.info(f"Fetching nodes attached to {slice_name}")
    node_ids = get_node_ids_for_slice(slice_name)
    if len(node_ids) < count:
        raise ValueError(f"Only {len(node_ids)} nodes attached to slice" +
                         f"{slice_name}. {count} was requested.")
    nodes = []
    blacklisted_nodes = conf.get_blacklisted_hosts()

    logger.info(f"Found nodes for {slice_name}: {node_ids}")

    for n_id in node_ids:
        details = get_node_details(n_id)
        hostname = details["hostname"]

        if hostname in blacklisted_nodes:
            logger.warning(f"Found blacklisted node {hostname}, skipping")
            continue

        if is_node_healthy(details):
            nodes.append(details)
            if len(nodes) == count:
                return nodes
        else:
            logger.warning(f"Found non-healthy node {hostname}" +
                           f" with id {n_id}, skipping")

    if len(nodes) < count:
        logger.error(f"Only found {len(nodes)}/{count} nodes, aborting")
        sys.exit(1)

    logger.info(f"Found {count} healthy nodes for slice {slice_name}")
    return nodes


def get_node_details(node_id):
    logger.info(f"Querying PL API for details of node {node_id}")
    nodes = api_server.GetNodes(auth, node_id)
    if len(nodes) == 0:
        logger.error(f"No node with id {node_id} could be found")
        return {}
    return nodes[0]


def get_all_nodes():
    logger.info("Checking ALL nodes on PlanetLab to see which are healthy")
    return api_server.GetNodes(auth)


def is_node_healthy(node_details):
    """Health check for a PlanetLab node."""
    hostname = node_details["hostname"]
    logger.info(f"Checking if {hostname} is healthy")

    # basic healthchecks
    if not node_details["boot_state"] == NODE_HEALTHY:
        return False
    if not responding_to_ping(hostname):
        logger.info(f"Node {hostname} is not responding to pings")
        return False
    if not node_responds_within_threshold(hostname):
        logger.info(f"Node {hostname} is not responding within treshold")
        return False

    # transfer healthcheck file
    if conn.transfer_files(
        hostname,
        [io.get_abs_path("scripts/healthcheck.sh")],
        "~"
    ) != 0:
        logger.error(f"Could not transfer healthcheck script to {hostname}")
        return False

    # start healthcheck script in background on host
    if conn.run_command(
        hostname,
        "nohup sh ./healthcheck.sh &>/dev/null &"
    ) != 0:
        logger.error(f"Could not run healthcheck script on {hostname}")
        return False
    else:
        logger.info(f"Launched healthcheck script on {hostname}")

    i = 0
    connected = False
    while i < 10 and not connected:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((hostname, HEALTH_CHECK_PORT))
        connected = result == 0
        sock.close()

        if not connected:
            logger.warning(f"{hostname}:{HEALTH_CHECK_PORT} not responding")
        else:
            logger.info(f"{hostname}:{HEALTH_CHECK_PORT} responded!")
        time.sleep(1)
        i += 1

    # kill healthcheck server on host
    conn.run_command(hostname, f"sudo pkill -f 'sh healthcheck'")
    conn.run_command(hostname, f"sudo pkill -f 'nc -l'")

    if not connected:
        logger.warning(f"Could not connect to {hostname}:{HEALTH_CHECK_PORT}")
        return False

    logger.info(f"{hostname} is healthy!")
    return True


def node_responds_within_threshold(hostname):
    """Checks if the node can run a simple command within threshold s."""
    logger.info(f"Checking if {hostname} responds within threshold")
    return True
    # start_time = time.time()
    # conn.run_command(hostname, "ls /", timeout=15)
    # responding_within_threshold = time.time() - start_time < NODE_CMD_THRESHOLD
    # if not responding_within_threshold:
    #     logger.warning(f"{hostname} is not responding within threshold")
    # return responding_within_threshold


def is_online(hostname):
    """Checks if the host with hostname can access Internet 'fast'."""
    logger.info(f"Checking if {hostname} is online")
    is_online = conn.run_command(
        hostname,
        "curl -m 5 http://google.com",
        timeout=10
    ) == 0
    if not is_online:
        logger.warning(f"{hostname} is considered to be offline")
    return is_online


def responding_to_ping(hostname):
    """Pings the specified hostname and returns if ping was successful."""
    return os.system(f"ping -c 1 {hostname} > /dev/null") == 0


def set_nodes_for_slice(nodes, slice_name=conf.get_slice()):
    api_server.UpdateSlice(auth, slice_name, {"nodes": nodes})
    logger.info(f"Set nodes {nodes} for slice {slice_name}")


def add_all_nodes_to_slice(slice_name=conf.get_slice()):
    """Adds ALL nodes on PlanetLab to slice."""
    nodes = get_all_nodes()
    nodes = list(map(lambda n: n["node_id"], nodes))
    set_nodes_for_slice(nodes)
