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



    def getData(self, file_name):
        with open(file_name, 'r') as f:
            data = json.load(f)

        return data
        
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
                actions[action_pos+end_sem_count_booster] = action_list[i]

        return actions

    def __get_action_name(self, action_name):
        if action_name.find("-"):
            act = action_name.split("-")
            act = [x.strip() for x in act]

        actionType = act[0]
        if act[0] == "Add":
            if act[1].find("Semester") > -1:
                actionType = "Complete Semester"
            else:
                actionType = "Defend"
              
        return [str(x) for x in self.__converter(actionType, act[1])]

    def __converter(self, action, name):
        switch = {
            "Add Course": self.__addCourse,
            "Add Chair": self.__addChairAndCommittee,
            "Add Committee": self.__addChairAndCommittee,
            "Complete Semester": self.__endSemester,
            "Defend": self.__defend,
            "Speicalize": self.__specialization
        }

        func = switch.get(action, self.__default)
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
        if self.sem_counter < 5:
            actions.append(self.mapper[action] + "_" + str(self.sem_counter))

        self.sem_counter = 0
        actions.append(self.mapper[action])
        return actions

    def __defend(self, action, name):
        return [self.mapper[action]]

    def __default(self, action, name):
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

def test():
    plan =  [
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
    test()
