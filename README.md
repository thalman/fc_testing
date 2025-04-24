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

## Tests

Create python virtual environment and install required libraries

    ./01-prepare-venv.sh

Run tests

    ./02-run.sh
