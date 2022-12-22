import git
import time
import os
import sys
import variables
import misc_functions as misc
import datetime
import traceback

time.sleep(0.25)
# get the parent of the current directory
parentDir = os.path.dirname(os.getcwd())
# get the current directory
currentDir = os.getcwd()
# using gitpython set the branch from branch and pull the latest version into the parent directory
repo = git.Repo(currentDir)
repo.git.checkout(variables.config.get("branch"))
repo.remotes.origin.pull()
misc.logWarn("Pulled latest version from GitHub.")
misc.logWarn("Killing process and running bot.py")
now = datetime.datetime.now()
# format the time to contain the date and time
currtime = now.strftime("%d/%m/%Y %H:%M")
variables.config.set("last_update (DO NOT EDIT)", currtime)
# wait 1 second
time.sleep(2)

# stop the current process and execute bot.py
os.execv(sys.executable, ['python bot.py'])