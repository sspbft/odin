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

log "Installing Python 3.7.2"
cd /usr/src
sudo wget https://www.python.org/ftp/python/3.7.2/Python-3.7.2.tgz
sudo tar xzf Python-3.7.2.tgz
cd Python-3.7.2
sudo ./configure --enable-optimizations
sudo make altinstall
sudo ln -s /usr/local/bin/python3.7 /bin/python3.7
log "Python 3.7.2 available as python3.7 in /bin"

# log "Installing rsyslog"
# sudo yum -y install rsyslog

log "Installing git"
sudo yum install git -y

log "Fetching Thor"
sudo rm -r /practicalbft
sudo mkdir /practicalbft
sudo chown -R chalmersple_2018_10_29 /practicalbft/
cd /practicalbft
git clone https://github.com/practicalbft/thor.git
cd thor
