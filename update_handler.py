import git
import time
import os
import sys

branch = "preview"
time.sleep(0.25)
# get the parent of the current directory
parentDir = os.path.dirname(os.getcwd())
# get the current directory
currentDir = os.getcwd()
# using gitpython set the branch from branch and pull the latest version into the parent directory
# os.chdir(parentDir)
repo = git.Repo(currentDir)
# set the repo to pull from
repo.git.pull()
# wait 1 second
time.sleep(0.25)

os.chdir(currentDir)
# stop the current process and execute bot.py
os.execv(sys.executable, ['python bot.py'])