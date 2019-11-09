
sleepTime = 600                     # free space check requency in sec
safeLine = 0.1                      # free space limit in percent 
criticalLine = 0.05                 # free space limit in percent 
removeFoldersPath = ["/uslog"]      # files remove from this folders

import shutil
import sys
import time
import os

def diskSpace (path):
    usage=shutil.disk_usage(path)
    return usage.free/usage.total

def removeDirtyFolders (path):
	for subFolder in os.listdir (path):
		if diskSpace(path) < safeLine:
			fullPath=os.path.join (path, subFolder)
			shutil.rmtree(fullPath)
		else:
			return 0

if len(sys.argv) > 1:
	removeFoldersPath = sys.argv[:]
	removeFoldersPath.pop(0)

while (True):
	for folderPath in removeFoldersPath:
		if (os.path.exists(folderPath)):
			freeSpace=diskSpace(folderPath)
			if freeSpace < criticalLine:
				removeDirtyFolders(folderPath)
	time.sleep(sleepTime)