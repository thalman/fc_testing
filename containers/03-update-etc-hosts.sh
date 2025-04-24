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
    echo "This scripts adds containers address to /etc/hosts so"
    echo "they can be accesses by name"
    exit 1
else
    new_hosts >/etc/hosts.new && mv /etc/hosts.new /etc/hosts
fi