#/bin/bash
# entrypoint for setting up a PlanetLab node

BLUE='\033[1;34m'
NO_COLOR='\033[0m'

log () {
	echo -e "${BLUE}[Odin.startup] ==> $1${NO_COLOR}"
}

log "Checking if node is bootstrapped"
log "Startup done!"
