# pull version.txt from github
# compare version.txt to local version.txt
# if version.txt is newer, download the new version
# if version.txt is older, do nothing
# if version.txt is the same, do nothing

import os
import requests
import shutil
import zipfile
import sys
import time
import asyncio
import misc_functions

branch = "preview"


async def updateChecker():
    # get the parent of the current directory
    parentDir = os.path.dirname(os.getcwd())
    # get the current directory
    currentDir = os.getcwd()
# get the current version
    try:
        with open("version.txt", "r") as version:
            currentVersion = version.read()
    except:
        misc_functions.logWarn("Failed to get version.txt from local directory.  Retrying in 4 minutes.")
        time.sleep(60*4)
        asyncio.run(updateChecker())

    # get the latest version
    try:
        latestVersion = requests.get("https://raw.githubusercontent.com/OverlordPotato1/Karmel/"+branch+"/version.txt").text
    except:
        misc_functions.logWarn("Failed to get version.txt from GitHub.  Retrying in 4 minutes.")
        time.sleep(60*4)
        asyncio.run(updateChecker())

    # split the version numbers into a list
    currentVersion = currentVersion.split(" ")
    latestVersion = latestVersion.split(" ")

    if len(currentVersion) > 1:
        currIsPreview = True
    if len(latestVersion) > 1:
        downloadIsPreview = True
        misc_functions.logWarn("On preview branch. Bugs will ocur.")

    currentVersion[0] = float(currentVersion[0])
    latestVersion[0] = float(latestVersion[0])
    currentVersion[2] = int(currentVersion[2])
    latestVersion[2] = int(latestVersion[2])

    misc_functions.logWarn("Current version: " + str(currentVersion))
    misc_functions.logWarn("Latest version: " + str(latestVersion))
    if currIsPreview:
        misc_functions.logWarn("Current version is a preview version.")
        misc_functions.logWarn("Preview version: "+str(currentVersion[2]))
    if downloadIsPreview:
        misc_functions.logWarn("Latest version is a preview version.")
        misc_functions.logWarn("Preview version: "+str(latestVersion[2]))
    

    # if the current version is older than the latest version
    if currentVersion[0] < latestVersion[0]:
        # download the new version into the parent folder
        r = requests.get("https://raw.githubusercontent.com/OverlordPotato1/Karmel/"+branch, stream=True)
        # download zip in parentDir
        with open(parentDir+"/Karmel.zip", "wb") as f:
            shutil.copyfileobj(r.raw, f)    
        # unzip the new version into the parent folder
        with zipfile.ZipFile(parentDir+"/Karmel.zip", "r") as zip_ref:
            # replace the old files in the current directory with the new files
            zip_ref.extractall(currentDir)
        # delete the zip file
        os.remove(parentDir+"/Karmel.zip")
        # delete the old version
        os.remove("version.txt")    
        # rename the new version
        os.rename(currentDir+"/Karmel-master/version.txt", "version.txt")
        # delete the old files
        shutil.rmtree(currentDir+"/Karmel-master")
        # restart the bot
        os.execv(sys.executable, ['python'] + sys.argv)

    elif currIsPreview and not downloadIsPreview:
        # download the new version into the parent folder
        r = requests.get("https://raw.githubusercontent.com/OverlordPotato1/Karmel/"+branch, stream=True)
        # download zip in parentDir
        with open(parentDir+"/Karmel.zip", "wb") as f:
            shutil.copyfileobj(r.raw, f)    
        # unzip the new version into the parent folder
        with zipfile.ZipFile(parentDir+"/Karmel.zip", "r") as zip_ref:
            # replace the old files in the current directory with the new files
            zip_ref.extractall(currentDir)
        # delete the zip file
        os.remove(parentDir+"/Karmel.zip")
        # delete the old version
        os.remove("version.txt")    
        # rename the new version
        os.rename(currentDir+"/Karmel-master/version.txt", "version.txt")
        # delete the old files
        shutil.rmtree(currentDir+"/Karmel-master")
        # restart the bot
        os.execv(sys.executable, ['python'] + sys.argv)
    if currIsPreview and downloadIsPreview:
        # compare the preview versions
        if currentVersion[2] < latestVersion[2]:
            # download the new version into the parent folder
            r = requests.get("https://raw.githubusercontent.com/OverlordPotato1/Karmel/"+branch, stream=True)
            # download zip in parentDir
            with open(parentDir+"/Karmel.zip", "wb") as f:
                shutil.copyfileobj(r.raw, f)    
            # unzip the new version into the parent folder
            with zipfile.ZipFile(parentDir+"/Karmel.zip", "r") as zip_ref:
                # replace the old files in the current directory with the new files
                zip_ref.extractall(currentDir)
            # delete the zip file
            os.remove(parentDir+"/Karmel.zip")
            # delete the old version
            os.remove("version.txt")    
            # rename the new version
            os.rename(currentDir+"/Karmel-master/version.txt", "version.txt")
            # delete the old files
            shutil.rmtree(currentDir+"/Karmel-master")
            # restart the bot
            os.execv(sys.executable, ['python'] + sys.argv)
        else:
            print("No update available")
            time.sleep(60*4)
            asyncio.run(updateChecker())
    else:
        print("No update available")
        time.sleep(60*4)
        asyncio.run(updateChecker())

asyncio.run(updateChecker())