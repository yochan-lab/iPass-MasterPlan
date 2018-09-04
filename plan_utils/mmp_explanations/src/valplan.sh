# path to fast downward #
VAL_PATH=$(locate VAL/validate|head -n 1)

# path to pr2plan #
PR2PLAN_PATH=$(locate pr2plan | head -n 1)

# ground domain and problem input using pr2plan #
#rm -f *-domain.pddl *-problem.pddl obs.dat
touch obs.dat
$PR2PLAN_PATH -d $1 -i $2 -o ./obs.dat > stdout.txt

cat pr-domain.pddl | grep -vE "(EXPLAIN|increase|functions)" > tr_val-domain.pddl
cat pr-problem.pddl | grep -vE "(EXPLAIN|increase|metric)" > tr_val-problem.pddl
sed -i 's/_R//g' tr_val-domain.pddl
sed -i 's/_R//g' tr_val-problem.pddl

# validate plan given domain and problem
output=$(${VAL_PATH} tr_val-domain.pddl tr_val-problem.pddl $3 | grep "Successful plans:"|wc -l)

if [ ${output} -gt 0 ]; then
    echo "True"
else
    echo "False"
fi
