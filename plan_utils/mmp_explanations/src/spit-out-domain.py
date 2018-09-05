import pddlpy
import sys

dom = sys.argv[1]
prob = sys.argv[2]


d_pr = pddlpy.DomainProblem(dom, prob)


for k in d_pr.operators():
    for pr in d_pr.domain.operators[k].precondition_pos:
         if type(pr) == "tuple":
             print (k+"-has-preconditon-"," ".join(list(pr)))
         else:
              print (k+"-has-preconditon-"," ".join(list(pr.predicate)))
    for pr in d_pr.domain.operators[k].precondition_neg:
        if type(pr) == "tuple":
            print (k+"-has-neg-preconditon-"," ".join(list(pr)))
        else:
             print (k+"-has-neg-preconditon-"," ".join(list(pr.predicate)))
