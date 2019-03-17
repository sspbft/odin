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

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    """Main entrypoint for running clients distributed."""

    if len(sys.argv) != 3:
        logger.error(f"Run as python run_clients_distributed [clients] [reqs]")

    nbr_of_clients = sys.argv[1]
    reqs_per_client = sys.argv[2]
