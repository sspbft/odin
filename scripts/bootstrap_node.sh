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
	wget https://www.python.org/ftp/python/3.7.2/Python-3.7.2.tgz
	tar xzf Python-3.7.2.tgz
	cd Python-3.7.2
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

install_node_exporter () {
	log "Installing node_exporter"
	cd /usr/src
	wget https://github.com/prometheus/node_exporter/releases/download/v0.17.0/node_exporter-0.17.0.linux-amd64.tar.gz
	tar -xvf node_exporter-0.17.0.linux-amd64.tar.gz
	cd node_exporter-0.17.0.linux-amd64
	sudo cp node_exporter /usr/local/sbin
	log "node_exporter installed"
}

log "Bootstrapping node"
rm -rf ~/wget-log*

log "Setting up PracticalBFT dir"
sudo rm -r /sspbft
sudo mkdir /sspbft
sudo chown -R chalmersple_2018_10_29 /usr/src/
sudo chown -R chalmersple_2018_10_29 /sspbft/
cd /sspbft

if ! [ -x "$(command -v remote_syslog)" ]; then
	install_rsyslog
else
	log "remote_syslog already installed, skipping"
fi

if ! [ -x "$(command -v node_exporter)" ]; then
	install_node_exporter
else
	log "node_exporter already installed, skipping"
fi

sudo nohup $(which remote_syslog) -c ~/log_files.yml >/dev/null 2>&1 &
IP=$(curl ifconfig.me)
nohup node_exporter --web.listen-address=$IP:9111 --collector.tcpstat >/dev/null 2>&1 &

log "Installing dependencies and build tools"
sudo yum install gcc openssl-devel bzip2-devel -y --nogpgcheck
sudo yum install gcc gcc-c++ -y --nogpgcheck
sudo yum install zlib zlib-devel -y --nogpgcheck
sudo yum install libffi-devel -y --nogpgcheck
sudo yum install make -y --nogpgcheck
sudo yum update nss curl -y --nogpgcheck

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
	sudo yum install git -y --nogpgcheck
else
	log "git already installed, skipping"
fi

log "Fetching Thor"
cd /sspbft
git clone https://github.com/sspbft/thor.git
cd thor
python3.7 -m venv env
source ./env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
deactivate
log "Thor installed and bootstrapped"

log "Fetching BFTList-client"
cd /sspbft
git clone https://github.com/sspbft/BFTList-client.git
cd BFTList-client
python3.7 -m venv env
source ./env/bin/activate
chmod +x *.sh
pip install --upgrade pip
pip install -r requirements.txt
deactivate
log "BFTList-client installed and bootstrapped"