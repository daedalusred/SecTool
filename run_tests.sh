#!/bin/bash

set -e
set -o pipefail

python3 -m unittest discover $1
