import os
import shutil
import sys
import subprocess

"""
# Script Name: dirDiscovery
# Description: Script can gather some basic information from dir structure to show file types and path to each file of that type
# Author: CarterLankford
# Date: 9/25/24
#
# Usage: To use this script, simply run it with the following command: python [script_name].py [optional arguments].
# 
# Parameters: None
#
# Parameters: <arg1:Main Swtch(scan, test)>//<arg2:setup, copy, dump, testarg(get name for this)>//<arg3:>
# 
# Dev Notes:
# • Script will always create file dump in directory it's run from.
##TODO:Task-Update above with accurate info, just jotted some stuff down while the idea was fresh
##TODO:Task-Refresh code. This was written to get a job done quickly. Need to re-write to make it more efficent and correct. - Nothing is more perm then a temp solution.
"""

userInputArg1 = sys.argv[1]

#needs to have logs
#needs to functions for things done
#make it work then make it pretty 
#create env if not already there

def copy_files_to_directory(file_paths, destination_dir):
    """
    Copy files to a directory using their paths from a text file.
    
    Args:
    file_paths (list): List of file paths.
    destination_dir (str): Destination directory.
    
    Returns:
    None
    """
    for path in file_paths:
        # Check if the file exists
        if os.path.isfile(path):
            try:
                # Copy the file to the destination directory
                shutil.copy2(path, destination_dir)
                print(f"File {path} copied successfully.")
            except Exception as e:
                print(f"Error copying file {path}: {str(e)}")
        else:
            print(f"File {path} does not exist.")

def copy_File_To(fullFileName, payloadDir):
    if os.path.isfile(fullFileName):
        try:
            shutil.copy2(fullFileName, payloadDir)
            print(f"File {fullFileName} copied successfully.")
        except Exception as e:
            print(f"Error copying file {fullFileName}: {str(e)}")
    else:
        print(f"File {fullFileName} does not exist.")

def send_CMD_Mkdir(dirName):
    #from https://stackoverflow.com/questions/793858/how-to-mkdir-only-if-a-directory-does-not-already-exist
    #mkdir -p test/omg/yeah
    #input can match <send_CMD_Mkdir("test/ohyeah")>
    proc = subprocess.Popen(['mkdir', '-p', dirName], stdout=subprocess.PIPE)

def send_CMD_Get_All_File_Types():
    ##this will pull all files and paths and make the complete target list and the file extension list in the log dir
    ##find . -type f | while read filename; do echo $filename >> merp.txt; done 2>/dev/null
    
    proc = subprocess.Popen(['find', '.', '-type', 'f'], stdout=subprocess.PIPE)
    ##raw file path list
    ##file path and extenion for each potential target file  // could be sumerized as :complete list path/target/ext :completeTargetList
    ##completeTargetList
    ##fileextentionlist//alluniquefileextlist
    ##drop these in payload/log
    payloadLogPath = "payload/log/"
    j = "{0}{1}".format(payloadLogPath,"completeTargetList.txt")
    g = "{0}{1}".format(payloadLogPath,"fileExtensionList.txt")

    with open(j, 'w') as f:
        for root, dirs, files in os.walk('.'):
            for file in files:
                filename = os.path.join(root, file)
                f.write(filename + '\n')
    # Open the file (replace 'file.txt' with your actual filename)
    with open(j, 'r') as f:
        # Read each line and get its extension
        extensions = set()
        for line in f.readlines():
            _, ext = os.path.splitext(line.strip())
            # Add the unique extension to the set
            extensions.add(ext)

    with open(g, 'w') as f:
        for i in extensions:
            f.write(i + '\n')

def updateLog(pathToLog, message, time):
    print("ya fools")

###############################
## Env createion and cleanup ##
###############################
def setup_Env():
    send_CMD_Mkdir("payload/log/output")

def clean_Env():
    proc1 = subprocess.Popen(['rm', '-rf', 'payload/log/output'], stdout=subprocess.PIPE)

def purge_Env():
    proc1 = subprocess.Popen(['rm', '-rf', 'payload/'], stdout=subprocess.PIPE)

##Reused code turned into functions
def generate_Target_File_List(targetFilePath, targetFile):
    target = targetFilePath+targetFile
    payload = []
    #with open('payload/log/completeTargetList.txt', 'r') as f:
    with open(target, 'r') as f:
        payload = [line.strip() for line in f.readlines()]
    return payload

def generate_File_Type_List(targetFilePath, targetFile):
    target = targetFilePath+targetFile
    payload = []
    with open(target, 'r') as f:
        payload = [line.strip() for line in f.readlines()]
    return payload

def copy_File_Type(fullFileList, fileType, outputDir):

    #payloadDir = "payload/log/output/"
    #targetFileType=".jpg"
    for i in fullFileList:
        if fileType in i: #test this idea out
            #print(i)
            #update the log
            copy_File_To(i,outputDir)

    
def main():
    ##notes on structure
    ##no arg = all files copied and sorted into file type specific folders//<get file type list> //<copy all of spcific file type to default location> or provide other location//<test>//<env create/destroy>//
    ## generate list, or copy specific file type
    ##tell user how to use this damn thing without having to read the code you ass. print out to line and log.
    ##when getting file type list. need to pull from text file and order it correctly
    if userInputArg1 == "test":
        ftl = generate_File_Type_List("payload/log/", "fileExtensionList.txt")
        #print(ftl[20])
    elif userInputArg1 == "clean":
        clean_Env()
    elif userInputArg1 == "setup":
        setup_Env()
    elif userInputArg1 == "purge_Env":
        purge_Env()
    elif userInputArg1 == "no":
        #ebreak - mainly here as a reminder to build something better
        exit
    elif userInputArg1 == "getTypeList":
        send_CMD_Get_All_File_Types()
        fileExtensionList = generate_File_Type_List("payload/log/", "fileExtensionList.txt")
        for i in fileExtensionList:
            print(i)
    elif userInputArg1 == "type":
        #python3 dirDiscovery.py type .mp3 & python3 dirDiscovery.py type .mp4 ##Need to find a way to do this from an input list
        userInputArg2 = sys.argv[2]
        setup_Env()
        send_CMD_Get_All_File_Types()
        fileExtensionList = generate_File_Type_List("payload/log/", "fileExtensionList.txt")
        fullFileList = generate_Target_File_List("payload/log/", "completeTargetList.txt")
        #copy_File_Type(fullFileList, ".jpg", "payload/log/")
        copy_File_Type(fullFileList, userInputArg2, "payload/log/output")
        """
        payloadDir = "payload/log/output/"
        targetFileType=".jpg"

        for i in fullFileList:
            if ".jpg" in i: #test this idea out
                print(i)
                #update the log
                copy_File_To(i,payloadDir)
        """
                
        
    else:
        # Specify the source text file containing file paths
        #source_file_path = "test.txt"
        
        # Specify the destination directory
        #destination_dir = "/home/gretiem/codetest/payload"
        
        try:
            #this is what the process will look like in prime time/main and do a full copy/sort ////another version will be needed for targeted file types
            send_CMD_Get_All_File_Types()
            fileExtensionList = generate_File_Type_List("payload/log/", "fileExtensionList.txt")
            fullFileList = generate_Target_File_List("payload/log/", "completeTargetList.txt")
            payloadDir = "payload/log/output/"
            #targetfile = "payload/log/fileExtensionList.txt"
            #copy_File_To(targetfile, payloadDir)
            highestlen = 3
            for i in fullFileList:
                if ".jpeg" not in i: #test this idea out
                    print ("merp")
                ft = i.split('.')
                #print(ft)
                if len(ft) > 3:
                    #print(len(ft))
                    if len(ft) > highestlen:
                        highestlen = len(ft)
                        print(highestlen)
            print(highestlen)
            #print(len(ft))
            """
            if i == targetFileType:   #add the function here to strip the name of the file type after that copyt the matches 
                #copy that file to the dirs
                print("merp")
            else:
                print("derp")
            copy_File_To(i,payloadDir)
            """
        except Exception as e:
            print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
    
    
"""
 find . -type f | while read filename; do echo $filename > test1.txt; done 2>/dev/null

##gets every file##
find . -type f | while read filename; do echo $filename; done 2>/dev/null

##gets every file and logs to file##
find . -type f | while read filename; do echo $filename >> merp.txt; done 2>/dev/null

##gets what I want
find target/ -type f -name "*.jpg" > test.txt

Need to get files jpg, jpeg_
"""


"""
Goals and planning

Python <target path> <file type(str)>

create dir for x if !exist: 
Payload
payload/log
payload/log/target
payload/output

os command to pull all path/files into array
sort algorithym to put each unique file/path type in own array 

for each file type array
    update log for each file type with current values appened
    make dir for each file type

log to unique file -- create an entry in the log file for each file/path to show result 
update log with summary of findings (44jpeg found on 4/4/2012 total file size etc)

copy the deseried arrays file paths to the payload/output folder

add a sys arg at the begining of the code to allow a clean mode/help/test



make a master list
make lists for each file type
log them to csv
name file<1> etc and have the first value be the file type



pull file list types
<main part>
if arg 1 is file type ignore most of loop and only get that file type

using a for each could copy one path to one destination path which can be accepted by a definition to handle each copy processes ##Idea: can that be threaded and if so should it?
</main part>
get list of all file paths of that type
copy all of those files to another directory

if they have the same name, rename one. like maybe even add a number betweeen the last char and the . 
compare path count with number of files in payload dir






        #from https://github.com/Gretiem/Projects/blob/master/dev/wv1-pingscript.py
        #host = str(input('IP: '))
        #p1 = subprocess.Popen(['ping', '-c 2', host], stdout=subprocess.PIPE)
        #output = p1.communicate()[0]
        #print(output.decode('utf-8'))

"""

