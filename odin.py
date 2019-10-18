"""Main entrypoint script for Odin CLI."""

from conf import conf
from orchestrator.deployment import deploy
from orchestrator.connector import run_command
import api.pl as api
import logging
import sys
import subprocess
import json
import signal
import helpers.io as io
import helpers.ps as ps
from shutil import which
import argparse
from helpers.constants import (CLEANUP, DEPLOY)

logger = logging.getLogger(__name__)
parser = argparse.ArgumentParser(
    description="CLI for deploying applications to PlanetLab")
parser.add_argument("mode",
                    help="either [deploy], [cleanup] or [find_healthy]")
parser.add_argument("-b", "--git-branch", help="the git branch to deploy")
parser.add_argument("-nss", "--non-selfstab",
                    help="run application without self-stabilization",
                    action="store_true")
parser.add_argument("-f", "--hosts-file", help="file containing hosts")
parser.add_argument("-r", "--reuse-hosts", help="re-use hosts from last " +
                    "deployment", action="store_true")
parser.add_argument("-ss", "--starting-state", help="path to " +
                    "start_state.json for state injection")
parser.add_argument("-s", "--scale", help="number of virtual instances on " +
                    "each PL node", type=int, default=1)
parser.add_argument("-rs", "--run-sleep", help="s to sleep in module.run")
parser.add_argument("-c", "--clients", help="number of clients", type=int,
                    default=6)


def setup_logging():
    """Configures the logging for Odin."""
    FORMAT = "\033[94mOdin.%(name)s ==> [%(levelname)s] : " + \
             "%(message)s\033[0m"
    logging.basicConfig(format=FORMAT, level=logging.INFO)


def generate_heimdall_sd(nodes, scale_factor):
    """Generate Heimdall SD file

    Generates the service discovery file used by the Prometheus container
    in Heimdall.
    """
    path = conf.get_heimdall_sd_path()
    app_folder = conf.get_app_folder()
    sd = {"targets": [], "labels": {"mode": "planetlab", "job": app_folder }}
    sd2 = {"targets": [], "labels": {"mode": "planetlab",
           "job": "node-exporter"}}

    # add all instances on Docker host to targets (only in local mode)
    for i, node in enumerate(nodes):
        instance_id = i * scale_factor
        for j in range(scale_factor):
            sd["targets"].append(f"{node['hostname']}:{3000 + instance_id}")
            sd2["targets"].append(f"{node['hostname']}:9111")
            instance_id += 1

    json_string = json.dumps([sd, sd2])
    io.write_file(path, json_string)
    return


def launch(args):
    """Main entrypoint of Odin CLI"""
    pl_slice = conf.get_slice()
    node_count = conf.get_number_of_nodes()
    byz_count = conf.get_number_of_byzantine()

    if not args.reuse_hosts:
        logger.info("Fetching nodes for slice")
        nodes = api.get_nodes_for_slice(pl_slice, node_count)
    else:
        logger.info("Re-using nodes from hosts.txt")
        if not io.exists("hosts.txt"):
            logger.error("Can't re-use hosts from non-existing hosts.txt")
            sys.exit(1)
        # parse hosts file
        with open("hosts.txt") as f:
            lines = [x.rstrip() for x in f.readlines()]
            nodes = [{"id": l.split(",")[0], "hostname": l.split(",")[1]}
                     for l in lines]

    regular_nodes = nodes[byz_count:]
    byz_nodes = nodes[:byz_count]

    if io.exists(conf.get_heimdall_sd_path()):
        generate_heimdall_sd(byz_nodes + regular_nodes, args.scale)

    setup_heimdall()
    deploy(byz_nodes, regular_nodes, args)


def cleanup():
    """Helper function that kills all processes started by on PL hosts."""
    user = conf.get_slice()
    with open("hosts.txt") as f:
        for l in f.readlines():
            hostname = l.split(",")[1]
            run_command(hostname, f"pkill -u {user}")


def on_sig_term(signal, frame):
    """SIGTERM interrup handler that kills a deployment"""
    logger.info("Quitting and killing all processes on PL nodes")
    cleanup()
    ps.kill_all_subprocesses()
    sys.exit(0)


def setup_heimdall(debug=False):
    """
    Starts the Heimdall service.

    Given that docker-compose is available and path to Heimdall project root
    is specified, this methods starts heimdall as a subprocess.
    """
    heimdall_root = conf.get_heimdall_root()
    if heimdall_root is not None and io.exists(heimdall_root):
        logger.info("Launching Heimdall")
        dc = "docker-compose"
        if which(dc) is None:
            raise EnvironmentError("Can't find docker-compose binary.")
        p = subprocess.Popen(f"rm -r ./prometheus/data && {dc} down && " +
                             f"{dc} up > /dev/null", shell=True,
                             cwd=heimdall_root)
        ps.add_subprocess_pid(p.pid)
        logger.info(f"Starting Heimdall with PID {p.pid}")
        logger.info("Grafana can be found on http://localhost:6060")
    else:
        logger.info("Heimdall not configured correctly, skipping")


if __name__ == "__main__":
    """Main entrypoint for Odin."""

    setup_logging()

    # parse args
    args = parser.parse_args()
    if args.git_branch:
        conf.set_application_git_branch(args.git_branch)
    if args.run_sleep:
        conf.set_run_sleep(args.run_sleep)
    mode = args.mode

    if args.mode == CLEANUP:
        cleanup()
    elif args.mode == DEPLOY:
        # register SIGINT handler
        signal.signal(signal.SIGINT, on_sig_term)
        launch(args)
    else:
        logger.error(f"Invalid mode {mode}, check help")
        sys.exit(1)
