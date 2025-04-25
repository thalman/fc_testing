#!/bin/sh

if [ `id -u` != 0 ] ; then
    echo "This script ($0) must run as root, trying sudo ..." 1>&2
    exec sudo $0
fi

podman-compose --file compose.yaml down
