# PlanetLab Healthcheck script
# run as ./healthcheck [port] [response]
# defaults to ./healthcheck 8080 OK

# kill possible nc processes
pkill -f nc

# Check for Internet access
wget -q --tries=10 --timeout=20 --spider http://google.com > /dev/null
if [[ $? -eq 0 ]]; then
        echo "Host appears to be online"
else
        echo "Host appears to be offline. Aborting."
        exit 1
fi

if [ -x "$(command -v python)" ]; then
        python -m SimpleHTTPServer 8080

elif ! [ -x "$(command -v ncat)" ]; then
        sudo yum -y install nmap
        # Listen for connections on external interface
        echo "Listening for connections on ${1:-8080}"
        RESPONSE="HTTP/1.1 200 OK\r\nConnection: keep-alive\r\n\r\n${2:-"OK"}\r\n"
        while { echo -en "$RESPONSE"; } | ncat -l 0.0.0.0 "${1:-8080}"; do
        echo "================================================"
        done
fi