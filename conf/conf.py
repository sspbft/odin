
from configparser import ConfigParser
import helpers.constants as cs

auth_conf = ConfigParser()
auth_conf.read(f"conf/{cs.AUTH_CONF}")
odin_conf = ConfigParser()
odin_conf.read(f"conf/{cs.ODIN_CONF}")


def get(conf, section, option):
    """Generic get method that reads a config item."""
    if conf == cs.AUTH_CONF:
        return auth_conf.get(section, option)
    else:
        return odin_conf.get(section, option)


def get_pl_username():
    """Returns the configured PlanetLab username."""
    return get(cs.AUTH_CONF, cs.AUTH_SECTION, cs.PL_USERNAME)


def get_pl_password():
    """Returns the configured PlanetLab password."""
    return get(cs.AUTH_CONF, cs.AUTH_SECTION, cs.PL_PASSWORD)


def get_ssh_key_path():
    """Returns the configured absolute path to the SSH key to use."""
    return get(cs.AUTH_CONF, cs.AUTH_SECTION, cs.SSH_KEY_ABS_PATH)


def get_number_of_nodes():
    """Returns the configured number of nodes."""
    return int(get(cs.ODIN_CONF, cs.MAIN_SECTION, cs.NUMBER_OF_NODES))


def get_number_of_byzantine():
    """Returns the configured number of byzantine nodes."""
    return int(get(cs.ODIN_CONF, cs.MAIN_SECTION, cs.NUMBER_OF_BYZ))


def get_application_git_url():
    """Returns the configured git url for the application to deploy."""
    return get(cs.ODIN_CONF, cs.APP_SECTION, cs.GIT_URL)


def get_application_git_branch():
    """Returns the configured git branch for the application to deploy."""
    return get(cs.ODIN_CONF, cs.APP_SECTION, cs.GIT_BRANCH)


def get_bootstrap_script():
    """Returns the configured path of the bootstrap script for the app."""
    return get(cs.ODIN_CONF, cs.APP_SECTION, cs.BOOTSTRAP_SCRIPT)


def get_target_dir():
    """Returns the configured target dir for the app on a PLanetLab node."""
    return get(cs.ODIN_CONF, cs.APP_SECTION, cs.TARGET_DIR)


def get_app_folder():
    """Returns the configured folder for the app on a PLanetLab node."""
    return get(cs.ODIN_CONF, cs.APP_SECTION, cs.APP_FOLDER)


def get_abs_path_to_app():
    """Returns the absolute path to the application root folder."""
    return f"{get_target_dir()}/{get_app_folder()}"


def get_app_entrypoint():
    """Returns the entrypoint command that starts the app."""
    return get(cs.ODIN_CONF, cs.APP_SECTION, cs.ENTRYPOINT)


def get_app_run_sleep():
    """Returns the entrypoint command that starts the app."""
    return get(cs.ODIN_CONF, cs.APP_SECTION, cs.RUN_SLEEP)


def get_client_src():
    """Return the folder containing the client code."""
    return get(cs.ODIN_CONF, cs.CLIENT_SECTION, cs.CLIENT_SRC)


def get_client_entrypoint():
    """Return the configured entrypoint script for a client process."""
    return get(cs.ODIN_CONF, cs.CLIENT_SECTION, cs.CLIENT_ENTRYPOINT)


def get_nbr_of_clients():
    """Return the configured number of clients that should be started."""
    return get(cs.ODIN_CONF, cs.CLIENT_SECTION, cs.NBR_OF_CLIENTS)


def get_reqs_per_client():
    """Returns the configured requests each client should send."""
    return get(cs.ODIN_CONF, cs.CLIENT_SECTION, cs.REQS_PER_CLIENT)


def get_slice():
    """Returns the configured slice."""
    return get(cs.ODIN_CONF, cs.PL_SECTION, cs.SLICE)


def get_blacklisted_hosts():
    """Returns a list of the blacklisted hostnames."""
    return get(cs.ODIN_CONF, cs.PL_SECTION, cs.BLACKLISTED_HOSTS).split(",")


def get_heimdall_sd_path():
    """Returns the absolute path to the Heimdall SD file."""
    return get(cs.ODIN_CONF, cs.ETC_SECTION, cs.HEIMDALL_SD_PATH)


def get_heimdall_root():
    """Returns the absolute path to the Heimdall project root."""
    return get(cs.ODIN_CONF, cs.ETC_SECTION, cs.HEIMDALL_ROOT)
