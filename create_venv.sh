#!/usr/bin/env bash

## create virtual environment
virtualenv -p /usr/bin/python .venv

#activate virtual environment
source .venv/bin/activate

## install dependencies
pip install -r requirements.txt
