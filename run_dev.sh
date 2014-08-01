#!/bin/bash
# Create virtual env
# run me as `source run_dev.sh`
if [ -f .env ]; then

	if [[ $1 = 'py3' ]]; then
		python3	bootstrap_venv.py python3
	else
		python bootstrap_venv.py
	fi

	source .env/bin/activate
	pip install -r requirements.txt
else
	source .env/bin/activate
fi
