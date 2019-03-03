from conf import conf
import logging
import subprocess

logger = logging.getLogger(__name__)
SSH_KEY_PATH = conf.get_ssh_key_path()
SLICE = conf.get_slice()


def transfer_files(hostname, files, target_dir):
    logger.info(f"Transferring files {files} to {hostname}:{target_dir}")

def run_command(hostname, cmd):
    logger.info(f"Running command {cmd} on {hostname}")
    cmd_string = f"ssh -l {SLICE} -i {SSH_KEY_PATH} {hostname} {cmd}"
    process = subprocess.Popen(cmd_string.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    logger.info(f"Output of command: {output}")