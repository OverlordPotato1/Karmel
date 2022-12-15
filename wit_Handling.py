import files
from wit import Wit

#set the wit access token
client = Wit(files.loadJson("tokens.json")["wit"])

###########################################################################################################################################################################
# Message to Wit.ai and get response ##
#######################################

async def CAR(message, debug = False):
    response = client.message(message.content)
    if debug:
        print(response)
    return response
