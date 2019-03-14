from conf import conf
from helpers import io
import logging
import subprocess

logger = logging.getLogger(__name__)
SSH_KEY_PATH = conf.get_ssh_key_path()
SLICE = conf.get_slice()


def get_log_file(hostname):
    if not io.exists("./etc/logs"):
        io.create_dir("./etc/logs")
    return open(f"./etc/logs/{hostname}.log", "a")


def transfer_files(hostname, files, target_dir, timeout=10):
    logger.debug(f"Transferring files {files} to {hostname}:{target_dir}")
    log_file = get_log_file(hostname)

    for f in files:
        cmd_string = (f"scp -o StrictHostKeyChecking=no -o UserKnownHosts" +
                      f"File=/dev/null -i {SSH_KEY_PATH} {f} " +
                      f"{SLICE}@{hostname}:{target_dir}")
        try:
            process = subprocess.Popen(cmd_string.split(), stdout=log_file,
                                       stderr=log_file)
            output, error = process.communicate(timeout=timeout)
            ret_code = process.returncode
            if error is not None or process.returncode != 0:
                logger.error(f"Got return code {ret_code} when copying {f} " +
                             f" to {hostname}. Error: {error}")
        except subprocess.TimeoutExpired:
            logger.error(f"Transferring {files} to {hostname} timed out")
            return 1
    log_file.close()
    return 0


def run_command(hostname, cmd, timeout=None):
    logger.debug(f"Running command {cmd} on {hostname}")
    log_file = get_log_file(hostname)
    cmd_string = (f"ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=" +
                  f"/dev/null -l {SLICE} -i {SSH_KEY_PATH} {hostname} {cmd}")
    process = subprocess.Popen(cmd_string.split(), stdout=log_file,
                               stderr=log_file)
    try:
        output, error = process.communicate(timeout=timeout)
        ret_code = process.returncode
        if error is not None or ret_code != 0:
            logger.error(f"Got return code {ret_code} when running {cmd} on " +
                         f"{hostname}. Error: {error}")
        return ret_code
    except subprocess.TimeoutExpired:
        logger.error(f"Cmd {cmd} on {hostname} timed out")
        return 1
