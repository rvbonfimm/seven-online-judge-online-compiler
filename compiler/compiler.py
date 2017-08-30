#!/usr/bin/env python

import os
import subprocess
import pexpect
import sys
import py_compile

from subprocess import Popen, PIPE
from pexpect import *


# Set the Debug Mode On or Off
if (str(sys.argv).find('-d') != -1): 

    DEBUG = True

else: 

    DEBUG = False


def main():

    MAIN_DIR = ((os.getcwd()).replace("web", "compiler") + "/")

    FILE_USER_IN_DIR = str(sys.argv[1])

    JUDGE_DIR = MAIN_DIR + "tojudge/"

    JUDGED_FILE_DIR = MAIN_DIR + "judged/"

    TEMP_DIR = JUDGE_DIR + "temp/"

    FILE_USER_IN = FILE_USER_IN_DIR.replace(JUDGE_DIR,"")

    EXERCISES_DIR = MAIN_DIR + "exercises/"

    EXERCISE_NUMBER = FILE_USER_IN[:4]

    EXERCISE_IN = EXERCISES_DIR + "input/" + EXERCISE_NUMBER + ".exercisein" 

    EXERCISE_OUT = EXERCISES_DIR + "output/" + EXERCISE_NUMBER + ".exerciseout"

    FILE_USER_ANSWER_OUT = TEMP_DIR + FILE_USER_IN.split('.')[0] + ".useranswerout"

    FILE_USER_JUDGED_RESULT = TEMP_DIR + FILE_USER_IN.split('.')[0] + ".judgeresult"

    WITHDETAIL = True
    
    #Search for the language choose
    if DEBUG: print("[DEBUG] Language selected: " + str(FILE_USER_IN.split('.')[1]) + "\n")

    if (FILE_USER_IN.split('.')[1] == 'c'):

        LANGUAGE = 'c'

        FILE_USER_COMPILED = FILE_USER_IN.split('.')[0] + ".gcctemp"

    elif(FILE_USER_IN.split('.')[1] == 'py'):

        LANGUAGE = 'python'

        FILE_USER_COMPILED = JUDGE_DIR + FILE_USER_IN.split('.')[0] + ".pyc"

    if DEBUG: print("[DEBUG] Starting 'Status 1' treatment\n")
    
    #Search for Status 1
    status = firstStatus(LANGUAGE, FILE_USER_IN_DIR, FILE_USER_COMPILED)

    moveFile(FILE_USER_IN_DIR, JUDGED_FILE_DIR)

    if DEBUG: print("[DEBUG] Status 1: " + str(status) + "\n")

    if(status):

        deleteFile(FILE_USER_COMPILED)

        return "Status 1"

    if DEBUG: print("[DEBUG] Starting 'Status 2, 3 and 4' treatment\n")

    #Search for Status 2, 3 or 4
    userCodeStatus = testUserCode(LANGUAGE, EXERCISE_IN, EXERCISE_OUT, FILE_USER_COMPILED, FILE_USER_ANSWER_OUT)
    
    deleteFile(FILE_USER_COMPILED)

    if(userCodeStatus == "Status 3" or userCodeStatus == "Status 4"):

        return userCodeStatus

    else:

        status = compareValues(EXERCISE_OUT, FILE_USER_ANSWER_OUT, WITHDETAIL)

        deleteFile(FILE_USER_ANSWER_OUT)

        if(status == "Status 5"):

            if DEBUG: print("[DEBUG] Status 2, 3 and 4: any problem was found.\n")

            if DEBUG: print("[DEBUG] The user code was succesfully accepted.\n")

        return status


def firstStatus(language, fileInput, fileCompiled):

    if DEBUG: print("[DEBUG] Compiling the file: " + str(fileInput) + "\n")

    if(language == "c"):

        if DEBUG: print("[DEBUG] Printing the .c file in: " + str(fileInput) + "\n")

        cmd = ["gcc", fileInput, "-o", fileCompiled]

        if DEBUG: print("[DEBUG] Printing the .c file out: " + str(fileCompiled) + "\n")

    elif(language == "python"):

        if DEBUG: print("[DEBUG] Printing the .py file in: " + str(fileInput) + "\n")

        cmd = ["python", "-m", "py_compile", fileInput]        

        if DEBUG: print("[DEBUG] Printing the .py file out: " + str(fileCompiled) + "\n")

    if DEBUG: print("[DEBUG] Printing the command: " + str(cmd) + "\n")

    try:

        subprocess.check_call(cmd)

        return False

    except subprocess.CalledProcessError, c:

        if DEBUG: print("[DEBUG - EXCEPTION] " + str(c) + "\n")

        return True

    except py_compile.PyCompileError, p:

        if DEBUG: print("[DEBUG - EXCEPTION] " + str(p) + "\n")

        return True

    except Exception, e:

        if DEBUG: print("[DEBUG - EXCEPTION] " + str(e) + "\n")

        return True


def testUserCode(language, exercise_in, exercise_out, compiledFile, fileUserAnswerOut):

    try:

        with open(exercise_in, 'r') as fileInReaded:

            fileInRows = fileInReaded.read().splitlines()

        fileInReaded.close

        answerOut = []

        #Each line is a case to test with the user code
        for line in fileInRows:
            
            splitter = line.split(' ')

            if(language == 'c'):

                cmd = ('./' + compiledFile)

            elif(language == 'python'):

                cmd = ('python ' + compiledFile)

            userCodeOut = pexpect.spawn(cmd, timeout=4)

            for item in splitter:

                userCodeOut.sendline(item)

            checkExpectOut = userCodeOut.expect([pexpect.EOF, pexpect.TIMEOUT])

            if(checkExpectOut == 1 ):

                return "Status 3"

            splitOut = userCodeOut.before.split('\n')

            if(language == 'c'):

                searchForNewLine = splitOut[len(splitOut)-1]

            elif(language == 'python'):            

                if(splitOut[len(splitOut)-2] == '\r'):

                    return "Status 4" #\n at print function

                searchForNewLine = splitOut[len(splitOut)-1]

            if(searchForNewLine != ""):

                return "Status 4"

            userCodeOut.close()

            finalOut = splitOut[len(splitOut)-2].replace('\r','')

            answerOut.append(finalOut)

        generateFileOut = open(fileUserAnswerOut, 'w')

        for item in answerOut:

            generateFileOut.write(item + "\n")

        generateFileOut.close

        return True

    except Exception, e:

        if DEBUG: print("[DEBUG - EXCEPTION] " + str(e) + "\n")

        return False


def compareValues(exercise_out, fileUserAnswerOut, withDetail):

    try:

        if DEBUG: print("[DEBUG] Comparing the files: " + str(exercise_out) + "\nwith: " + str(fileUserAnswerOut) + "\n")

        if DEBUG: print("[DEBUG] With output detail? " + str(withDetail) + "\n")

        if not(withDetail):

            result = open(exercise_out, 'rb').read() == open(fileUserAnswerOut, 'rb').read()

        else:
        
            resultOut = []

            aux = 1

            with open(exercise_out, 'r') as ourFileOutReaded:

                ourFileOut = ourFileOutReaded.read().splitlines()

            ourFileOutReaded.close()

            with open(fileUserAnswerOut, 'r') as fileUserOutReaded:

                fileOutUser = fileUserOutReaded.read().splitlines()

            fileUserOutReaded.close()

            for our, user in zip(ourFileOut, fileOutUser):

                if(our == user):

                    result = "Status 5"

                else:

                    tempOur = our.replace(" ", "")

                    tempUser = user.replace(" ", "")

                    if(tempOur != tempUser):

                        result = "Status 2"

                    else:

                        result = "Status 4"                        
        
                resultOut.append("Line " + str(aux) + ": " + str(result) + "; Expected result: " + str(our) + "; Your result: " + str(user) + ";\n")

                aux += 1

            for item in resultOut:

                if DEBUG: print ("[DEBUG] " + str(item))

        if DEBUG: print("[DEBUG] Comparing the files: " + str(result) + "\n")

        return result

    except Exception, e:

        if DEBUG: print("[DEBUG - EXCEPTION] " + str(e) + "\n")

        return False


def deleteFile(fileInput):

    if DEBUG: print("[DEBUG] Deleting the file: " + str(fileInput) + "\n")

    try:

        cmd = ["rm", fileInput]

        subprocess.Popen(cmd, shell=False);

        if DEBUG: print("[DEBUG] Deleted successfully.\n")

        return True

    except Exception, e: 

        if DEBUG: print("[DEBUG - EXCEPTION] " + str(e) + "\n")

        return False


def moveFile(fileInput, destiny):

    if DEBUG: print("[DEBUG] Moving the file: " + str(fileInput) + " to: " + str(destiny) + "\n")

    try:

        cmd = ["mv", fileInput, destiny]

        subprocess.Popen(cmd, shell=False);        

        if DEBUG: print("[DEBUG] Moved successfully.\n")

        return True

    except Exception, e:

        if DEBUG: print("[DEBUG - EXCEPTION] " + str(e) + "\n")

        return False


if __name__ == '__main__':

    result = main()

    if DEBUG: print("[DEBUG] " + str(result) + "\n")

    print(result)