# Odin
Orchestrator service used to manage nodes and deployment of code on PlanetLab. Named after the god of gods, Odin.

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