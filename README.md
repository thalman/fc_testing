# Testing federation components with containers and pytest_mh

## Containers

Rootless containers are not supported at the moment.

To build and run containers use scripts in `containers` folder

    cd containers
    sudo ./00-dependencies.sh
    ./01-certificates.sh
    sudo ./02-compose-up.sh
    sudo ./03-update-etc-hosts.sh
    sudo ./04-update-ca-trust.sh

Containers are named `web` and `keycloak` and they should be accessible
from your browser under those names.

## Tests

Create python virtual environment and install required libraries

    ./01-prepare-venv.sh

Run tests

    sudo ./02-run.sh
