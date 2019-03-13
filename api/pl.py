from api.auth import get_auth
from conf import conf
from helpers import io
from helpers.constants import API_URL, NODE_CMD_THRESHOLD, NODE_HEALTHY
import xmlrpc.client as xc
import logging
import time
import os
import sys
import orchestrator.connector as conn
import socket

api_server = xc.ServerProxy(API_URL)
auth = get_auth()
logger = logging.getLogger(__name__)


def get_node_ids_for_slice(slice_name):
    logger.info(f"Querying PL API for nodes on slice {slice_name}")
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

    logger.info(f"found nodes: {node_ids}")

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


def is_node_healthy(node_details):
    """Health check for a PlanetLab node."""
    hostname = node_details["hostname"]

    # basic healthchecks
    if not node_details["boot_state"] == NODE_HEALTHY:
        return False
    if not responding_to_ping(hostname):
        return False
    if not node_responds_within_threshold(hostname):
        return False

    # transfer healthcheck file
    if conn.transfer_files(
        hostname,
        [io.get_abs_path("scripts/healthcheck.sh")],
        "~"
    ) != 0:
        return False

    # start healthcheck script in background on host
    if conn.run_command(
        hostname,
        "nohup sh ./healthcheck.sh &>/dev/null &"
    ) != 0:
        return False

    i = 0
    connected = False
    while i < 10 and not connected:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((hostname, 8080))
        connected = result == 0
        sock.close()
        if not connected:
            logger.info(f"{hostname}:8080 not responding, re-trying")
        time.sleep(1)
        i += 1

    # kill healthcheck server
    conn.run_command(hostname, f"sudo pkill -f 'sh healthcheck'")
    conn.run_command(hostname, f"sudo pkill -f 'nc -l'")

    if not connected:
        logger.info(f"Could not connect to {hostname}:8080")
        return False

    logger.info(f"Connection attempt to {hostname}:8008 successful")
    return True


def node_responds_within_threshold(hostname):
    """Checks if the node can run a simple command within threshold s."""
    start_time = time.time()
    conn.run_command(hostname, "ls /", timeout=10)
    responding_within_threshold = time.time() - start_time < NODE_CMD_THRESHOLD
    if not responding_within_threshold:
        logger.warning(f"{hostname} is not responding within threshold")
    return responding_within_threshold


def is_online(hostname):
    """Checks if the host with hostname can access Internet 'fast'."""
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
    return os.system(f"ping -c 1 {hostname}") == 0
