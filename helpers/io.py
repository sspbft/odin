"""Wrappers around basic IO commands."""

import os


def exists(path):
    """Returns True if a file/dir exists at the given path."""
    return os.path.isfile(path) or os.path.isdir(path)


def get_abs_path(relative_path):
    """Returns the absolut path for a given path."""
    return os.path.abspath(relative_path)


def write_file(path, contents, mode="w"):
    """Writes contents to a file at a given path."""
    with open(path, mode) as f:
        f.write(contents)


def create_dir(path):
    """Creates a directory at the given path."""
    os.makedirs(path)
