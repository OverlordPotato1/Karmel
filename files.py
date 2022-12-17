import json

class async_dictionary():
    def __init__(self, file):
        self.file = file
        self.dictionary = loadJson(file)

    async def set_dict(self, category: str, variable: str, value):
        if category not in self.dictionary:
            self.dictionary[category] = {}
        self.dictionary[category][variable] = value

    async def read_dict(self, category: str, variable: str):
        return self.dictionary[category][variable]

    async def checkExists_category(self, category: str):
        if category in self.dictionary:
            return True
        else:
            return False

    async def checkExists_variable(self, category: str, variable: str):
        if variable in self.dictionary[category]:
            return True
        else:
            return False
        


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

