#!/bin/bash
export PYTHONPATH=$PWD/external/tornado:$PYTHONPATH
python main.py $@
