#!/bin/bash
cd "$(dirname "$0")"
python3 ./create_virtualenv.py
source ./venv/bin/activate
./venv/bin/python -m pip install fake-bpy-module
read -n1 -r -p "Press any key to continue..." key
