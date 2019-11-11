
import zipfile

archiveFoldersPath = ["/uslog"]      # files archive in this folders
archiveExtension = ".zip"            # extension for new archives
diffTimeInSec = 300
sleepTimeInSec = 300
compressType = zipfile.ZIP_LZMA

import sys
import time
import os

def getCTime (path):
	return time.ctime(os.path.getctime(path))

def getMTime (path):
	return os.path.getmtime(path)

if len(sys.argv) > 1:
	archiveFoldersPath = sys.argv[:]
	archiveFoldersPath.pop(0)
print("Start pylogrotate_archive")
reverseWalk=False
while True:
	allDirectories = []
	for folderPath in archiveFoldersPath:
		if (os.path.exists(folderPath)):
			for subFolder in os.listdir (folderPath):
				allDirectories.append(os.path.join(folderPath,subFolder))
	allDirectories.sort(key=getCTime,reverse=reverseWalk)
	for directory in allDirectories:
		nowTime = time.time ()
		checkDate = (nowTime-getMTime(directory)) < diffTimeInSec
		for folderName, subFolders, fileNames in os.walk (directory):
			for fileName in fileNames:
				if fileName.endswith(archiveExtension):
					continue
				fileFullPath = os.path.join(directory,fileName)
				readyForArchive = True
				if checkDate:
					readyForArchive = (nowTime-getMTime(fileFullPath)) > diffTimeInSec
				if readyForArchive:
					newZip = zipfile.ZipFile (fileFullPath + archiveExtension , 'w', compressType)
					newZip.write(fileFullPath,fileName)
					newZip.close()
					os.remove (fileFullPath)
	reverseWalk = True
	time.sleep(sleepTimeInSec)	