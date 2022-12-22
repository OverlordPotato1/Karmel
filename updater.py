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

async def updateChecker():
# get the current version
    with open("version.txt", "r") as version:
        currentVersion = version.read()

    # get the latest version
    latestVersion = requests.get("https://raw.githubusercontent.com/OverlordPotato1/Karmel/master/version.txt").text

    # if the current version is older than the latest version
    if currentVersion < latestVersion:
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