import json

class dictionary():
    def __init__(self, file):
        self.file = file
        self.dictionary = loadJson(file)

    async def write(self, category: str, variable: str, newValue):
        '''
        Sets the value of category, variable
        
        Args:
            Category: its pretty self explantory
            Variable: its whats under the category
            newValue: if you need an explanation you shouldn't be coding
        
        
        '''

        self.dictionary[category][variable] = newValue

    async def get(self, category: str, variable: str):
        '''
        Gets the data at category, variable
        
        Args:
            Category: the category of the variable
            Variable: the variable
            
        Returns:
            The data at the variable
            
        Excepts:
            None
        '''
        return self.dictionary[category][variable]
    
    async def wipe(self, category: str, variable: str):
        '''
        Sets the data at category, variable to ""
        
        Args:
            Category: the category of the variable
            Variable: the variable

        Returns:
            Boolean: did the command suceed
        '''
        try:
            self.dictionary[category][variable] = ""
            return True
        except:
            return False
    
    async def checkBool(self, category: str, variable: str):
        '''
        Checks if the value of a variable is value that can be converted to a binary value
        
        Args:
            Category: the category of the variable
            Variable: the variable
            
        Returns:
            Boolean: the binary value of the variable
        '''
        trueList = ["yes", "true", "on", "valid", "correct"]
        falseList = ["no", "false", "off", "invalid", "incorrect"]
        if (self.dictionary[category][variable].lower in trueList):
            return True
        if (self.dictionary[category][variable].lower in falseList):
            return False
        else:
            raise ValueError("\"{}\" is not a known boolean value".format(self.dictionary[category][variable]))
        
    async def doesExist(self, category: str, variable: str):
        '''
        Checks if the variable is in memory
        
        Args:
            Category: the category of the variable
            Variable: the variable
            
        Returns:
            Boolean: whether the variable exists or not
        '''

        try:
            temp = self.dictionary[category][variable]
            del temp
            return True
        except:
            print("Failed to get variable")
            return False
        
    async def load(self):
        self.dictionary = loadJson(self.file)

    async def save(self):
        saveJson(self.file, self.dictionary)
        


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

sharedMemory = dictionary("memory.json")