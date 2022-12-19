import files
from wit import Wit

#set the wit access token
wit = Wit(files.loadJson("tokens.json")["wit"])

###########################################################################################################################################################################
# Message to Wit.ai and get response ##
#######################################

async def CAR(message, debug = False):
    response = wit.message(message.content)
    if debug:
        print(response)
    return response

###########################################################################################################################################################################
# Send prompt to Wit.ai without returning it's response ##
##########################################################

def analyseSinResponse(prompt):
    print("Sending "+prompt+" to Wit.ai")
    wit.message(prompt)
    return
