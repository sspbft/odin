from api.auth import get_auth
from helpers.constants import NODE_HEALTHY
import xmlrpc.client as xc
import logging
import os

api_server = xc.ServerProxy("https://www.planet-lab.eu/PLCAPI/")
auth = get_auth()
logger = logging.getLogger(__name__)


def get_node_ids_for_slice(slice_name, count):
    logger.info(f"Querying PL API for nodes on slice {slice_name}")
    slices = api_server.GetSlices(auth, slice_name)
    if len(slices) == 0:
        logger.error(f"No slice with name {slice_name} could be found")
        return []
    return slices[0]["node_ids"]


def get_nodes_for_slice(slice_name, count):
    logger.info(f"Fetching nodes attachhed to {slice_name}")
    node_ids = get_node_ids_for_slice(slice_name, count)
    if len(node_ids) < count:
        raise ValueError(f"Only {len(node_ids)} nodes attached to slice" +
                         f"{slice_name}. {count} was requested.")
    nodes = []
    for n_id in node_ids:
        details = get_node_details(n_id)
        if is_node_healthy(details):
            nodes.append(details)
        else:
            logger.info(f"Found non-healthy node {details['hostname']}" +
                        f" with id {n_id}")

    if len(nodes) > count:
        nodes = nodes[:count]
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
    return (node_details["boot_state"] == NODE_HEALTHY and
            responding_to_ping(node_details["hostname"]))


def responding_to_ping(hostname):
    """Pings the specified hostname and returns if ping was successful."""
    return os.system(f"ping -c 1 {hostname}") == 0
