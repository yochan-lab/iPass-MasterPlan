#!/usr/bin/env python

'''
Topic   :: Help with PDDL stuff
Project :: Explanations for Multi-Model Planning
Author  :: Tathagata Chakraborti
Date    :: 09/29/2016
'''

import re, os


'''
Global :: global variables
'''

__DOMAIN_SOURCE__ = '../../domain/domain_template.pddl'

__GROUND_CMD__ = "./ground.sh {} {} > stdout.txt"
__PARSER_CMD__ = "./spit-out-domain.sh {} {}"
__CREATE_TMP_CMD__ = "./create_tmp.sh {} {} > stdout.txt"
__FD_PLAN_CMD__ = "./fdplan.sh {} {}"
__FD_PLAN_COST_CMD__ = "./get_plan_cost.sh"
__VAL_PLAN_CMD__ = "./valplan.sh {} {} {}"
__GRAPH_TEST_CMD__ = "./graph_test.sh {} {} {}"
__FAIL_POINT_CMD__ = "./fail_point.sh {} {} {}"



def get_problem_state_preds(domain_file, proble_file, section_prefix):
    pddl.Parser()
    return init_state


'''
Method :: write domain file from given state
'''

def write_domain_file_from_state(state, domain_source, problem_source):

    predicateList = set()
    actionList    = {}
    init_state_list = []
    goal_state_list =[]

    for item in state:
        if "state" not in item:
            regex_probe   = re.compile("(.*)-has-(parameters|negprecondition|precondition|add-effect|delete-effect)-(.*)$").search(item)
            actionName    = regex_probe.group(1)
            _condition    = regex_probe.group(2)
            predicateName = regex_probe.group(3)

            predicateList.add(predicateName)

            if actionName not in actionList: actionList[actionName] = {'parameters':"", 'precondition' : [], 'negprecondition' : [], 'add-effect' : [], 'delete-effect' : []}
            if _condition == 'parameters':
                actionList[actionName][_condition] = predicateName
            else:
                actionList[actionName][_condition].append(predicateName) 
        else:
            regex_probe   = re.compile("has-(initial|goal)-state-(.*)$").search(item)
            state_type = regex_probe.group(1)
            pred = regex_probe.group(2)
            if state_type == 'initial':
                init_state_list.append('({})'.format(' '.join(pred.split('@'))))
            else:
                goal_state_list.append('({})'.format(' '.join(pred.split('@'))))

    temp_domainFileName = 'temp.pddl'
    temp_problemFileName = 'temp_prob.pddl'

    with open(domain_source, 'r') as template_domain_file:
        template_domain = template_domain_file.read()

    with open(problem_source, 'r') as template_prob_file:
        template_problem = template_prob_file.read()



    with open(temp_domainFileName, 'w') as temp_domain_file:

        predicateString = '\n'.join(['( {} )'.format(item) if item != '' else '' for item in predicateList])
        actionString    = '\n'.join(['(:action {}\n:parameters ({})\n:precondition\n(and\n{}\n)\n:effect\n(and\n{}\n)\n)\n'\
                                     .format(key, actionList[key]['parameters'],'\n'.join(['( {} )'.format(p) for p in actionList[key]['precondition']]) + '\n'+
                                             '\n'.join(['(not ( {} ) )'.format(p) for p in actionList[key]['negprecondition']]), \
                                             '{}\n{}'.format('\n'.join(['( {} )'.format(p) for p in actionList[key]['add-effect']]), \
                                                             '\n'.join(['(not ( {} ))'.format(p) for p in actionList[key]['delete-effect']]))) for key in actionList.keys()])

        template_domain = template_domain.replace('%PREDICATES%',predicateString)
        temp_domain_file.write(template_domain.replace('%OPERATORS%',actionString))

    with open(temp_problemFileName, 'w') as temp_problem_file:
        template_problem = template_problem.replace('%INIT%','\n'.join(init_state_list))
        template_problem = template_problem.replace('%GOAL%','\n'.join(goal_state_list))
        temp_problem_file.write(template_problem) 
    return (temp_domainFileName, temp_problemFileName)
        

'''
Method :: read state from given domain file
'''

def read_state_from_domain_file(domainFileName, problemFileName):

    state = parse_problem(domainFileName, problemFileName)
    with open('/tmp/state','w') as s_fd:
        s_fd.write("\n".join(state))
       
    return state



def parse_problem(domainFileName, problemFileName):
    output = os.popen(__PARSER_CMD__.format(domainFileName, problemFileName)).read().strip()
    state = [item.strip() for item in output.split('\n')] if output != '' else []
    return state


'''
Method :: compute plan from domain and problem files
'''

def get_plan(domainFileName, problemFileName):
    output = os.popen(__FD_PLAN_CMD__.format(domainFileName, problemFileName)).read().strip()
    plan   = [item.strip() for item in output.split('\n')] if output != '' else []
    if len(plan) > 0:
        output = os.popen(__FD_PLAN_COST_CMD__).read().strip()
        cost   = int(output)
    else:
        cost = 0

    return [plan, cost]


''' 
Method :: ground PDDL domain and problem files
'''

def ground(domainFileName, problemFileName):

    output = os.system('./clean.sh')
    output = os.system(__GROUND_CMD__.format(domainFileName, problemFileName))



def ground1(domainFileName, problemFileName):

    output = os.system('./clean.sh')
    output = os.system(__GROUND_CMD__.format(domainFileName, problemFileName))





def create_temp_files(domainFileName, problemFileName):

    output = os.system('./clean.sh')
    output = os.system(__CREATE_TMP_CMD__.format(domainFileName, problemFileName))

''' 
Method :: validate plan given PDDL domain and problem files
'''

def validate_plan(domainFileName, problemFileName, planFileName):
    #print __VAL_PLAN_CMD__.format(domainFileName, problemFileName, planFileName)
    output = os.popen(__VAL_PLAN_CMD__.format(domainFileName, problemFileName, planFileName)).read().strip()
    return eval(output)

def plan_graph_test(domainFileName, problemFileName, planFileName):
    #print __GRAPH_TEST_CMD__.format(domainFileName, problemFileName, planFileName)
    output = os.popen(__GRAPH_TEST_CMD__.format(domainFileName, problemFileName, planFileName)).read().strip()
    #exit(0)
    return eval(output)

def find_fail_point(domainFileName, problemFileName, planFileName):
    output = os.popen(__FAIL_POINT_CMD__.format(domainFileName, problemFileName, planFileName)).read().strip()
    if output != '':
        return int(output)
    else:
        return 0



if __name__ == '__main__':
    pass

    ''' debug list '''
    #print validate_plan('../domain/fetchworld-base-m.pddl', '../domain/problem1.pddl', 'sas_plan')
    #state = read_state_from_domain_file('../domain/fetchworld-base-m.pddl')
    #write_domain_file_from_state(state)
