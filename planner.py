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

        # Domain and problem files
        self.domain = self.PDDL_FILES_DIR.format('domain.pddl')
        self.human_domain = self.PDDL_FILES_DIR.format('domain_human.pddl')
        self.problem = self.PDDL_FILES_DIR.format('problem.pddl')

        # Grounded pr-domain and pr-problem files
        self.pr_domain = './pr-domain.pddl'
        self.pr_problem = './pr-problem.pddl'
        self.val_pr_domain = self.PLAN_FILES_DIR.format('pr-domain.pddl')
        self.val_pr_problem = self.PLAN_FILES_DIR.format('pr-problem.pddl')

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
    Writes a dict of indexed actions into the observation file.
        @Input
            actions - Dict of indexed actions eg. {0:'a1', '1':a2 ... }
            @Optional tillEndOfPresentPlan - Consider the plan only till the last validated action. Used for
                                             fixing a validation error or a parital plan.
        @Output
            Writes the action list to a file in sas style
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
    Validate - validates a plan
        @Input
            Dict of indexed actions eg. {0:'a1', '1':a2 ... }
        @Outputs
            wrties action list with validation error to observation file
    '''
    def getValidatedPlan(self, actions):
        # Save plan from UI to observation file
        self.__writeObservations(actions)
        
        # Create pr-problem and pr-domain files with no observation for validate to use
        cmd = self.CALL_PR2 + ' -d ' + self.domain + \
                    ' -i ' + self.problem + ' -o ' + self.blank_obs
        os.system(cmd)
        copyf(self.pr_domain, self.val_pr_domain)
        copyf(self.pr_problem, self.val_pr_problem)

        # Run validate
        try:
            cmd = self.CALL_VAL + \
                  ' {} {} {}'.format(self.val_pr_domain, self.val_pr_problem, self.obs)
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
            (out, err) = proc.communicate()
        except BaseException:
            print('[ERROR] Failed to execute VAL on given plan!')

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
    Generates a plan.
        @Input
            @Optional use - whether to use Fast Forward of Fast Downward
        @Output
            Writes the output to a observation
    '''

    def plan(self, use='ff'):
        try:
            if use == 'ff':
                cmd = self.CALL_FF + \
                    " -o {} -f {} | grep -E '[0-9]: '".format(self.domain, self.problem, self.plan_output)
                proc = subprocess.Popen(
                    cmd, stdout=subprocess.PIPE, shell=True)
                (out, err) = proc.communicate()
                f = open(self.plan_output, 'w')
                f.write(out.replace('step', '').strip())
                f.close()
                print('Fast FOrward called...')
            else:
                cmd = self.CALL_FAST_DOWNWARD + self.pr_domain + ' ' + \
                    self.pr_problem + ' --search "astar(lmcut())"'
            os.system(cmd)
            print('FAST-DOWNWARD called...')
        except BaseException:
            raise Exception('[ERROR] While trying to run planner.')

    '''
    def getLandmarks(self):
        try:
            cmd = '{0} {1} --landmarks name=lm_zg'.format(self.landmark_code, self.output)
            os.system(cmd)
        except:
            raise Exception('[ERROR] In generating landmarks')

        f = open('landmark.txt', 'r')
        lm = []
        for l in f:
            if 'explained' not in l.lower():
                lm.append( l.split('Atom ')[1] )
        return lm
    '''

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

    def getSuggestedPlan(self, actions, tillEndOfPresentPlan=False):
        self.__writeObservations(actions)

        # If actions are blank, use the present pr_domain and pr_problem files to plan. If not, generate new files with the known actions to be explained.
        if actions:
            # Save the present domain
            copyf(self.pr_domain, self.val_pr_domain)
            copyf(self.pr_problem, self.val_pr_problem)
            try:
                os.system('\n=====\ncat {0}\n======\n'.format(self.obs))
                cmd = self.CALL_PR2 + ' -d ' + self.val_pr_domain + \
                    ' -i ' + self.val_pr_problem + ' -o ' + self.obs
                os.system(cmd)
            except BaseException:
                raise Exception('[ERROR] In Call to PR2!')

        self.plan()

        # Write plan to observation file
        plan_actions = {}
        f = file(self.sas_plan, 'r')
        i = 0
        acts = [x.strip('() \n') for x in actions.values()]
        for l in f:
            if '(general cost)' not in l:
                if 'EXPLAIN_OBS_' in l.upper():
                    a = l.upper().replace('EXPLAIN_OBS_', '').strip()
                    plan_actions[i] = re.sub('_[0-9]', '', a)
                    i += 1
                    '''
                    for a in acts:
                        if a.upper() in l.upper():
                            plan_actions[i] = '(' + a.upper().strip() + ' )'
                            i += 1
                            break
                    '''
                else:
                    plan_actions[i] = l.upper().strip() + ';--'
                    i += 1
        f.close()
        self.__writeObservations(plan_actions, tillEndOfPresentPlan)

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
            cmd = self.CALL_PR2 + ' -d ' + self.domain + ' -i ' + \
                self.problem + ' -o ' + self.PLAN_FILES_DIR.format('blank_obs.dat')
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

    def savePlan(self):
        copyf(self.obs, self.saveduiPlan)

    def loadPlan(self):
        print("[LOG] Copying {0} to {1}".format(self.saveduiPlan, self.obs))
        copyf(self.saveduiPlan, self.obs)

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

    def getOrderedObservations(self):
        observations = {}
        f = open(self.obs)
        count = 1
        for l in f:
            observations[count] = l.strip()
            count += 1
        return observations

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
