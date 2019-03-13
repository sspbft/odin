import os


def exists(path):
    return os.path.isfile(path) or os.path.isdir(path)


def get_abs_path(relative_path):
    return os.path.abspath(relative_path)


def write_file(path, contents, mode="w"):
    """Writes contents to a file at a given path."""
    with open(path, mode) as f:
        f.write(contents)


def create_dir(path):
    os.makedirs(path)
