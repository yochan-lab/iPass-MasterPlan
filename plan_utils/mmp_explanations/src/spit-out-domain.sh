#!/bin/bash
dos2unix $1 $2 > /dev/null
python3 spit-out-domain.py $1 $2 
