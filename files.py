import inspect
import json
from misc_functions import *
import os

# open config.txt
class config():
    def __init__(self, file):
        self.file = file
        # if the file does not exist, create it
        if not os.path.isfile(file) or os.stat(file).st_size == 0:
            with open(file, "w") as config:
                # write the default config from default_config_DO_NOT_EDIT.config
                with open("default_config_DO_NOT_EDIT.config", "r") as default_config:
                    default_config = default_config.read()
                config.write(default_config)
        # open the file                
        with open(file, "r") as config:
            config = config.read()
        # split config.txt into a list
        config = config.split("\n")
        # convert the list into a dictionary
        self.config = dict([x.split(": ") for x in config])

    def __write(self):
        # convert dictionary into a list with each item being a different line
        config = [key + ": " + value for key, value in self.config.items()]
        # convert the list into a string
        config = "\n".join(config)
        # write the new config to config.txt
        with open(self.file, "w") as configfile:
            configfile.write(config)

    def get(self, key):
        return self.config[key]

    def set(self, key, value):
        self.config[key] = value
        # write the new config to config.txt
        self.__write()

class async_dictionary():
    def __init__(self, file):
        self.file = file
        self.dictionary = loadJson(file)

    async def set_dict(self, category: str, variable: str, value):
        if type(category) != str:
            category = str(category)
        if type(variable) != str:
            variable = str(variable)
        if category not in self.dictionary:
            logWarn("Category ("+category+") not found in dictionary. Creating category.")
            self.dictionary[category] = {}
        self.dictionary[category][variable] = value

    async def read_dict(self, category = None, variable = None, defOnFail = None, convBinary = False):
        if category == None:
            return self.dictionary
        if variable == None:
            return self.dictionary[category]
        # raise exception if category or variable are not a string
        line = inspect.currentframe().f_back.f_lineno
        prevFile = inspect.currentframe().f_back.f_code.co_filename
        if type(category) != str:
            category = str(category)
        if type(variable) != str:
            variable = str(variable)
        try:
            value = self.dictionary[category][variable]
        except:
            if defOnFail != None:
                self.dictionary[category][variable] = defOnFail
                logWarn("An unknown error occured during read of variable ("+variable+") in category ("+category+"). A fallback value was provided, program continued.")
                # raise KeyError("An unknown error occured during read of variable ("+variable+") in category ("+category+"). A fallback value was provided, program will continue.")
            else:
                # logError("read_dict failed to find variable ("+variable+") in category ("+category+") and no fallback definition was provided. Line "+str(line)+" in file "+prevFile+".")
                raise KeyError("read_dict failed to find variable ("+variable+") in category ("+category+") and no fallback definition was provided. Line "+str(line)+" in file "+prevFile+".")
        trueVals = ["true", "t", "yes", "y", "1", "yes", "on", "enable", "enabled", "active", "activated"]
        falseVals = ["false", "f", "no", "n", "0", "no", "off", "disable", "disabled", "inactive", "deactivated"]
        if convBinary:
            if value.lower() in trueVals:
                return True
            elif value.lower() in falseVals:
                return False
            else:
                raise TypeError("read_dict failed to convert binary value ("+value+") to boolean. Recieved value is not a known valid binary value: "+value)
        else:
            return value


    async def checkExists_category(self, category: str):
        if type(category) != str:
            category = str(category)
        try:
            test = self.dictionary[category]
            return True
        except:
            return False


    async def checkExists_variable(self, category: str, variable: str):
        if type(category) != str:
            category = str(category)
        if type(variable) != str:
            variable = str(variable)
        try:
            test = self.dictionary[category][variable]
            return True
        except:
            return False


    async def save(self):
        saveJson(self.file, self.dictionary)


    async def reload(self):
        self.dictionary = loadJson(self.file)
        # for when im to lazy to find and replace the parts that just read directly from the file and save to it

    async def add_dict(self, category: str, variable: str, value):
        if category not in self.dictionary:
            self.dictionary[category] = {}
        self.dictionary[category][variable] += value
        


def loadJson(filename):
    try:
        print("Reading from " + filename)
        with open(filename) as f:
                memory = f.read()
        f.close()
        memory = json.loads(memory)
        return memory
    except:
        print("Error reading from " + filename)
        return {}


def saveJson(filename, data):
    try:
        print("Writing to " + filename)
        with open(filename, 'w') as f:
            json.dump(data, f)
        f.close()
    except:
        print("Error writing to " + filename)
        return {}

