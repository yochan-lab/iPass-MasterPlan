from os import listdir
from os.path import join, getmtime
import time, json, sys
import pandas as pd


class Parser:
    def __init__(self):
        # nothing to do here for now
        # self.specialization_ai = ["CSE571", "CSE574", "CSE575"]
        # self.specialization_bd = ["CSE510", "CSE512", "CSE572"]
        # self.specialization_cs = ["CSE543", "CSE545", "CSE548"]
        self.dummy = None

    '''
    ' function to parse all the log data and write it to a csv
    '''
    def parse(self, folderName):
        times, files = self.__get_files(folderName)
        data = self.__get_data(files, times)
        data_copy = data.copy()
        for index, row in data_copy.iterrows():
            data["completion_ratio"] = self.__parse_ipos(row["final-IPOS"])

        with open("logs_data.csv", "w+") as f:
            data.to_csv(f, sep="\t", encoding="utf-8", index = False)


    '''
    ' get all the log file names and their last modified
    ' times from <folderName>\logs folder, in two lists
    '''
    def __get_files(self, folderName):
        # append logs to the folder parent folder
        folder = join(folderName, "logs")
        # get all files in the folder
        files = [join(folder, x) for x in listdir(folder)]
        # get last modified time of each file
        times = [time.strftime('%m-%d-%Y %H:%M:%S', time.gmtime(getmtime(x))) for x in files]
        return times, files

    '''
    ' get list of json objects for all the files
    '''
    def __get_data(self, files, times):
        objs = pd.DataFrame
        for count, f in enumerate(files):
            # read the file and put it in list of objects
            with open(f, 'r') as data_file:
                # read data as dictionary and then to a dataframe
                print f
                d = pd.DataFrame.from_dict(json.load(data_file), orient = "index").T
                # add corresponding time to the file
                d["edit_time"] = times[count]
                if objs.empty:
                    objs = d
                else:
                    # merge data with the previous dataset
                    objs = pd.concat([objs, d])

        objs = objs.sort_value("edit_time")
        return objs
    '''
    ' returns the ratio of actions completed to actual valid plan length of 21
    '''
    def __parse_ipos(self, ipos):
        return min(1, len(ipos)/21)

    '''
    The idea is dropped
    ' parses ipos which is in the form of actions to define
    ' whether all deficiencies were taken - 0, 1 value
    ' ten courses were completed - -1 (less than 10), 0 (10), 1(greater than 10)
    ' thesis A was added - 0, 1 value
    ' thesis B was added - 0, 1 value
    ' defense was added - 0, 1 value
    ' foundation, application, system were completed - 0, 1 value
    ' were there three specialization courses - 0, 1 value
    ' specialization was completed - 0, 1 value
    ' is the plan valid and correct - 0, 1 value
    def __parse_ipos(self, data, index):
        status = {
            "deficiency": False,
            "ten_course": False,
            "thesis_A": False,
            "thesis_B": False,
            "defense": False,
            "concentration": False,
            "specialization_courses": False,
            "specialization": False,
            "plan_valid": False
        }

        ui_action = {
            "name": "",
            "x": 0,
            "y": 0,
            "width": 12,
            "height": 1
        }

        plan = data[index]["final-IPOS"]
        fomatted_plan = []
        for count, action in enumerate(plan):
            temp = ui_action.copy()
            temp["y"] = count
            temp["name"] = action
            formatted_plan.append(temp)

        is_plan_complete =
    '''

if __name__ == "__main__":
    p = Parser()
    p.parse(sys.argv[1])
