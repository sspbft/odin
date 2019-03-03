
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


def get_slice():
    """Returns the configured slice."""
    return get(cs.ODIN_CONF, cs.MAIN_SECTION, cs.SLICE)


def get_number_of_nodes():
    """Returns the configured number of nodes."""
    return int(get(cs.ODIN_CONF, cs.MAIN_SECTION, cs.NUMBER_OF_NODES))


def get_number_of_byzantine():
    """Returns the configured number of byzantine nodes."""
    return int(get(cs.ODIN_CONF, cs.MAIN_SECTION, cs.NUMBER_OF_BYZ))


def get_application_git_url():
    """Returns the configured git url for the application to deploy."""
    return get(cs.ODIN_CONF, cs.APP_SECTION, cs.GIT_URL)


def get_bootstrap_script():
    """Returns the configured path of the bootstrap script for the app."""
    return get(cs.ODIN_CONF, cs.APP_SECTION, cs.BOOTSTRAP_SCRIPT)
