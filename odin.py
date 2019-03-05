from conf import conf
from orchestrator.deployment import deploy
from orchestrator.connector import run_command
import api.pl as api
import logging
import sys
import json
import signal
import helpers.io as io

logger = logging.getLogger(__name__)


def setup_logging():
    """Configures the logging for Odin."""
    FORMAT = "\033[94mOdin.%(name)s ==> [%(levelname)s] : " + \
             "%(message)s\033[0m"
    logging.basicConfig(format=FORMAT, level=logging.INFO)


def generate_heimdall_sd(nodes):
    """
    Generates the service discovery file used by the Prometheus container
    in Heimdall.
    """
    path = conf.get_heimdall_sd_path()
    sd = {"targets": [], "labels": {"mode": "planetlab", "job": "bft-list"}}

    # add all instances on Docker host to targets (only in local mode)
    for i, node in enumerate(nodes):
        sd["targets"].append(f"{node['hostname']}:{6000 + i}")

    json_string = json.dumps([sd])
    io.write_file(path, json_string)
    return


def launch():
    pl_slice = conf.get_slice()
    node_count = conf.get_number_of_nodes()
    byz_count = conf.get_number_of_byzantine()

    nodes = api.get_nodes_for_slice(pl_slice, node_count)
    regular_nodes = nodes[byz_count:]
    byz_nodes = nodes[:byz_count]

    generate_heimdall_sd(regular_nodes + byz_nodes)
    deploy(regular_nodes, byz_nodes)


def cleanup():
    user = conf.get_slice()
    with open("hosts.txt") as f:
        for l in f.readlines():
            hostname = l.split(",")[1]
            run_command(hostname, f"pkill -u {user}")


def on_sig_term(signal, frame):
    logger.info("Quitting and killing all processes on PL nodes")
    cleanup()
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, on_sig_term)

    if len(sys.argv) > 1 and sys.argv[1] == "cleanup":
        cleanup()
    else:
        setup_logging()
        launch()
