#!/bin/bash
#
# run me as root so I can reach containers
# via podman exec
#

if [ `id -u` != 0 ] ; then
    echo "This script ($0) must run as root, trying sudo ..." 1>&2
    exec sudo $0 "$@"
fi

set -e

. .venv/bin/activate
pytest --mh-config=./mhc.yml tests "$@"
