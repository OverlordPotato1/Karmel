import json

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