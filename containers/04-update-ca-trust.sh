#!/bin/bash

get_container_ip() {
    podman inspect $1 | jq -r '.[0].NetworkSettings.Networks | keys[] as $k | (.[$k] | .IPAddress )'
}


remove() {
    grep -v -E '^[0-9.]+[[:space:]]+'$1'$'
}

add() {
    echo `get_container_ip $1` $1
}

new_hosts() {
    cat /etc/hosts | remove web | remove keycloak
    add web
    add keycloak
}

if [ `id -u` != 0 ]; then
    echo "Run $0 as root"
    echo "This script put testing CA into host system"
    echo "So the containers are trusted."
    exit 1
else
    if [ -f ca/rootCA.crt ]; then
        cp ca/rootCA.crt /etc/pki/ca-trust/source/anchors/FederationComponentsTesting.crt
        update-ca-trust
    else
        echo "File ca/rootCA.crt not found. Run ./01-certificates.sh first." 1>&2
        exit 1
    fi
fi