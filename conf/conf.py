
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


def get_slice():
    """Returns the configured slice."""
    return get(cs.ODIN_CONF, cs.MAIN_SECTION, cs.SLICE)


def get_number_of_nodes():
    """Returns the configured number of nodes."""
    return int(get(cs.ODIN_CONF, cs.MAIN_SECTION, cs.NUMBER_OF_NODES))


def get_number_of_byzantine():
    """Returns the configured number of byzantine nodes."""
    return int(get(cs.ODIN_CONF, cs.MAIN_SECTION, cs.NUMBER_OF_BYZ))
