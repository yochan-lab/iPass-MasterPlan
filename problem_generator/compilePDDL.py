#!/usr/bin/env python

'''
import packages
'''

import random, json
import argparse

'''
global variables
'''
CONFIG_FILES_DIR = './problem_generator/config/{}'
PDDL_FILES_DIR = './problem_generator/output/{}'

# list of committee members and their properties
with open(CONFIG_FILES_DIR.format('committee.json'), 'r') as committee_file:
    temp = committee_file.read()
    committee_dict = json.loads(temp)

# list of courses and their properties
with open(CONFIG_FILES_DIR.format('courses.json'), 'r') as courses_file:
    temp = courses_file.read()
    courses_dict = json.loads(temp)

'''
method :: generate random state configuration
'''

def generateState():

    # sample state configuration
    with open(CONFIG_FILES_DIR.format('state.json'), 'r') as state_file:
        stateJSON = state_file.read()
        
    state_dict = json.loads(stateJSON)

    for course in state_dict['deficiency']:

        if random.randint(0, 1): state_dict['deficiency'][course] = "yes"
        else:                    state_dict['deficiency'][course] = "no"
            
    if random.randint(0, 1): state_dict['ra/ta'] = "yes"
    else:                    state_dict['ra/ta'] = "no"
    
    if random.randint(0, 1): state_dict['international'] = "yes"
    else:                    state_dict['international'] = "no"

    specialization_options       = ["big data", "ai", "cybersecurity"]
    state_dict['specialization'] = specialization_options[random.randint(0, 2)]
    
    return json.dumps(state_dict)


'''
method :: compile JSON to random problem instance
'''

def compile2pddl(stateJSON):

    # template file for problem instance
    with open(PDDL_FILES_DIR.format('template.pddl'), 'r') as template_file:
        template = template_file.read()

    temp_dict = {}

    for course in courses_dict:

        if courses_dict[course][1] not in temp_dict:
            temp_dict[courses_dict[course][1]] = []

        temp_dict[courses_dict[course][1]].append(str(course))

    course_block = ''

    for key in temp_dict:
        course_block += '{} - {}\n'.format( ' '.join(temp_dict[key]), key)

    template = template.replace('[COURSES]', course_block)

    professor_block       = '{} - {}'.format(' '.join(committee_dict.keys()), 'professor')
    state_professor_block = '\n'.join( ['(is_{} {})'.format(committee_dict[professor][1], professor) for professor in committee_dict] )

    template = template.replace('[PROFESSORS]', professor_block).replace('[PROFESSOR_BLOCK]', state_professor_block)

    state_dict = json.loads(stateJSON)

    deficiency_block = '\n'.join( ['(has_taken {})'.format(course) if state_dict['deficiency'][course] == 'yes' else ''  for course in state_dict['deficiency']] )
    
    template = template.replace('[DEFICIENCY_BLOCK]', deficiency_block)

    if state_dict['ra/ta'] == 'yes':
        template = template.replace('[IS_RA_TA]', '(is_ra_ta)')
    else:
        template = template.replace('[IS_RA_TA]', '')
        
    if state_dict['international'] == 'yes':
        template = template.replace('[IS_INTERNATIONAL]', '(is_international)')
    else:
        template = template.replace('[IS_INTERNATIONAL]', '')
        
    if state_dict['specialization'] != 'yes':
        template = template.replace('[SPECIALIZATION]', '(specialized_in_{})'.format(state_dict['specialization'].replace(' ', '_')))
    else:
        template = template.replace('[SPECIALIZATION]', '')

    # if not required, comment out i/o for speed 
    with open(PDDL_FILES_DIR.format('problem.pddl'), 'w') as problem_file:
        problem_file.write(template)
        
    return template

        
'''
method :: main
'''

def main():

    parser = argparse.ArgumentParser(description='Make PDDL files for planner.')
    parser.add_argument('-f', '--file', default=CONFIG_FILES_DIR.format('state.json'), help='path to json file for state information')

    args = parser.parse_args()

    with open(args.file) as state_file:
        stateJSON = state_file.read()

    #print generateState()
    #print ss
    #problem = compile2pddl(ss) 


if __name__ == '__main__':
    main()
