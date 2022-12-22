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

async def updateChecker():
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
        latestVersion = requests.get("https://raw.githubusercontent.com/OverlordPotato1/Karmel/master/version.txt").text
    except:
        misc_functions.logWarn("Failed to get version.txt from GitHub.  Retrying in 4 minutes.")
        time.sleep(60*4)
        asyncio.run(updateChecker())

    # split the version numbers into a list
    currentVersion = currentVersion.split(" ")
    latestVersion = latestVersion.split(" ")
    # set currentVersion and latestVersion to doubles
    currentVersion = float(currentVersion[0])
    latestVersion = float(latestVersion[0])

    if len(currentVersion) > 1:
        currIsPreview = True
    if len(latestVersion) > 1:
        downloadIsPreview = True
        misc_functions.logWarn("On preview branch. Bugs will ocur.")

    # if the current version is older than the latest version
    if currentVersion[0] < latestVersion[0]:
        # download the latest version
        r = requests.get("https://raw.githubusercontent.com/OverlordPotato1/Karmel/master", stream=True)
        with open("Karmel.zip", "wb") as f:
            shutil.copyfileobj(r.raw, f)
        # unzip the latest version
        with zipfile.ZipFile("Karmel.zip", "r") as zip_ref:
            zip_ref.extractall()
        # delete the zip file
        os.remove("Karmel.zip")
        # delete the old version
        os.remove("version.txt")
        # rename the new version
        os.rename("Karmel-master/version.txt", "version.txt")
        # delete the old files
        shutil.rmtree("Karmel-master")
        # restart the bot
        os.execv(sys.executable, ['python'] + sys.argv)

    elif currIsPreview and not downloadIsPreview:
        # download the latest version
        r = requests.get("https://raw.githubusercontent.com/OverlordPotato1/Karmel/master", stream=True)
        with open("Karmel.zip", "wb") as f:
            shutil.copyfileobj(r.raw, f)
        # unzip the latest version
        with zipfile.ZipFile("Karmel.zip", "r") as zip_ref:
            zip_ref.extractall()
        # delete the zip file
        os.remove("Karmel.zip")
        # delete the old version
        os.remove("version.txt")
        # rename the new version
        os.rename("Karmel-master/version.txt", "version.txt")
        # delete the old files
        shutil.rmtree("Karmel-master")
        # restart the bot
        os.execv(sys.executable, ['python'] + sys.argv)
    elif currIsPreview and downloadIsPreview:
        # compare the preview versions
        if currentVersion[2] < latestVersion[2]:
            # download the latest version
            r = requests.get("https://raw.githubusercontent.com/OverlordPotato1/Karmel/master", stream=True)
            with open("Karmel.zip", "wb") as f:
                shutil.copyfileobj(r.raw, f)
            # unzip the latest version
            with zipfile.ZipFile("Karmel.zip", "r") as zip_ref:
                zip_ref.extractall()
            # delete the zip file
            os.remove("Karmel.zip")
            # delete the old version
            os.remove("version.txt")
            # rename the new version
            os.rename("Karmel-master/version.txt", "version.txt")
            # delete the old files
            shutil.rmtree("Karmel-master")
            # restart the bot
            os.execv(sys.executable, ['python'] + sys.argv)
    else:
        print("No update available")
        time.sleep(60*4)
        asyncio.run(updateChecker())

asyncio.run(updateChecker())