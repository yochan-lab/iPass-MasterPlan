#/usr/bin/env bash

/home/ssengu15/Dropbox\ \(ASU\)/code/iPass-MasterPlan/plan_utils/ff -o $1 -f $2 | grep -E '[0-9]: ' | awk -F': ' '{print $2}' > sas_plan

# path to fast downward #
# FD_PATH=$(locate fast-downward.py | head -n 1)

# find optimal plan using fd on input domain and problem #
# rm -f output output.sas sas_plan
# ${FD_PATH} $1 $2 --search "astar(lmcut())" | grep -e \([0-9]\) | awk '{$NF=""; print $0}'
