#/bin/bash
# bootstraps a PlanetLab node for PracticalBFT usage

BLUE='\033[1;34m'
NO_COLOR='\033[0m'

log () {
	echo -e "${BLUE}[Odin.bootstrap] ==> $1${NO_COLOR}"
}

install_python () {
	log "Installing Python 3.7.2"
	cd /usr/src
	sudo wget https://www.python.org/ftp/python/3.7.2/Python-3.7.2.tgz
	sudo tar xzf Python-3.7.2.tgz
	cd Python-3.7.2
	# export LD_LIBRARY_PATH=$(which openssl):$LD_LIBRARY_PATH
	# export LD_LIBRARY_PATH=/usr/local/openssl:$LD_LIBRARY_PATH
	# sudo LDFLAGS="-L/usr/local/openssl" ./configure --enable-optimizations --with-openssl=/usr/local/openssl
	# sudo LDFLAGS="-L$(which openssl)" ./configure --enable-optimizations --with-openssl=$(which openssl)
	sudo ./configure --enable-optimizations
	sudo make altinstall
	sudo ln -s /usr/local/bin/python3.7 /bin/python3.7
	log "Python 3.7.2 available as python3.7 in /bin"
}

install_rsyslog () {
	log "Installing remote_syslog"
	touch application.log
	chmod 777 application.log
	wget https://github.com/papertrail/remote_syslog2/releases/download/v0.20/remote_syslog_linux_amd64.tar.gz -O remote_syslog2.tar.gz
	tar -xvf remote_syslog2.tar.gz
	cd remote_syslog
	sudo cp ./remote_syslog /usr/local/sbin
	log "remote_syslog installed"
}

log "Bootstrapping node"
rm -rf ~/wget-log*

log "Setting up PracticalBFT dir"
sudo rm -r /practicalbft
sudo mkdir /practicalbft
sudo chown -R chalmersple_2018_10_29 /practicalbft/
cd /practicalbft

if ! [ -x "$(command -v remote_syslog)" ]; then
	install_rsyslog
else
	log "remote_syslog already installed, skipping"
fi

sudo /usr/local/sbin/remote_syslog -c ~/log_files.yml &

log "Installing dependencies and build tools"
sudo yum -y install gcc openssl-devel bzip2-devel
sudo yum -y install gcc gcc-c++ 
sudo yum -y install zlib zlib-devel
sudo yum -y install libffi-devel 
sudo yum install -y make
sudo yum update -y nss curl

if ! [ -x "$(command -v python3.7)" ]; then
	install_python
else
	log "Python 3.7.2 already installed, skipping"
	log "Checking if pip is working"
	cd ~
	python3.7 -m venv env
	source ./env/bin/activate
	pip install numpy
	if [ $? -eq 0 ]; then
		deactivate
		rm -r env
		log "pip seems to be working, continuing"
	else
		deactivate
		rm -r env
		log "pip is not working, re-installing Python 3.7.2/pip"
		install_python
	fi
fi

if ! [ -x "$(command -v git)" ]; then
	log "Installing git"
	sudo yum install git -y
else
	log "git already installed, skipping"
fi

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
