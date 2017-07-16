#!/usr/bin/env python

import subprocess
import pexpect
import sys
import os
import shutil
import filecmp

from pexpect import *
from os import listdir
from os.path import isfile, join
from subprocess import Popen, PIPE

try:

    aux = str(sys.argv[1:])

    if (aux.find('-d') != -1): 

        DEBUG = True

    else:

        DEBUG = False

except Exception, e:

    DEBUG = False

#Define the project directory
CURRENT_DIR = ((os.getcwd()).replace("web", "compiler") + "/")

if(DEBUG): print ("[COMPILER] current dir:" + str(CURRENT_DIR))

def main():

    #Get the file to compile
    files = searchFilesToCompile()

    if files == [] or files == False: 

        if(DEBUG): print ("No files to compile was found at " + CURRENT_DIR)

        return (False)

    else:

        #Loop through each .c files to compile
        for item in files: 

            item = item.replace(CURRENT_DIR, '')

            if (DEBUG): print ("[COMPILER] item: " + str(item))

            global FILE_USER_IN, FILE_USER_COMPILED, FILE_USER_OUT, FILE_USER_IN_ORIGIN, FILE_USER_IN_JUDGED_DEST, FILE_USER_IN_NO_JUDGED_DEST, INPUT_DIR_EXERCISE_FILE, OUTPUT_DIR_EXERCISE_FILE, FILE_USER_ANSWER_OUT

            #Define the user code to run
            FILE_USER_IN = item

            #Define the user compiled code
            FILE_USER_COMPILED = item.split('.')[0] + ".tempuserout"

            #Define the user output file that will contain the results
            FILE_USER_OUT = CURRENT_DIR + "judged/" + item.split('.')[0] + ".judged"

            #Get the exercise number to take the corresponding files .exercisein and .exerciseout
            EXERCISE_NUMBER = item[:4]

            #Define the .in file to test with the user code 
            INPUT_DIR_EXERCISE_FILE = CURRENT_DIR + "inputs/" + EXERCISE_NUMBER + ".exercisein" 

            #Define the .out file to test with the user code output
            OUTPUT_DIR_EXERCISE_FILE = CURRENT_DIR + "outputs/" + EXERCISE_NUMBER + ".exerciseout" 

            #Define the .userout file containing the output from user code
            FILE_USER_ANSWER_OUT = CURRENT_DIR + "temp/" + FILE_USER_IN.split('.')[0] + ".userout" 

            FILE_USER_IN_ORIGIN = CURRENT_DIR + FILE_USER_IN
            FILE_USER_IN_JUDGED_DEST = CURRENT_DIR + "judged/" + FILE_USER_IN
            FILE_USER_IN_NO_JUDGED_DEST = CURRENT_DIR + "nojudged/" + FILE_USER_IN

            if(DEBUG): print ("Running the file " + FILE_USER_IN + ":----------------------------------------------------\n")

            #Calling module compileUserFile to check and compile the user code
            #if (compileUserFile(FILE_USER_IN, FILE_USER_COMPILED) == True): 
            if (compileUserFile(FILE_USER_IN_ORIGIN, FILE_USER_COMPILED) == True): 

                if(DEBUG): print("Compile the file " + str(FILE_USER_IN) + ": ok.\n")

            else:

                writeFinal("1", False)

                if(DEBUG): print("-------------------------------------\n")

                if(DEBUG): print ("Status 1: An error occurred in the file " + str(FILE_USER_IN) + ".\n")

                if(DEBUG): print("-------------------------------------\n")

                moveFiles("nojudged")

                continue;

            # Call the module testUserFile to test the output user code with our values in .in file, and later compare the user out with our .out file
            checkTestUser = testUserFile()

            if(checkTestUser == True):

                if(DEBUG): print("Test the file " +  str(FILE_USER_IN) + ": ok.\n")

            else:

                if(checkTestUser == "Status 3"):

                    if(DEBUG): print("-------------------------------------\n")

                    if(DEBUG): print ("Status 3: Timeout in the file " + str(FILE_USER_IN) + ".\n")

                    if(DEBUG): print("-------------------------------------\n")

                elif(checkTestUser == "Status 4"):

                    if(DEBUG): print("-------------------------------------\n")

                    if(DEBUG): print("Status 4: Presentation error in the file " + str(FILE_USER_IN) + ".\n")

                    if(DEBUG): print("-------------------------------------\n")                    

                moveFiles("nojudged")

                deleteFile(FILE_USER_COMPILED)  

                continue;

            #Check the difference between our expected output with the user code output
            checkCompareFiles = compareFiles(True)

            if(checkCompareFiles == "Status 2"): 

                moveFiles("nojudged")

                deleteFile(FILE_USER_COMPILED)

                if(DEBUG): print("-------------------------------------\n")

                if(DEBUG): print("Status 2: The user code output is not equal with our expected output.\n")

                if(DEBUG): print("-------------------------------------\n")

                continue;

            elif(checkCompareFiles == "Status 4"):

                moveFiles("nojudged")

                deleteFile(FILE_USER_COMPILED)

                if(DEBUG): print("-------------------------------------\n")

                if(DEBUG): print("Status 4: Presentation error in the file " + str(FILE_USER_IN) + ".\n")

                if(DEBUG): print("-------------------------------------\n")

                continue;

            moveFiles("judged")

            deleteFile(FILE_USER_COMPILED)
            
            if(DEBUG): print("-------------------------------------\n")

            if(DEBUG): print("Status 5: The file " + FILE_USER_IN + " was accepted succesfully.\n")

            if(DEBUG): print("-------------------------------------\n")

        return (True)


def searchFilesToCompile():

    try:

        files = []

        for arg in sys.argv:

            if(arg.find('.c') != -1): #Try to find .c files at command line parameters

                files.append(arg)

        if(files != []):

            if(DEBUG): print("Search files from command line: ok.\n")

        else:

            files = [f for f in listdir(CURRENT_DIR) if isfile(join(CURRENT_DIR, f)) if f.split('.')[1] == 'c']

        if(DEBUG): print("Search files to compile: ok.\n")

        return files

    except Exception, e:

        if(str(e) == 'list index out of range'): 

            for trashItem in f:

                # Move the file without extension to trash dir
                origin = CURRENT_DIR + trashItem

                dest = CURRENT_DIR + "trash/" + trashItem

                shutil.move(origin, dest)
            
            if(DEBUG): print("Problems when search the files to compile.------------------------------------------\n")

            return (False)

def compileUserFile(fileToCompile, fileCompiled):

    #Prepare the command to compile the user code, generating the FILEUSEROUT (c executable)
    compileFile = ["gcc", fileToCompile, "-o", fileCompiled]

    # Running the compileFile command
    process = subprocess.Popen(compileFile, shell=False, stdout=subprocess.PIPE)

    #Wait the end of process
    process.wait()

    # Get the output/errors from process
    process.communicate()[0]

    #Check if any error occurred when run the user code
    if(process.returncode == 1):

        return "Status 1"

    return (True)

def testUserFile():

    arrayAnswerOut = []

    with open(INPUT_DIR_EXERCISE_FILE, 'r') as fileInReaded:

        fileInRows = fileInReaded.read().splitlines()

        fileInReaded.close

    with open(OUTPUT_DIR_EXERCISE_FILE, 'r') as fileOutReaded:

        fileOutRows = fileOutReaded.read().splitlines()

        fileOutReaded.close

    for line in fileInRows:

        splitter = line.split(' ')

        #Execute the .tempuserout file and pass the arguments
        userCodeOut = pexpect.spawn('./' + FILE_USER_COMPILED, timeout=5)

        for i in splitter: 

            userCodeOut.sendline(i)

        checkExpectOut = userCodeOut.expect([pexpect.EOF, pexpect.TIMEOUT])

        if(checkExpectOut == 1 ):

            writeFinal("3", False)

            return "Status 3"

        splitStr = userCodeOut.before.split('\n')

        if(splitStr[len(splitStr)-1].replace('\r','') != ""):

            writeFinal("4", False)

            return "Status 4"

        else:

            finalStrOut = splitStr[len(splitStr)-2].replace('\r','')

        arrayAnswerOut.append(finalStrOut)

        userCodeOut.close()

    if(writeFileOut(arrayAnswerOut, FILE_USER_ANSWER_OUT) == True):

        deleteFile(FILE_USER_ANSWER_OUT)

        return (True)

    else:

        if(DEBUG): print("Problems when write the user output result to output temp file.\n")

        return (False)

def writeFileOut(dataInput, fileToWrite):

    try:

        generateOutFile = open(fileToWrite, 'a') #Create and write at the file - not truncate

        for item in dataInput:
            generateOutFile.write(str(item) + "\n")

        generateOutFile.close

        if(DEBUG): print("Write at the file " + fileToWrite + ": ok.\n")

        return (True)

    except Exception, e:

        if(DEBUG): print(e)

        if(DEBUG): print("Problems when write file out.\n")

        return (False)

def compareFiles(generateOutput):

    if(DEBUG): print("Compare the files:\n")

    try:

        booleanResult = filecmp.cmp(OUTPUT_DIR_EXERCISE_FILE, FILE_USER_ANSWER_OUT)

        if(booleanResult == True):

            if(DEBUG): print("Diff result: equal.\n")

        else:

            if(DEBUG): print("Diff result: not equal.\n")                

        result = checkStatus24(OUTPUT_DIR_EXERCISE_FILE, FILE_USER_ANSWER_OUT)

        if(generateOutput == True): #Generate the output file containing all tests

            fileOut = open(FILE_USER_OUT, 'a')

            fileOut.write(str(result) + "\n")

            fileOut.close    

        if(str(result).find('Status 2') != -1):

            writeFinal("2", False)

            return "Status 2"

        elif(str(result).find('Status 4') != -1 ):

            writeFinal("4", False)

            return "Status 4"    
    
        writeFinal("5", True)

        if(DEBUG): print("Compare the files: ok.\n")

        return (True)

    except Exception, e:

        if(DEBUG): print(e)

        if(DEBUG): print("Problems when comparing the output files.\n")

        return (False)

def moveFiles(judgedOrNot):

    try:
        
        if(judgedOrNot == "judged"):

            shutil.move(FILE_USER_IN_ORIGIN, FILE_USER_IN_JUDGED_DEST)

        elif(judgedOrNot == "nojudged"):

            shutil.move(FILE_USER_IN_ORIGIN, FILE_USER_IN_NO_JUDGED_DEST)

        if(DEBUG): print("Move the file " +  FILE_USER_IN_ORIGIN + ": ok.\n")

        return (True)

    except Exception, e:

        if(DEBUG): print(e)

        if(DEBUG): print ("Problems when move the judged files.\n")

        return (False)

def deleteFile(fileToDelete):

    try:

        prepareCmdOut = ["rm", fileToDelete];

        getCompilerOutput = subprocess.Popen(prepareCmdOut, shell=False);

        if(DEBUG): print("Delete the file " + fileToDelete + ": ok.\n")

        return (True)

    except Exception, e:
    
        if(DEBUG): print(e)

        if(DEBUG): print ("Problems when delete the judged files.\n")

        return (False)

def writeFinal(case, boolean):

    CASE_1_OK = "1: ACCEPTED"
    CASE_2_OK = "2: ACCEPTED"
    CASE_3_OK = "3: ACCEPTED"
    CASE_4_OK = "4: ACCEPTED"
    CASE_5_OK = "5: ACCEPTED"

    CASE_1_NOK = "1: ERROR"
    CASE_2_NOK = "2: ERROR"
    CASE_3_NOK = "3: ERROR"
    CASE_4_NOK = "4: ERROR"
    CASE_5_NOK = "5: ERROR"

    try:

        generateOutFile = open(FILE_USER_OUT, 'a') #Truncate the file out and write

        if(boolean == True):

            if(case == "1"): 

                generateOutFile.write(CASE_1_OK + "\n")

            elif(case == "2") :

                generateOutFile.write(CASE_2_OK + "\n")

            elif(case == "3") :

                generateOutFile.write(CASE_3_OK + "\n")

            elif(case == "4"): 

                generateOutFile.write(CASE_4_OK + "\n")

            elif(case == "5"): 

                generateOutFile.write(CASE_5_OK + "\n")

        else:

            if(case == "1"): 

                generateOutFile.write(CASE_1_NOK + "\n")

            elif(case == "2") :

                generateOutFile.write(CASE_2_NOK + "\n")

            elif(case == "3") :

                generateOutFile.write(CASE_3_NOK + "\n")

            elif(case == "4"):

                generateOutFile.write(CASE_4_NOK + "\n")

            elif(case == "5"): 

                generateOutFile.write(CASE_5_NOK + "\n")
            
        generateOutFile.close

        return (True)

    except Exception, e:

        print(e)

        return (False)

def checkStatus24(expectedOutput, userOutput):

    try:

        with open(expectedOutput, 'r') as expectedAlias:
            expectedOut = expectedAlias.read().splitlines()
        expectedAlias.close

        with open(userOutput, 'r') as userAlias:
            userOut = userAlias.read().splitlines()
        userAlias.close

        arrayAnswerOut = []

        for rowExpect, rowUser in map(None, expectedOut, userOut):

            tempExpectedO = rowExpect.replace(' ', '')

            tempUserO = rowUser.replace(' ', '')

            lengthExpectedO = len(rowExpect) 

            lengthUserO = len(rowUser)

            if((rowExpect.find('=') != -1 and rowUser.find('=') != -1) or (rowExpect.find(':') != -1 and rowUser.find(':') != -1)):

                if((rowExpect.find('=') != -1 and rowUser.find('=') != -1)):

                    splitExpectedO = tempExpectedO.split('=')[1]
 
                    splitUserO = tempUserO.split('=')[1]

                elif((rowExpect.find(':') != -1 and rowUser.find(':') != -1)):

                    splitExpectedO = tempExpectedO.split(':')[1]

                    splitUserO = tempUserO.split(':')[1]                

                if((splitExpectedO == splitUserO) and lengthExpectedO != lengthUserO): #Error status 4

                    arrayAnswerOut.append("Status 4:" + " {" + str(rowExpect) + " with " + str(rowUser) + "}")

                elif(splitExpectedO != splitUserO):

                    arrayAnswerOut.append("Status 2:" + " {" + str(rowExpect) + " with " + str(rowUser) + "}")

                else:

                    arrayAnswerOut.append("Status 5:" + " {" + str(rowExpect) + " with " + str(rowUser) + "}")

            else:

                if(rowExpect == rowUser):

                    arrayAnswerOut.append("Status 5:" + " {" + str(rowExpect) + " with " + str(rowUser) + "}")                

                elif(rowExpect != rowUser):

                    arrayAnswerOut.append("Status 2:" + " {" + str(rowExpect) + " with " + str(rowUser) + "}")

        if(DEBUG): print(str(arrayAnswerOut) + "\n")

        return arrayAnswerOut

    except Exception, e:

        if(DEBUG): print(e)

        return (False)

#The __main__ is the main module to be executed when this script (compiler.py) is ran
if __name__ == '__main__':

    main()