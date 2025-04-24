#!/bin/bash

set -e

rm -rf .venv
python -m venv .venv

. ./.venv/bin/activate

pip install -r requirements.txt
