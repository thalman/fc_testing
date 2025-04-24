#!/bin/bash
#
# run me as root so I can reach containers
# via podman exec
#

if [ `id -u` != 0 ]; then
    echo "Run me as root"
    exit 1
fi

set -e

. .venv/bin/activate
pytest --mh-config=./mhc.yml tests "$@"
