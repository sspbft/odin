"""Module containing PlanetLab auth code."""

from conf import conf


def get_auth():
    """Returns auth object used when connecting to a PlanetLab host."""
    username = conf.get_pl_username()
    password = conf.get_pl_password()

    if not username or not password:
        raise ValueError(f"Auth not configured correctly")

    return {
        "AuthMethod": "password",
        "Username": username,
        "AuthString": password
    }
