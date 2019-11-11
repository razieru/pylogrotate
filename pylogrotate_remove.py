
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

def getCTime (path):
	return time.ctime(os.path.getctime(path))

if len(sys.argv) > 1:
	removeFoldersPath = sys.argv[:]
	removeFoldersPath.pop(0)
print("Start pylogrotate_remove")
if len(removeFoldersPath) == 1:
	while (True):
		for folderPath in removeFoldersPath:
			if (os.path.exists(folderPath)):
				if diskSpace(folderPath) < criticalLine:
					for subFolder in os.listdir (folderPath):
						if diskSpace(folderPath) < safeLine:
							fullPath=os.path.join (folderPath, subFolder)
							if (os.path.exists(fullPath)):
								shutil.rmtree(fullPath)
						else:
							break
		time.sleep(sleepTime)
if len(removeFoldersPath) > 1:
	while (True):
		allDirectories = []
		for folderPath in removeFoldersPath:		
			if (os.path.exists(folderPath)):			
				if diskSpace(folderPath) < criticalLine:
					for subFolder in os.listdir (folderPath):
						allDirectories.append(os.path.join(folderPath,subFolder))
		allDirectories.sort(key=getCTime)
		for directory in allDirectories:
			if (os.path.exists(directory)):
				if diskSpace(directory) < safeLine:
					shutil.rmtree(directory)
		time.sleep(sleepTime)