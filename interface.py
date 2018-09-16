import json

class Interface:
    def __init__(self, connector = "_"):
        path = "problem_generator/config/"
        self.courses = self.getData(path + "courses.json")
        self.committee = self.getData(path + "committee.json")
        self.cache = dict()
        self.connector = connector
        self.num = [
            "ZERO", "ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE", "TEN",
            "ELEVEN", "TWELVE", "THIRTEEN", "FOURTEEN", "FIFTEEN", "SIXTEEN", "SEVENTEEN",
            "EIGHTEEN", "NINETEEN", "TWENTY", "TWENTYONE", "TWENTYTWO", "TWENTYTHREE", "TWENTYFOUR",
            "TWENTYFIVE", "TWENTYSIX", "TWENTYSEVEN", "TWENTYEIGHT", "TWENTYNINE", "THIRTY"
        ]
        self.mapper = {
            "deficiency": "TAKE_DEFICIENCY_COURSE",
            "normal": "TAKE_NORMAL_COURSE",
            "Complete Semester": "COMPLETE_SEMESTER",
            "Add Chair": "SELECT_COMMITTEE_CHAIR",
            "Add Committee": "SELECT_COMMITTEE_MEMBER",
            "Defend": "DEFEND",
            "Complete Deficiency": "COMPLETE_DEFICIENCY",
            "Complete Foundations": "COMPLETE_FOUNDATIONS",
            "Complete Applications": "COMPLETE_APPLICATIONS",
            "Complete Systems": "COMPLETE_SYSTEMS",
            "Thesis Course A": "TAKE_CSE599A",
            "Thesis Course B": "TAKE_CSE599B",
            "Add Specialization": "SPECIALIZE"
        }
        self.invert_mapper = {
            "TAKE_DEFICIENCY": "Add Course - ",
            "TAKE_NORMAL": "Add Course - ",
            "TAKE_CSE599A": "Add Course - Thesis Course A (other)",
            "TAKE_CSE599B": "Add Course - Thesis Course B (other)",
            "SELECT_COMMITTEE_CHAIR": "Add Chair - ",
            "SELECT_COMMITTEE_MEMBER": "Add Committee - ",
            "SPECIALIZE": "Add Specialization - ",
            "DEFEND": "Add - Defense",
            "COMPLETE_SEMESTER": "Add - End of Semester"

        }
        self.feedback = {
            "current_num": "Completing 10 courses",
            "sem_quota": "Completing preferred number of course(s) in the Semester",
            "has_committee": "Chosing committee members and chairs",
            "has_taken": "Completing {} course",
            "has_taken_cse599b": "Completing thesis credits",
            "has_taken_cse599a": "Completing thesis credits",
            "completed_deficiency": "Completing deficiency courses",
            "chair_expertise": "Chosing an advisor for your thesis work from {} specialization",
            "completed_specialization": "Completing specialization specific courses for AI, Big Data or Cybersecurity",
            "completed_concentration": "Completing foundation, systems and application concentrations",
            "defended": "Defending thesis work",
            "not-is_international": "As an international student, taking less than 3 courses in a semester",
            "not-is_ra_ta": "Taking less than 3 courses if you are an RA/TA",
            "is_ra_ta": "Only an RA/TA can take 4 courses in a semester",
            "is_international": "An international student needs to take atleast 3 courses in a semester",
            "not-has_taken": "Taking the same course {}, twice",
            "not-sem_quota": "Taking less than 1 course and more than 4 courses,",
            "not-current_num": "Adding more than 10 courses in the iPOS",
            "not-selected": "Adding the same professor {}, twice in your committee",
            "not-completed_specialization": "Adding the same specialization twice,",
            "not-has_committee_chair": "Adding more than 1 chair to the committee",
            "not-has_committee_member": "Adding more than 2 members (other than the chair)"
        }

        self.actions = {
            "take_normal_course": "Adding normal course",
            "take_deficiency_course": "Adding deficiency course",
            "take_cse599a": "Adding thesis credit a",
            "take_cse599b": "Adding thesis credit b",
            "complete_semester": "End of Semester",
            "select_committee_chair": "Selecting committee chair",
            "select_committee_member_2": "Selecting second committee member",
            "select_committee_member_3": "Selecting third committee member",
            "defend": "Scheduling defense action",
            "specialize_big_data": "Completing Big Data specialization",
            "specialize_ai": "Completing AI specialization",
            "specialize_cybersecurity": "Completing Cybersecurity specialization"
        }

        self.predicates = {
            "chair_expertise": "chair to be an expert in the area of specialization",
            "is_expert": "chair to be an expert in the area of specialization",
            "is_concentration": "the course from each concentration",
            "has_committee_chair_done": "having a chair in the committee",
            "has_committee_chair": "having a chair in the committee",
            "selected": "member is selected",
            "has_taken CSE599a": "completing first thesis courses",
            "has_taken CSE599b": "taking both the thesis courses",
            "has_taken": "completing the deficiency courses",
            "has_committee_member2": "second committee member",
            "has_committee_member3": "third committee member",
            "completed_concentration": "completing concentration of foundation, algorithm and systems",
            "completed_specialization": "completing specialization of AI, Big Data or Cybersecurity",
            "sem_quota": "student to not take 4 courses in the semester",
            "current_num": "student to take 10 courses",
            "is_concentration": "course has appropriate concentration for student to complete",
            "specialize-has_taken": "student to complete specialization specific courses"
        }

    def getData(self, file_name):
        with open(file_name, 'r') as f:
            data = json.load(f)

        return data

    '''
    Given an output plan (list of actions) with validation or suggesting action markers,
    generated the corresponding dictionary of actions that can be displayed in the UI.
    '''
    def actionsToUI(self, actions, is_explanations=False):
        # print ("[DEBUG] PDDL to UI : ", actions)
        
        # New action dict since some actions in the old list may
        # be omitted.
        ui_actions = {}

        if is_explanations:
            for k in actions.keys():
                if ";" not in actions[k]:
                    continue

                action, explanation = actions[k].split(";")
                actionArray = self.__action_to_array(action)
                if not actionArray:
                    continue    
                act = self.__invertor(actionArray)
                explanation = self.__get_explanation(explanation)
                if not act:
                    continue
                act += ";"
                if explanation:
                    ui_actions[k] = act + explanation
                else:
                    ui_actions[k] = act + "~~~"

            return ui_actions
        
        # code for feedback on validate and 
        idx = 0
        self.global_feedback = []
        for action in actions:
            # resetting the parameters for the loop
            has_property = False
            act = None
            a_property = ""
            # Check if action is a validated or suggested action
            if ";" in action:
                action, a_property = action.split(";")
                has_property = True

            actionArray = self.__action_to_array(action)

            if not actionArray:
                continue

            act = self.__invertor(actionArray)
            if act is not None:
                # action has a ui_action mapping
                if has_property:
                    act += ";" + self.__getFeedback(a_property)
                ui_actions[idx] = str(act)
                #whenever there is an action increment the index
                idx += 1

        #print ("[DEBUG] final actions from interface: ", ui_actions)
        return ui_actions

    '''
    Takes as input actions from the ui (gridstack action list)
    and returns PDDL grounds actions that can be mapped to pr-domain operators.
    '''
    def uiToActions(self, ui_actions):
        # Initializing global variables everytime request comes from the frontend
        #print ("[DEBUG] UI to PDDL: ", ui_actions)
        ui_actions.sort(key = lambda action: action['y'])
        self.course_counter = 0
        self.sem_counter = 0
        self.committee_counter = 1
        self.committee_members = []

        actions = {}
        end_sem_count_booster = 0
        for action in ui_actions:
            action_pos = int(action['y'])
            action_list = self.__get_action_name(action['name'])

            for i in range(len(action_list)):
                if i > 0:
                    end_sem_count_booster += 1
                actions[action_pos+end_sem_count_booster] = "({})".format(action_list[i])

        #print ("[DEBUG] ui_actions converted in interface : ", ui_actions)
        return actions

    '''
    Returns action name split by _
    '''
    def __action_to_array(self, action):
        # Map the action name to UI action name
        action = action[1: -1]
        # splits the action to convert an array. In case of empty string we go to next action.
        if "_" in action:
            actionArray = action.split("_")
        elif action:
            actionArray = [action]
        else:
            actionArray = None

        return actionArray

    def __get_action_name(self, action_name):
        if "-" in action_name:
            act = action_name.split("-")
            act = [x.strip() for x in act]
        actionType = act[0]
        if act[0] == "Add":
            if act[1].find("Semester") > -1:
                actionType = "Complete Semester"
            else:
                actionType = "Defend"
        #print "[DEBUG] __get_action_name parameters: ", actionType, act      
        return [str(x) for x in self.__converter(actionType, act[1])]

    def __invertor(self, action):
        switch = {
            "TAKE": self.__invertCourse,
            "SELECT": self.__invertCommittee,
            "COMPLETE": self.__invertSemester,
            "SPECIALIZE": self.__invertSpecialization,
        }
        func = switch.get(action[0], self.__defaultInvertor)

        return func(action)

    def __converter(self, action, name):
        switch = {
            "Add Course": self.__addCourse,
            "Add Chair": self.__addChairAndCommittee,
            "Add Committee": self.__addChairAndCommittee,
            "Complete Semester": self.__endSemester,
            "Defend": self.__defend,
            "Add Specialization": self.__specialization
        }

        func = switch.get(action, self.__defaultConvertor)
        return func(action, name)

    def __addChairAndCommittee(self, action, name):
        prof, specialization = self.__find(self.committee, name)
        if prof is None:
            return None

        prof = prof.upper()
        act = self.mapper[action]
        if action == "Add Committee":
            if self.committee_counter < 3:
                self.committee_counter += 1
            act += "_" + str(self.committee_counter)
            self.committee_members.append(prof)
        else:
            self.committee_members = [prof] + self.committee_members

        act += self.connector + prof
        if " " in specialization:
            specialization = specialization.replace(" ", "_")

        if action == "Add Chair":
            act += self.connector + specialization.upper()
        return [act]

    '''
    ' where ever _ is used instead of the connector - it is because whatever the next
    ' string is, it is a part of the action and not a parameter to the action
    '''
    def __specialization(self, action, name):
        name = name if " " not in name else name.replace(" ", "_")
        return [self.mapper[action] + "_" + name.upper()]

    def __endSemester(self, action, name):
        actions = []
        if 0 < self.sem_counter < 5:
            actions.append(self.mapper[action] + "_" + str(self.sem_counter))

        self.sem_counter = 0
        actions.append(self.mapper[action])
        return actions

    def __defend(self, action, name):
        return [self.mapper[action]]

    def __defaultConvertor(self, action, name):
        return [self.mapper[action] + self.connector + name.upper()]

    def __addCourse(self, action, name):
        if name in self.cache:
            course, course_type = self.cache[name]
            temp = "deficiency" if course_type == "deficiency" else "normal"
            action =    self.mapper[temp] + self.connector +\
                        course.upper() + self.connector
            course_type = course_type.lower()
        else:
            if "Thesis" in name:
                name = self.__removeType(name)
                action =    self.mapper[name]
                course_type = ""
                temp = "normal"
            else:
                course, course_type = self.__find(self.courses, name)
                if course is None:
                    return None
                self.cache[name] = [course, course_type]
                temp = "deficiency" if course_type == "deficiency" else "normal"
                action =        self.mapper[temp] + self.connector + course.upper() + self.connector

        if temp == "normal":
            action +=   course_type.upper() + self.connector

        incremented     = self.course_counter + 1 if self.course_counter < 10 else 10
        sem_incremented = self.sem_counter + 1 if self.sem_counter < 10 else 10

        action +=           self.num[self.course_counter] + self.connector +\
                            self.num[incremented] + self.connector +\
                            self.num[self.sem_counter] + self.connector +\
                            self.num[sem_incremented]

        if course_type != "deficiency": self.course_counter += 1
        self.sem_counter += 1

        return [action]

    def __find(self, data, name):
        name = self.__removeType(name)
        for key in data.keys():
            if data[key][0] == name:
                return key, data[key][1]

        print "No value found for ", name
        return None, None

    def __removeType(self, name):
        return name.split("(")[0].strip()

    def __invertSemester(self, actionStrings):
        key = "_".join(actionStrings[0:2])
        # Look at COMPLETE_SEMEMSTER_x actions for sending the
        # COMPLETE_SEMSTER action back.
        if len(actionStrings) == 3:
            return self.invert_mapper[key]

        return None

    def __invertSpecialization(self, actionStrings):
        length = len(actionStrings)
        if length == 2 and len(actionStrings[1]) == 2:
            specialization = "AI"
        elif length == 2:
            specialization = "Cybersecurity"
        else:
            specialization = "Big Data"

        return self.invert_mapper[actionStrings[0]] + specialization

    def __invertCommittee(self, actionStrings):
        key = "_".join(actionStrings[0:3])
        profName = actionStrings[3].title()
        if "MEMBER" in key:
            profName = actionStrings[4].title()
        prof = self.committee[profName]
        prof[1] = prof[1] if "_" not in prof[1] else prof[1].replace("_", " ")
        action = self.invert_mapper[key] + prof[0] + " (Specialization: " + prof[1] + ")"
        return action

    def __invertCourse(self, actionStrings):
        key = "_".join(actionStrings[0:2])
        if "CSE" in actionStrings[1]:
            # find UI name for CSE599A and CSE599B
            action = self.invert_mapper[key]
        else:
            # UI name for all other courses
            course = self.courses[actionStrings[3]]
            action = self.invert_mapper[key] + course[0] + " (" + course[1] + ")"

        return action

    def __defaultInvertor(self, actions):
        return self.invert_mapper[actions[0]]

    '''
    ' converts val un-met predicates to readable feedback
    '''
    def __getFeedback(self, soup):
        if soup == "--":
            return soup
        elif soup == "Invalid Action":
            return soup
        #print "[DEBUG] feedback string from interface ", soup

        string_for_true = "{} <b>before</b> the action required"
        string_for_false = "{}, can not be done"
        ui_feedback = []

        if ":" in soup:
            # check if the sentence has predicates or talks about
            # the predicates missing in any of the actions.
            ingredients = soup.split(":")
            for spices in ingredients:
                # each sub sentence has the predicates that are
                # have to be set as true or false
                # these are the preconditions that are not met
                if "Set" in spices:
                    # this has a predicate which needs to be checked
                    important_spice     = spices.split("(")[-1]
                    condition_of_spice  = important_spice.split(")")
                    # exact predicate which has to be checked
                    important_spice     = condition_of_spice[0]
                    # is it to be set to true or set to false
                    is_it_spicy         = condition_of_spice[1]
                    spice               = self.__formatFeedback(important_spice)
                    # convert the predicate to human readable feedbak
                    if "false" in is_it_spicy or "not" in important_spice :
                        fb = string_for_false.format(spice)
                    else:
                        fb = string_for_true.format(spice)
                    # ensuring similar UI feedbacks are not given to the user
                    if fb not in ui_feedback and fb not in self.global_feedback:
                        ui_feedback.append(fb)
                        self.global_feedback.append(fb)

        return ";".join(ui_feedback)

    def __formatFeedback(self, spice):
        # default case like defended, cse599a or cse599b is
        # handled from this key
        key = spice
        if "not-has_taken" in spice:
            key         = spice[0:13]
            f           = self.feedback[key]
            course      = spice[14:21].upper()
            return f.format(self.courses[course][0] + " (" + course +  ")")
        elif "not-sem_quota" in spice:
            key         = spice[0:13]
        elif "not-current_num" in spice:
            key         = spice[0:15]
        elif "not-selected" in spice:
            key         = spice[0:12]
            f           = self.feedback[key]
            prof        = spice[13:]
            return f.format(self.committee[prof.title()][0])
        elif "not-completed_specialization" in spice:
            key         = spice[0:28]
        elif "not-has_committee_chair" in spice:
            key         = spice[0:23]
        elif "not-has_committee_member" in spice:
            key         = spice[0:24]
        elif "has_taken" in spice and "cse599" not in spice:
            #condition for course related feedback
            # all other kind of courses
            key         = spice[0:9]
            f           = self.feedback[key]
            course      = spice[10:16].upper()
            course      = self.courses[course][0] + " (" + course + ")"
            return f.format(course)
        elif "chair_expertise" in spice:
            # chair for the expertise has to be selected
            key         = spice[0:15]
            f           = self.feedback[key]
            expertise   = spice[16:]
            if "_" in expertise: expertise = expertise.replace("_", " ")
            return f.format(expertise)
        elif "has_committee" in spice:
            # all committee related feedbacks have same comment
            key         = spice[0:13]
        elif "completed_concentration" in spice:
            # all concentration have one message, to ensure there
            # are no biases against a specific concentration
            key         = spice[0:23]
        elif "current_num" in spice:
            # any number of courses can be asked for completion
            # for different actions. I end up showing message for
            # 10 courses only. because it does not make sense that
            # I show complete one course in the case validate says
            # current_num_one to true
            key         = spice[0:11]
        elif "sem_quota" in spice:
            # preferred courses are what I say in the message
            key         = spice[0:9]

        return self.feedback[key]

    def __get_explanation(self, explanation):
        explanations = []
        ui_explanations = []
        if "\n" not in explanation:
            # only one explanation
            if ">>" not in explanation:
                # not even one explanation 
                return None
            else:
                explanations = [explanation]
        else:
            explanations = explanation.split("\n")

        # error handling completed
        if not explanations:
            return None

        for exp in explanations:
            # there is only one, there are two values after splitting
            # difference tells the kind of model difference
            # predicate is the predicate which is different
            if not exp:
                continue

            difference, predicate = [x.strip().strip("'") for x in exp[1:-1].split(",")]
            # removed the condition as we need to put the add and delete
            # model differences back in the model.
            #if "ADD" in difference:
            #    continue
            pred = self.__convert_predicate(predicate)

            #print predicate, pred
            if pred is not None and pred not in ui_explanations:
                ui_explanations.append(pred)
        
        return "<br/>".join(ui_explanations)

    def __convert_predicate(self, model_difference):
        pred = ""
        act = ""
        s = ""
        # ppe can be about action precondition, add or delete effects
        if "has-preconditon" in model_difference:
            s = "-has-preconditon-"
            kind = "requires"
        elif "has-neg-preconditon" in model_difference:
            # negative preconditions are for book keeping so killing it right here
            return None
        elif "add" in model_difference:
            s = "-has-add-effect-"
            kind = "adds"
        elif "delete" in model_difference:
            s = "-has-delete-effect-"
            kind = "deletes"

        # spliting the string to get the action and predicate
        act, pred = model_difference.split(s)
        pred = pred.strip()
        act = act.strip()
        # removing the predicate parameters
        if "has_taken" in pred:
            # courses of thesis and deficiency type
            if "CSE599a" in pred:
                # checking for first thesis course to return that in feedback
                pred = "has_taken CSE599a"
            elif "CSE599b" in pred:
                # checking for second thesis course
                pred = "has_taken CSE599b"
            else:
                # these are usually deficiency course so key for that is has_taken
                pred = "has_taken"
        elif " " in pred:
            pred = pred.split(" ")[0]

        if "semester" in act:
            # added to remove extra number at the end of complete_semester action
            act = "complete_semester"

        # specialization has requirement of taking few extra courses.
        if "specialize" in act and pred == "has_taken":
            pred = "specialize-has_taken"

        # if either the action or predicate was missing sentences
        # then return empty action
        if pred not in self.predicates or act not in self.actions:
            return None

        print "[WAS FOUND]", model_difference, act
        return self.actions[act] + " " + kind + " " + self.predicates[pred]

