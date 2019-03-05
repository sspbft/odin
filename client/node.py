"""This module contains code modelling nodes in the distributed system."""

import os


class Node:
    """Class representing a node."""

    def __init__(self, id, hostname, ip, port):
        """Initializes a node."""
        self.id = int(id)
        self.hostname = hostname
        self.ip = ip
        self.port = int(port)
        self.api_port = int(os.getenv("API_PORT", 4000)) + self.id

    def __str__(self):
        return f"{self.hostname},{self.ip}:{self.port}"


def get_nodes():
    """Parses nodes file to a dict of nodes such that dct[id] = node."""
    if not os.path.isfile("../hosts.txt"):
        raise ValueError(f"Could not find hosts file in Odin root dir")
    with open("../hosts.txt") as f:
        lines = [x.strip().split(",") for x in f.readlines()]
        nodes = {}
        for l in lines:
            nodes[int(l[0])] = Node(id=l[0], hostname=l[1], ip=l[2], port=l[3])
        return nodes