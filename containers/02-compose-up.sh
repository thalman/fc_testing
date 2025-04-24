#!/bin/sh

if [ `id -u` != 0 ] ; then
    echo "Run $0 as root" 1>&2
    exit 1
fi

podman-compose --file compose.yaml up -d "$@"
