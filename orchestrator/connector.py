from conf import conf
import logging
import subprocess

logger = logging.getLogger(__name__)
SSH_KEY_PATH = conf.get_ssh_key_path()
SLICE = conf.get_slice()


def transfer_files(hostname, files, target_dir):
    logger.info(f"Transferring files {files} to {hostname}:{target_dir}")
    for f in files:
        cmd_string = (f"scp -o StrictHostKeyChecking=no -o UserKnownHosts" +
                      f"File=/dev/null -i {SSH_KEY_PATH} {f} " +
                      f"{SLICE}@{hostname}:{target_dir}")
        process = subprocess.Popen(cmd_string.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        if error is not None:
            logger.error(f"Error when copying {f} to {hostname}: {error}")


def run_command(hostname, cmd):
    logger.info(f"Running command {cmd} on {hostname}")
    cmd_string = (f"ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=" +
                  f"/dev/null -l {SLICE} -i {SSH_KEY_PATH} {hostname} {cmd}")
    process = subprocess.Popen(cmd_string.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    if error is not None:
        logger.error(f"Error when running {cmd} on {hostname}")
