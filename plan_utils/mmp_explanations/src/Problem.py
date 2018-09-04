#!/usr/bin/env python

'''
Topic   :: Environment definition
Project :: Explanations for Multi-Model Planning
Author  :: Tathagata Chakraborti
Date    :: 09/29/2016
'''

from PDDLhelp import *
from Search   import astarSearch
import copy, argparse, os, sys

'''
Class :: Environment Definition
'''

class Problem:

    def __init__(self, robotModelFile, humanModelFile, problemFile, domainTemplate, robotPlanFile = None):

        print "Setting up MMP..."

        self.domainTemplate = domainTemplate
        if not robotPlanFile:
            
            # If robotPlanFile is not given, build a plan
            self.robotPlanFile   = '../domain/cache_plan.dat'
            self.plan, self.cost = get_plan(robotModelFile, problemFile)
            with open(self.robotPlanFile, 'w') as plan_file:
                plan_file.write('\n'.join(['({})'.format(item) for item in self.plan]) + '\n; cost = {} (unit cost)'.format(self.cost))
            
        else:
            
            self.robotPlanFile = robotPlanFile
            with open(robotPlanFile, 'r') as plan_file:
                temp      = plan_file.read().strip().split('\n')
                self.plan = temp
                # Since we do not have costs in the domain, set makespan as the cost
                self.cost = len(self.plan)
            
        ground(robotModelFile, problemFile)
        self.groundedRobotPlanFile   = '../domain/cache_grounded_plan.dat'
        with open(self.groundedRobotPlanFile, 'w') as plan_file:
            plan_file.write('\n'.join(['{}'.format(item) for item in self.plan]) + '\n; cost = {} (unit cost)'.format(self.cost))
        self.ground_state = set(read_state_from_domain_file('tr-domain.pddl'))
        ground(humanModelFile, problemFile)

        try:    self.initialState = set(read_state_from_domain_file('tr-domain.pddl'))
        except: self.initialState = set()

        # Do plan patch explanations for the domain
        add_set          = self.ground_state.difference(self.initialState)
        del_set          = self.initialState.difference(self.ground_state)
        
        myap = {}
        for cond in add_set:
            act = cond.split('-has-')[0]
            if act in myap.keys():
               myap[act]['add'].add(cond)
            else:
               myap[act] = {}
               myap[act]['del'] = set()
               myap[act]['add'] = set()
               myap[act]['add'].add(cond)
               
        for cond in del_set:
            act = cond.split('-has-')[0]
            if act in myap.keys():
               myap[act]['del'].add(cond)
            else:
               myap[act] = {}
               myap[act]['add'] = set()
               myap[act]['del'] = set()
               myap[act]['del'].add(cond)
       
        rel_add = set()        
        rel_del = set()
        for p in myap.keys():
            for act in self.plan:
                
                #Ignore external actions
                if 'complete_semester_' in act.lower() \
                    or 'enable' in act.lower():
                    continue
                
                # Add action definition differences
                if p.lower() in act.lower():
                   for f in myap[p]['add']:
                       rel_add.add(f)
                   for f in myap[p]['del']:
                       rel_del.add(f)
                   
        for p in rel_add:  
            print ("ADD>>",p)
        for p in rel_del:  
            print ("DEL>>",p)
        
        exit(0)
        
    def getStartState(self):
        return self.initialState

    def isGoal(self, state):

        temp_domain      = write_domain_file_from_state(state, self.domainTemplate)
        # plan, cost       = get_plan(temp_domain, 'tr-problem.pddl')
        # optimality_flag  = cost == self.cost
        
        feasibility_flag = validate_plan(temp_domain, 'tr-problem.pddl', self.groundedRobotPlanFile)
        return feasibility_flag# and optimality_flag

    
    def heuristic(self, state):
        return 0.0

    
    def getSuccessors(self, node):

        listOfSuccessors = []

        state            = set(node[0])
        ground_state     = set(self.ground_state)

        add_set          = ground_state.difference(state)
        del_set          = state.difference(ground_state)

        for item in add_set:
            new_state    = copy.deepcopy(state)
            new_state.add(item)
            listOfSuccessors.append([list(new_state), item])

        for item in del_set:
            new_state    = copy.deepcopy(state)
            new_state.remove(item)
            listOfSuccessors.append([list(new_state), item])
            
        return listOfSuccessors
        

'''
main method
'''

def main():
    
    parser = argparse.ArgumentParser(description = '''This is the Problem class. Explanations for Multi-Model Planning.''',
                                     epilog      = '''Usage >> ./Problem.py -m ../domain/fetchworld-tuck-m.pddl -n ../domain/fetchworld-base-m.pddl -f ../domain/problem1.pddl ''')
     
    parser.add_argument('-m', '--model',   type=str, help="Domain file with real PDDL model of robot.")
    parser.add_argument('-n', '--nmodel',  type=str, help="Domain file with human model of the robot.")
    parser.add_argument('-d', '--domain_template',   type=str, help="Domain template for the current MMP.")
    parser.add_argument('-f', '--problem', type=str, help="Problem file.")
    parser.add_argument('-p', '--plan',    type=str, help="Plan file.")
 
    args   = parser.parse_args()

    if not sys.argv[1:]:
        print parser.print_help()

    else:
        print "args plan",args.plan    
        problem_instance = Problem(args.model, args.nmodel, args.problem, args.domain_template, args.plan)
        plan             = astarSearch(problem_instance)
        
        explanation      = ''
        for item in plan:
            explanation += "Explanation >> {}\n".format(item)

        print explanation.strip()
        with open('exp.dat', 'w') as explanation_file:
            explanation_file.write(explanation.strip())
        

if __name__ == '__main__':
    main()
