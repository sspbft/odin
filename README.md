# Odin
Orchestrator service used to manage nodes and deployment of code on PlanetLab. Named after the god of gods, Odin.
[![Build status](https://travis-ci.org/practicalbft/odin.svg?branch=master)](https://travis-ci.org/travis-ci/travis-web)


## About Odin
## Set up
```
git clone https://github.com/practicalbft/odin.git && cd odin
python3.7 -m venv env
source ./env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
mv conf/auth.example.ini conf/auth.ini  # edit with appropriate details
```

Modify `conf/odin.ini` to contain the appropriate configuration values.

## Deploying an application to PlanetLab
First, make sure that everything is installed and that `conf/auth.ini` and `conf/odin.ini` exists and contain the right settings.

Then, Odin can be used as follows
`python odin.py flags [--git-branch BRANCH --starting-state PATH_TO_JSON_FILE --non-selfstab --reuse-hosts --scale SCALE_FACTOR] deploy|cleanup`

After deploying, run `CTRL + C` in the same shell and Odin will kill off the running processes started by the user on the nodes.