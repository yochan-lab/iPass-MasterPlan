#/usr/bin/env bash

# path to pr2plan #
#PR2PLAN_PATH=$(locate pr2plan | head -n 1)

# ground domain and problem input using pr2plan #
rm -f *-domain.pddl *-problem.pddl obs.dat
#touch obs.dat
#$PR2PLAN_PATH -d $1 -i $2 -o ./obs.dat > stdout.txt

#rm -f *-domain.pddl *-problem.pddl obs.dat
cp $1 tr-domain.pddl
cp $2 tr-problem.pddl

#cat pr-domain.pddl | grep -vE "(EXPLAIN|increase|functions)" > tr-domain.pddl
#cat pr-problem.pddl | grep -vE "(EXPLAIN|increase|metric)" > tr-problem.pddl
#sed -i 's/_R//g' tr-domain.pddl
#sed -i 's/_R//g' tr-problem.pddl
