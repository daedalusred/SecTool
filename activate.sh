#!/usr/bin/bash

set -e
set -o pipefail

virtualenv --python=python3.4 --no-site-packages --distribute .env && source .env/bin/activate && pip3 install -r requirements.txt  
source .env/bin/activate
