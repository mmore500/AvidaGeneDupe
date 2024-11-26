#!/usr/bin/bash

cd "$(dirname $0)"

python3 -m uv pip compile requirements.in > requirements.txt
