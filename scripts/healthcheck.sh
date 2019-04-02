# PlanetLab Healthcheck script
# run as ./healthcheck [port] [response]
# defaults to ./healthcheck 9876 OK

# kill possible nc processes
pkill -f nc

# check for Internet access
wget -q --tries=10 --timeout=20 --spider https://media.inneva.se/inneva.png > /dev/null
if [[ $? -eq 0 ]]; then
        echo "Host appears to be online"
else
        echo "Host appears to be offline. Aborting."
        exit 1
fi

# check if yum is working
# sudo yum clean all
# sudpo yum update all
# sudo yum install git -y --nogpgcheck
# if [[ $? -eq 0 ]]; then
#         echo "yum seems to be working"
# else
#         echo "yum does not work, aborting"
#         exit 1
# fi

if [ -x "$(command -v python)" ]; then
        python -m SimpleHTTPServer 9876

elif ! [ -x "$(command -v ncat)" ]; then
        sudo yum install nmap -y --nogpgcheck
        # Listen for connections on external interface
        echo "Listening for connections on ${1:-9876}"
        RESPONSE="HTTP/1.1 200 OK\r\nConnection: keep-alive\r\n\r\n${2:-"OK"}\r\n"
        while { echo -en "$RESPONSE"; } | ncat -l 0.0.0.0 "${1:-9876}"; do
        echo "================================================"
        done
fi