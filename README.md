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

Then, it is as easy as running `python odin.py` and watching the magic happen!

## Deploying an application to PlanetLab
`// TODO`

## Using the bundled client for BFTList
First, make sure that a deployment has been done and the nodes are running. Then run
```
cd client && ./start_shell
```
and start sending requests using the client shell!