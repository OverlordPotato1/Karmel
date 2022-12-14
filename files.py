import json

def loadJson(filename):
    print("Reading from " + filename)
    with open(filename) as f:
            memory = f.read()
    f.close()
    memory = json.loads(memory)
    return memory

def saveJson(filename, data):
    print("Writing to " + filename)
    with open(filename, 'w') as f:
        json.dump(data, f)
    f.close()