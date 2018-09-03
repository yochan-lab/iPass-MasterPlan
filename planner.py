import os
import re
import subprocess
import problem_generator.compilePDDL as problem_generator
from shutil import copy as copyf
from copy import deepcopy


class Planner():

    def __init__(self):

        self.PLAN_FILES_DIR = './plan_utils/{}'
        self.PDDL_FILES_DIR = 'problem_generator/output/{}'

        # File paths to planning technologies
        self.CALL_FF = self.PLAN_FILES_DIR.format('ff')
        self.CALL_FAST_DOWNWARD = self.PLAN_FILES_DIR.format(
            'FAST-DOWNWARD/fast-downward.py ')
        self.CALL_VAL = self.PLAN_FILES_DIR.format('VAL/validate -v ')
        self.CALL_PR2 = self.PLAN_FILES_DIR.format('PR2/pr2plan ')
        
        # Takes two parameters-- time and command. Eg. timeout 3s ls -l
        self.TIMEOUT_CALL = 'timeout '
        self.TIMEOUT_CODE = 124
        
        # Domain and problem files
        self.domain = self.PDDL_FILES_DIR.format('domain.pddl')
        self.human_domain = self.PDDL_FILES_DIR.format('domain_human.pddl')
        self.problem = self.PDDL_FILES_DIR.format('problem.pddl')

        # Grounded pr-domain and pr-problem files
        self.pr_domain = './pr-domain.pddl'
        self.pr_problem = './pr-problem.pddl'
        self.grounded_pr_domain = self.PLAN_FILES_DIR.format('pr-domain.pddl')
        self.grounded_pr_problem = self.PLAN_FILES_DIR.format(
            'pr-problem.pddl')

        # Plan files
        self.plan_output = './generated_plan'
        self.obs = self.PLAN_FILES_DIR.format('obs.dat')
        self.blank_obs = self.PLAN_FILES_DIR.format('blank_obs.dat')
        self.saveduiPlan = self.PLAN_FILES_DIR.format('saved_obs.dat')

        # Explanation files
        self.exc_file = self.PLAN_FILES_DIR.format('mmp/src/exp.dat')
        self.exp_file = self.PLAN_FILES_DIR.format(
            'mmp_explanations/src/exp.dat')

        # Generating Landmarks
        self.landmark_code = '../RADAR/FD/src/fast-downward.py'
        self.output = './output'

        # Files for storing problem state as a json
        self.problem_state_json = './static/files/state.json'

    '''
    Saves the plan from the frontend to a file that can restore it.
    '''
    def save_plan(self):
        print("[DEBUG] Saving observations in {0} to {1}".format(self.obs, self.saveduiPlan))
        copyf(self.obs, self.saveduiPlan)

    '''
    Loads a saved plan for sending it to the frontend. 
    '''
    def load_plan(self):
        print("[DEBUG] Loading observations from {0} to {1}".format(self.saveduiPlan, self.obs))
        copyf(self.saveduiPlan, self.obs)

    '''
    Given a dict of indexed actions (eg. {0:'a1', '1':a2 ... }), wrties an action list
    with the first validation error (if any) to observation file that will be rendered
    in the frontend.
    '''

    def get_validated_plan(self, actions):
        self.__writeObservations(actions)
        self.__create_grounded_files()

        # Run validate
        out = self.__run_validate(
            self.grounded_pr_domain,
            self.grounded_pr_problem,
            self.obs)

        # Parse VAL's output
        if out:
            if 'Plan failed to execute' in out:
                faults = out.split("Plan Repair Advice:\n")[1].strip()
                if ')' in faults:
                    action_name = faults.split(') ')[0].strip().upper() + ")"
                    reason = faults.split(
                        '\n\n')[0].strip().replace('\n', " : ")

                f = file(self.obs, 'w')
                for k in sorted(actions):
                    print (
                        actions[k].strip('\n( )').lower(),
                        action_name.strip('\n( )').lower())
                    if actions[k].strip('\n( )').lower(
                    ) in action_name.strip('\n( )').lower():
                        f.write(actions[k].strip() + ';' + reason + '\n')
                    else:
                        f.write(actions[k].strip() + '\n')
                f.close()
    
    '''
    Checks if a given plan achieves the goal.
    '''

    def is_plan_complete(self, actions):
        self.__writeObservations(actions)
        self.__create_grounded_files()

        # Run validate
        out = self.__run_validate(
            self.grounded_pr_domain,
            self.grounded_pr_problem,
            self.obs)

        if out:
            if 'The goal is not satisfied' in out:
                return False
        return True

    '''
    Given a dict of indexed actions (eg. {0:'a1', '1':a2 ... }), tried to come up with
    the next (and intermediate) actions that achieve this goal. Finally, they write this to
    the observation file rendered in the frontend and returns,
    False -- if -- pr2plan times out when finding a plan OR plan generated is empty
    True -- otherwise.
    '''

    def get_suggested_plan(self, actions, tillEndOfPresentPlan=False):
        self.__writeObservations(actions)
        self.__create_grounded_files()
        
        # Run pr2plan and plan
        self.__run_pr2(
            self.grounded_pr_domain,
            self.grounded_pr_problem,
            self.obs)
        timeout_status = self.__plan(self.pr_domain, self.pr_problem, '10s')
        
        # If timeout occured, pr2 could not find a plan in 10s
        if timeout_status == self.TIMEOUT_CODE:
            print('[WARNING] Timeout occured')
            return False
        
        # Write plan to observation file
        with open(self.plan_output, 'r') as f:
            lines = f.read().strip()

        # Check if the generated plan is empty
        if not lines:
            print('[WARNING] Empty plan occured')
            return False
        
        lines = lines.split('\n')
        i = 0
        plan_actions = {}
        for l in lines:
            if '(general cost)' not in l:
                if 'EXPLAIN_OBS_' in l.upper():
                    # Remove prefix and postfix of PR2 modified action name
                    # for user added actions
                    a = l.upper().replace('EXPLAIN_OBS_', '').strip()
                    a = re.sub('_[0-9]*$', '', a)
                    plan_actions[i] = '({})'.format(a)
                else:
                    # Append ;-- to PR2 generated, i.e. suggested actions
                    plan_actions[i] = '({});--'.format(l.upper().strip())
                i += 1

        self.__writeObservations(plan_actions, tillEndOfPresentPlan)
        return True
    
    '''
    Returns the plan in the observation file as a action list.
    '''
    def get_action_sequence_list(self):
        with open(self.obs, 'r') as f:
            actions = f.readlines()

        return [a.strip() for a in actions]


    '''
    Create pr-problem and pr-domain files with no observations for getting a domain and
    problem file with grounded action names.
    '''

    def __create_grounded_files(self):
        self.__run_pr2(self.domain, self.problem, self.blank_obs)
        
        # Remove the proposition EXPLAINED_FULL_OBS_SEQUENCE from
        # the goal state that makes the problem infeasible.
        with open(self.pr_problem, 'r') as f:
            lines = f.read().split('\n')
        
        s = ''
        for line in lines:
            if 'EXPLAINED_FULL_OBS_SEQUENCE' in line:
                continue
            s += "{}\n".format(line.strip())
        s = s.strip()
        
        with open(self.pr_problem, 'w') as f:
            f.write(s)
        
        copyf(self.pr_domain, self.grounded_pr_domain)
        copyf(self.pr_problem, self.grounded_pr_problem)

    '''
    Given a dictionary of indexed actions (eg. {0:'a1', '1':a2 ... }), writes the action
    list to the observation file that will be rendered in the frontend.
    '''

    def __writeObservations(self, actions, tillEndOfPresentPlan=False):

        if tillEndOfPresentPlan:
            acts = deepcopy(actions)
            # Traverse from the end and break when you find the action causing
            # the validation error (indicated by ';--'
            for i in range(len(acts.keys()) - 1, 0, -1):
                if ';--' not in acts[i]:
                    break
            actions = {}
            for j in range(0, i + 1):
                actions[j] = acts[j]

        # Write plan to file in sas_plan style
        s = ''
        for k in sorted(actions):
            s += actions[k].strip() + '\n'

        f = file(self.obs, 'w')
        f.write(s)
        f.close()

    '''
    Function to call pr2 plan. Saves pr-problem and pr-domain files in the home directory.
    '''
    
    def __run_pr2(self, domain_file, problem_file, obs_file):
        print(
            '[INFO] Running pr2plan with the following files:\ndomain:{}\nproblem:{}\nobservation:{}'.format(
                domain_file,
                problem_file,
                obs_file))
        try:
            cmd = self.CALL_PR2 + ' -d ' + domain_file + \
                ' -i ' + problem_file + ' -o ' + obs_file
            os.system(cmd)
        except BaseException:
            print('[ERROR] Call Failed!')

    '''
    Function to call validate. Returns the output as a string.
    '''

    def __run_validate(self, domain_file, problem_file, obs_file):
        try:
            cmd = self.CALL_VAL + \
                ' {} {} {}'.format(domain_file, problem_file, obs_file)
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
            (out, err) = proc.communicate()
            return out
        except BaseException:
            print(
                '[ERROR] Failed to execute VAL with the given files:\ndomain:{}\nproblem:{}\nobservation:{}'.format(
                    domain_file,
                    problem_file,
                    obs_file))

    def __remove_costs(self, file_name):
        with open(file_name, 'r') as f:
            lines = f.read().split('\n')

        s = ''
        for line in lines:
            if 'increase' in line \
                or 'functions' in line \
                or 'total-cost' in line:
                # These keywords indicate that the line relates to
                # functions with action costs. Skip them.
                continue
            s += "{}\n".format(line.strip())
            
        s = s.replace(':action-costs', '')
        
        with open(file_name, 'w') as f:
            f.write(s)

    '''
    Given a domain and problem file, generates a plan.
    '''

    def __plan(self, domain_file=None, problem_file=None, use='ff', timeout='10s'):

        # Initiate domain and problem files, if not provided by caller.
        if domain_file is None:
            domain_file = self.domain
        if problem_file is None:
            problem_file = self.problem

        print(
            '[INFO] Using ff to find plan. Args:\nDomain: {}\nProblem: {}'.format(
                domain_file,
                problem_file))

        # Since ff cannot handle action cost, remove them
        self.__remove_costs(domain_file)
        self.__remove_costs(problem_file)

        # Run ff
        cmd = self.CALL_FF + \
            " -o %s -f %s | grep -E '[0-9]: ' | awk -F': ' '{print $2}' > %s" % (domain_file, problem_file, self.plan_output)
        status_code = os.system(self.TIMEOUT_CALL + timeout + ' ' + cmd)
        return status_code

    def reconcileModels(self, changes):
        print(changes)
        changeHumanModel = []
        changeRobotModel = []
        for key in changes.keys():
            if '-reject' in key:
                act = key.split('-reject')[0]
                changeRobotModel.append(act)
                changes.pop(key, None)
                changes.pop(act, None)

        for key in changes.keys():
            changeHumanModel.append(key)

        self.updateDomainFile(
            self.domain.split('.pddl')[0] +
            '_human.pddl',
            changeHumanModel)
        self.updateDomainFile(self.domain, changeRobotModel, True)

    def updateDomainFile(self, fname, changes, remove=False):
        if not changes:
            return

        act_updates = {}
        for c in changes:
            act, pre = c.split('-has-precondition-')
            act_updates[act] = pre

        print(
            "Updating ...\nfile: {0}\nremove: {1}\nchanges: {2}".format(
                fname,
                remove,
                act_updates))
        f = open(fname, 'r')
        s = ""
        removePredicate = False
        for l in f:
            if removePredicate:
                if prec in l:
                    removePredicate = False
                    continue
            if '(:action ' in l:
                act_name = l.split(':action ')[1].strip()
                try:
                    prec = act_updates[act_name]
                    if remove:
                        s += l
                        removePredicate = True
                    else:
                        s += l
                        s += prec + "\n"
                except BaseException:
                    s += l
                    continue
            else:
                s += l
        f.close()
        f = open(fname.split('.pddl')[0] + '_modify.pddl', 'w')
        f.write(s)
        f.close()
        print(
            "Updated '{0}'!".format(
                fname.split('.pddl')[0] +
                '_modify.pddl'))
        if remove:
            self.domain = fname.split('.pddl')[0] + '_modify.pddl'
        else:
            self.human_domain = fname.split('.pddl')[0] + '_modify.pddl'

    def getExplanations(self):

        cmd = "cd ./planner/mmp_explanations/src && ./Problem.py -m ../../../{0} -n ../../../{1} -d ../domain/radar_domain_template.pddl -f ../../mock_problem.pddl".format(
            self.domain, self.human_domain)
        try:
            os.system(cmd)
        except BaseException:
            print("[ERROR] while generating explanations for the present plan")

        try:
            f = open(self.exp_file, 'r')
        except BaseException:
            print(
                "[WARNING] No explanations were generated.  Probably there is no model difference")
            return {1: "None"}
        reason = {}
        i = 1
        for l in f:
            s = l.strip()
            if not s:
                continue
            s = l.split('Explanation >> ')[1].strip()
            reason[i] = s
            i += 1
        return reason

    def getExcuses(self):
        cmd = "cd ./planner/mmp/src && ./Problem.py -m ../domain/radar_domain.pddl -n ../domain/radar_domain.pddl -d ../domain/radar_domain_template.pddl -q ../domain/complete_initial_state_problem_template.pddl -f ../domain/complete_initial_state_problem.pddl -t ../../mock_problem.pddl"
        try:
            os.system(cmd)
        except BaseException:
            print(
                "[ERROR] Error while generation explanations for changing initial state to make it feisable")

        f = open(self.exc_file, "r")
        reason = ''
        for l in f:
            s = l.strip()
            if not s:
                continue
            s = l.split('Explanation >> has-initial-state-')[
                1].replace("has_", "Get ").replace("_number@", " ")
            reason = reason + s + ' '
        plan_actions = {
            '1': 'INVALID_INITIAL_STATE ;{0}'.format(
                reason.replace(
                    '\n', ' '))}
        return plan_actions

    def deletePrFiles(self):
        try:
            os.remove(self.pr_domain)
            os.remove(self.pr_problem)
        except BaseException:
            print(
                "[WARNING] Problem deleting pr-domain and pr-problem files.  Probably they already don't exist!")

    def getActionNames(self):
        self.deletePrFiles()
        try:
            cmd = self.CALL_PR2 + ' -d ' + self.domain + ' -i ' + self.problem + \
                ' -o ' + self.PLAN_FILES_DIR.format('blank_obs.dat')
            os.system(cmd)
        except BaseException:
            raise Exception('[ERROR] Call to PR2 failed!')

        if not os.path.isfile(
                self.pr_domain) or not os.path.isfile(
                self.pr_problem):
            print("[ERROR] Goal cannot be reached from initial state")
            return []

        try:
            cmd = 'cat pr-problem.pddl | grep -v "EXPLAIN" > pr-problem.pddl.tmp && mv pr-problem.pddl.tmp pr-problem.pddl'
            os.system(cmd)
            cmd = 'cat pr-domain.pddl | grep -v "EXPLAIN" > pr-domain.pddl.tmp && mv pr-domain.pddl.tmp pr-domain.pddl'
            os.system(cmd)
        except BaseException:
            raise Exception(
                '[ERROR] Removing "EXPLAIN" from pr-domain and pr-problem files.')

        actionNames = []
        f = open('./pr-domain.pddl')
        for l in f:
            if '(:action ' in l:
                actionNames.append('(' + l.split('(:action ')[1].strip() + ')')
        return actionNames

    def getImpResources(self):
        try:
            f = file(selt.sas_plan, 'r')
        except BaseException:
            # If no plan exists for the present state
            self.plan()
            f = file(self.sas_plan, 'r')

        # Write plan to observation file
        resources = []
        for l in f:
            for r in self.resource_list:
                if (r in l.lower()) and (r not in resources):
                    resources.append(r)
        return resources

        '''
    Creates the problem.pddl file
        @Input - Goal for which planning problem is to be made
        @Output - Creates problem.pddl
    '''

    def definePlanningProblem(self):
        problem_state = problem_generator.generateState()

        # Get pddl file from problem state
        problem_generator.compile2pddl(problem_state)

        # Write json to file for ui
        with open(self.problem_state_json, 'w') as f:
            f.write(problem_state)
