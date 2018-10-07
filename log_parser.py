from os import listdir
from os.path import join, getmtime
import time, json, sys
import pandas as pd


class Parser:
    def __init__(self):
        # nothing to do here for now
        self.dummy = None

    '''
    ' function to parse all the log data and write it to a csv
    '''
    def parse(self, folderName):
        times, files = self.__get_files(folderName)
        data = self.__get_data(files, times)
        with open("logs_data.csv", "w+") as f:
            data.to_csv(f, sep="\t", encoding="utf-8", index = False)
        #for index, row in data.iterrows():
            #parse

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

        return objs

if __name__ == "__main__":
    p = Parser()
    p.parse(sys.argv[1])
