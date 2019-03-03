from conf import conf
from helpers.constants import (PL_USERNAME, PL_PASSWORD)


def get_auth():
    username = conf.get_pl_username()
    password = conf.get_pl_password()

    if not username or not password:
        raise ValueError(f"Auth not configured correctly")

    return {
        "AuthMethod": "password",
        "Username": username,
        "AuthString": password
    }
