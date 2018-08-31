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
            "Complete Semester": "COMPLETE_SEM",
            "Add Chair": "SELECT_COMMITTEE_CHAIR",
            "Add Committee": "SELECT_COMMITTEE_MEMBER",
            "Defend": "DEFEND",
            "Complete Deficiency": "COMPLETE_DEFICIENCY",
            "Complete Foundations": "COMPLETE_FOUNDATIONS",
            "Complete Applications": "COMPLETE_APPLICATIONS",
            "Complete Systems": "COMPLETE_SYSTEMS",
            "Thesis Course A": "TAKE_CSE599A",
            "Thesis Course B": "TAKE_CSE599B"
        }



    def getData(self, file_name):
        with open(file_name, 'r') as f:
            data = json.load(f)

        return data

    def uiToActions(self, ui_actions):
        self.course_counter = 0
        self.sem_counter = 0
        self.committee_counter = 1
        self.committee_members = []
        actions = []
        for action in ui_actions:
            if action['name'].find("-"):
                act = action['name'].split("-")
                act = [x.strip() for x in act]

            actionType = act[0]
            if act[0] == "Add":
                if act[1].find("Semester") > -1:
                    actionType = "Complete Semester"
                else:
                    actionType = "Defend"
            actions.append(str(self.__converter(actionType, act[1])))

        return actions

    def __converter(self, action, name):
        switch = {
            "Add Course": self.__addCourse,
            "Add Chair": self.__addChairAndCommittee,
            "Add Committee": self.__addChairAndCommittee,
            "Complete Semester": self.__endSemester,
            "Defend": self.__defend,
        }

        func = switch.get(action, self.__default)
        return func(action, name)

    def __addChairAndCommittee(self, action, name):
        prof, _ = self.__find(self.committee, name)
        if prof is None:
            return None

        prof = prof.upper()
        action = self.mapper[action] + self.connector
        if action == "Add Committee":
            if self.committee_counter < 3:
                self.committee_counter += 1
            action += self.committee_counter + self.connector
            self.committee_members.append(prof)
        else:
            self.committee_members = [prof] + self.committee_members

        action += prof
        return action

    def __endSemester(self, action, name):
        action = self.mapper[action] + self.connector + str(self.sem_counter)
        self.sem_counter = 0
        return action

    def __defend(self, action, name):
        return self.mapper[action] + self.connector + self.connector.join(self.committee_members)

    def __default(self, action, name):
        return self.mapper[action] + self.connector + name.upper()

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
                if courseType == "deficiency":
                    action =    self.mapper["deficiency"] + self.connector + course.upper() + self.connector
                    action +=   self.num[10] + self.connector + self.num[10] + self.connector
                else:
                    action =    self.mapper["normal"]
                    action +=   self.connector + course.upper() + self.connector

            if courseType != "deficiency":
                action +=   self.num[self.course_counter] + self.connector +\
                            self.num[self.course_counter + 1] + self.connector
                self.course_counter += 1

            action +=       self.num[self.sem_counter] + self.connector +\
                            self.num[self.sem_counter + 1]

        self.sem_counter += 1

        return action


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
                {"name": "Add Committee - Guoliang Xue (foundations)",
                        "x": 0, "y": 3, "width": 12, "height": 1},
                {"name": "Add - End of Semester", "x": 0, "y": 4, "width": 12, "height": 1},
                {"name": "Add Chair - Arunabha Sen (foundations)",
                        "x": 0, "y": 5, "width": 12, "height": 1},
                {"name": "Add Course - Thesis Course A (research)", "x": 0, "y": 4, "width": 12, "height": 1},
                {"name": "Add - Defense", "x": 0, "y": 6, "width": 12, "height": 1}
            ]

    inter = Interface(" ")
    print inter.uiToActions(plan)

if __name__ == "__main__":
    test()
