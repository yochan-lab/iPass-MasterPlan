import json

class Interface:
    def __init__(self, connector = "_"):
        path = "problem_generator/config"
        self.courses = self.get_data(path + "courses.json")
        self.professors = self.get_data(path + "committee.json")
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
            "Thesis Credit A": "TAKE_CSE599A",
            "Thesis Credit B": "TAKE_CSE599B"
        }



    def getData(self, file_name):
        with open(file_name, 'r') as f:
            data = json.load(f)

        return data

    def uiToAction(self, ui_actions):
        self.course_counter = 0
        self.sem_counter = 0
        self.committee_counter = 1
        actions = []
        for action in ui_actions['plan']:
            if action['name'].find("-"):
                act = action['name'].split("-")
                act = [x.strip() for x in act]
            else:
                act = [action['name'].strip(), None]    
            actions.push(self.__converter(act[0], act[1]))

        return actions

    def __converter(self, action, name):
        switch = {
            "Add Course": __addCourse,
            "Add Chair": __addChair,
            "Add Committee": __addCommittee
            "Complete Semester": __endSemester
        }

        func = switcher.get(action, __default)
        return func(action, name)

    def __addChair(self, action, name):
        name = name.upper()
        action = self.mapper[action] + self.connector + name
        self.committee_members = [name] + self.committee_members

    def __addCommittee(self, action, name):
        if self.committee_counter < 3:
            self.committee_counter += 1
        name = name.upper()
        action =    self.mapper[action] + self.connector + self.num[self.committee_counter] +
                    self.connector + name
        self.committee_membners.append(name)
        return action

    def __endSemester(self, action, name):
        action = self.mapper[action] + self.connector + self.sem_counter
        self.sem_counter = 0
        return action

    def __default(self, action, name):
        return self.mapper[action] + self.connector + name.upper()

    def __addCourse(self, action, name):
        if name in self.cache:
            action =    self.mapper[self.cache[name][1]] + self.connector +
                        self.cache[name][0] + self.connector
        else:
            if name.find("Thesis"):
                action =    self.mapper[name] + self.connector
            else:
                course, courseType = self.__getAction(name)
                if course is None:
                    print "Course not found"
                    return None
                self.cache[name] = [course, courseType]
                action =    self.mapper[courseType] + self.connector + self.course + self.connector

        action +=   self.num[self.course_counter] + self.connector +
                    self.num[self.course_counter + 1] + self.connector + 
                    self.num[self.sem_counter] + self.connector +
                    self.num[self.sem_counter + 1]

        self.course_counter += 1
        self.sem_counter += 1

        return action


    def __getAction(self, name):
        for key in self.courses.keys():
            if self.courses[key][0] == name:
                return key, self.courses[key][1]
        
        return None, None
