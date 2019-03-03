#/bin/bash
# bootstraps a PlanetLab node for PracticalBFT usage

BLUE='\033[1;34m'
NO_COLOR='\033[0m'

log () {
	echo -e "${BLUE}[Odin.bootstrap] ==> $1${NO_COLOR}"
}

log "Bootstrapping node"

log "Installing dependencies and build tools"
sudo yum -y install gcc openssl-devel bzip2-devel
sudo yum -y install gcc gcc-c++ 
sudo yum -y install zlib zlib-devel
sudo yum -y install libffi-devel 
sudo yum install -y make

if ! [ -x "$(command -v python3.7)" ]; then
	log "Installing Python 3.7.2"
	cd /usr/src
	sudo wget https://www.python.org/ftp/python/3.7.2/Python-3.7.2.tgz
	sudo tar xzf Python-3.7.2.tgz
	cd Python-3.7.2
	sudo ./configure --enable-optimizations
	sudo make altinstall
	sudo ln -s /usr/local/bin/python3.7 /bin/python3.7
	log "Python 3.7.2 available as python3.7 in /bin"
else
	log "Python 3.7.2 already installed, skipping"
fi

if ! [ -x "$(command -v git)" ]; then
	log "Installing git"
	sudo yum install git -y
else
	log "git already installed, skipping"
fi

log "Setting up PracticalBFT dir"
sudo rm -r /practicalbft
sudo mkdir /practicalbft
sudo chown -R chalmersple_2018_10_29 /practicalbft/

log "Fetching Thor"
cd /practicalbft
git clone https://github.com/practicalbft/thor.git
cd thor
python3.7 -m venv env
source ./env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
deactivate
log "Thor installed and bootstrapped"
