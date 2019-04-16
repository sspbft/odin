# ntoe that this is the bootstrap script for BFTList and not a generic script
cp /practicalbft/priv_hosts.txt conf/hosts.txt
python3.7 -m venv env
source ./env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
deactivate
