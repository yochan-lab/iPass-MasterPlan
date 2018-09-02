import json

class Interface:
    def __init__(self, connector = "_"):
        path = "problem_generator/config/"
        self.courses = self.getData(path + "courses.json")
        self.committee = self.getData(path + "committee.json")
        self.cache = dict()
        self.connector = connector
        self.num = ["ZERO", "ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE", "TEN"]
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
            "Specialize": "SPECIALIZE"
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

    def getData(self, file_name):
        with open(file_name, 'r') as f:
            data = json.load(f)

        return data

    def actionsToUI(self, actions):
        ui_actions = []
        temp = []
        isFeedbackNeeded = False
        for action in actions:
            if action.find(";") >= 0:
                temp = action.split(";")
                isFeedbackNeeded = True
                action = temp[0]

            action = action[1: -1]
            if action.find("_") >= 0:
                actionArray = action.split("_")
            else:
                actionArray = [action]

            ui_action = str(self.__invertor(actionArray))
            if ui_action is not None:
                if isFeedbackNeeded:
                    ui_action += ";" + self.__getFeedback(temp[1])

                print ui_action
                ui_actions.append(ui_action)

        return ui_actions

    def uiToActions(self, ui_actions):
        # Initializing global variables everytime request comes from the frontend
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

        return actions

    def __get_action_name(self, action_name):
        if action_name.find("-"):
            act = action_name.split("-")
            act = [x.strip() for x in act]
        print(act)
        actionType = act[0]
        if act[0] == "Add":
            if act[1].find("Semester") > -1:
                actionType = "Complete Semester"
            else:
                actionType = "Defend"
              
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
            "Speicalize": self.__specialization
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

        if action == "Add Chair":
            act += self.connector + specialization.upper()
        return [act]

    '''
    ' where ever _ is used instead of the connector - it is because whatever the next
    ' string is, it is a part of the action and not a parameter to the action
    '''
    def __specialization(self, action, name):
        name = name if name.fine(" ") < 0 else name.replace(" ", "_")
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
            action =    self.mapper[self.cache[name][1]] + self.connector +\
                        self.cache[name][0] + self.connector
        else:
            if name.find("Thesis") > -1:
                name = self.__removeType(name)
                action =    self.mapper[name] + self.connector
                courseType = "research"
            else:
                course, courseType = self.__find(self.courses, name)
                if course is None:
                    return None
                self.cache[name] = [course, courseType]
                temp = "deficiency" if courseType == "deficiency" else "normal"
                action =        self.mapper[temp] + self.connector + course.upper() + self.connector

                if temp == "normal":
                    action +=   courseType.upper() + self.connector

            incremented     = self.course_counter + 1 if self.course_counter < 10 else 10
            sem_incremented = self.sem_counter + 1 if self.sem_counter < 10 else 10

            action +=           self.num[self.course_counter] + self.connector +\
                                self.num[incremented] + self.connector +\
                                self.num[self.sem_counter] + self.connector +\
                                self.num[sem_incremented]

        if courseType != "deficiency": self.course_counter += 1
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

        return self.invert_mapper[self.actionStrings[0]] + specialization

    def __invertCommittee(self, actionStrings):
        key = "_".join(actionStrings[0:3])
        profName = actionStrings[3].title()
        prof = self.committee[profName]
        action = self.invert_mapper[key] + prof[0] + " (specialization:" + prof[1] + ")"
        return action

    def __invertCourse(self, actionStrings):
        key = "_".join(actionStrings[0:2])
        print key
        if actionStrings[1].find("CSE") >= 0:
            action = self.invert_mapper[key]
        else:
            course = self.courses[actionStrings[3]]
            action = self.invert_mapper[key] + course[0] + " (" + course[1] + ")"

        return action


    def __defaultInvertor(self, actions):
        return self.invert_mapper[actions[0]]

    def __getFeedback(self, soup):
        return "TODO: feedback -- actual string " + soup

def test_invertor():
    plan = [
        "(SELECT_COMMITTEE_CHAIR_ZHANG_AI)",
        "(TAKE_DEFICIENCY_COURSE_CSE340_ZERO_ONE_ZERO_ONE)",
        "(DEFEND);(defend) has an unsatisfied precondition at time 1 : (Follow each of: :     (Set (current_num_ten) to true) :     and (Set (has_taken_cse599b) to true) :     and (Set (has_taken_cse599a) to true) :     and (Set (completed_specialization) to true) :     and (Set (has_committee_member3) to true) :     and (Set (has_committee_member2) to true) :     and (Set (has_committee_done) to true) :     and (Set (has_committee_chair_done) to true) : )"
    ]
    inter = Interface()
    print inter.actionsToUI(plan)

def test():
    plan =  [
                {"name": "Add - End of Semester", "x": 0, "y": 1, "width": 12, "height": 1},
                {"name":"Add Course - Embedded Operating Systems Internals (systems)",
                        "x": 0, "y": 0, "width": 12, "height": 1},
                {"name": "Add Course - Software Project, Process and Quality Management (systems)",
                        "x": 0, "y": 0, "width": 12, "height": 1},
                {"name": "Add Course - Computer Organization and Assembly Language Programming (deficiency)",
                        "x": 0, "y": 0, "width": 12, "height": 1},
                {"name": "Add - End of Semester", "x": 0, "y": 1, "width": 12, "height": 1},
                {"name": "Add Course - Software Verification, Validation and Testing (systems)",
                        "x": 0, "y": 2, "width": 12, "height": 1},
                {"name": "Add Committee - Guoliang Xue (Specialization: big data)",
                        "x": 0, "y": 3, "width": 12, "height": 1},
                {"name": "Add - End of Semester", "x": 0, "y": 4, "width": 12, "height": 1},
                {"name": "Add Chair - Arunabha Sen (Specialization: none)",
                        "x": 0, "y": 5, "width": 12, "height": 1},
                {"name": "Add Course - Thesis Course A (research)", "x": 0, "y": 4, "width": 12, "height": 1},
                {"name": "Add - Defense", "x": 0, "y": 6, "width": 12, "height": 1}
            ]

    inter = Interface(" ")
    print inter.uiToActions(plan)

if __name__ == "__main__":
    #test()
    test_invertor()
