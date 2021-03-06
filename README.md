# DEPRECATED
Please use [plcli](https://github.com/axelniklasson/plcli) instead!

# Odin
[![Build status](https://travis-ci.org/sspbft/odin.svg?branch=master)](https://travis-ci.org/travis-ci/travis-web)

Orchestrator service used to manage nodes and deployment of code on PlanetLab. Named after the god of gods, Odin.


## About Odin
## Set up
```
git clone https://github.com/sspbft/odin.git && cd odin
python3.7 -m venv env
source ./env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cp conf/auth.example.ini conf/auth.ini  # edit with appropriate details
```

Modify `conf/odin.ini` to contain the appropriate configuration values.

## Deploying an application to PlanetLab
First, make sure that everything is installed and that `conf/auth.ini` and `conf/odin.ini` exists and contain the right settings.

```
usage: odin.py [-h] [-b GIT_BRANCH] [-nss] [-f HOSTS_FILE] [-r]
               [-ss STARTING_STATE] [-s SCALE] [-rs RUN_SLEEP] [-c CLIENTS]
               mode

CLI for deploying applications to PlanetLab

positional arguments:
  mode                  either [deploy], [cleanup] or [find_healthy]

optional arguments:
  -h, --help            show this help message and exit
  -b GIT_BRANCH, --git-branch GIT_BRANCH
                        the git branch to deploy
  -nss, --non-selfstab  run application without self-stabilization
  -f HOSTS_FILE, --hosts-file HOSTS_FILE
                        file containing hosts
  -r, --reuse-hosts     re-use hosts from last deployment
  -ss STARTING_STATE, --starting-state STARTING_STATE
                        path to start_state.json for state injection
  -s SCALE, --scale SCALE
                        number of virtual instances on each PL node
  -rs RUN_SLEEP, --run-sleep RUN_SLEEP
                        s to sleep in module.run
  -c CLIENTS, --clients CLIENTS
                        number of clients
```

After deploying, run `CTRL + C` in the same shell and Odin will kill off the running processes started by the user on the nodes.
