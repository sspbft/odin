"""Contains constants used throughout this project."""

# Conf
AUTH_CONF = "auth.ini"
ODIN_CONF = "odin.ini"

AUTH_SECTION = "auth"
PL_USERNAME = "pl_username"
PL_PASSWORD = "pl_password"
SSH_KEY_ABS_PATH = "ssh_key_abs_path"
MAIN_SECTION = "main"
SLICE = "slice"
NUMBER_OF_NODES = "number_of_nodes"
NUMBER_OF_BYZ = "number_of_byzantine"

APP_SECTION = "application"
GIT_URL = "git_url"
GIT_BRANCH = "git_branch"
BOOTSTRAP_SCRIPT = "bootstrap_script"
TARGET_DIR = "target_dir"
APP_FOLDER = "app_folder"
ENTRYPOINT = "entrypoint"
RUN_SLEEP = "run_sleep"

PL_SECTION = "planetlab"
BLACKLISTED_HOSTS = "blacklisted_hosts"

ETC_SECTION = "etc"
HEIMDALL_SD_PATH = "heimdall_sd_path"
HEIMDALL_ROOT = "heimdall_root"

# PlanetLab API
API_URL = "https://www.planet-lab.eu/PLCAPI/"
NODE_HEALTHY = "boot"
NODE_CMD_THRESHOLD = 10

# Etc
HEALTH_CHECK_PORT = 9876

# CLI Args
DEPLOY = "deploy"
CLEANUP = "cleanup"
FIND_HEALTHY = "find_healthy"
ADD_ALL_NODES_TO_SLICE = "add_all_nodes"
ADD_HEALTHY_NODES_TO_SLICE = "add_healthy"
REMOVE_NODES_FROM_SLICE = "remove_nodes"
