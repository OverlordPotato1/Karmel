import json

class async_dictionary():
    def __init__(self, file):
        self.file = file
        self.dictionary = loadJson(file)

    async def OTF_set(self, category: str, variable: str, value):
        self.dictionary[category][variable] = value

    async def OTF_get(self, category: str, variable: str):
        return self.dictionary[category][variable]
        


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

