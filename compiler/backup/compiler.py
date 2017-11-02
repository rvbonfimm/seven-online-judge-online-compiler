#!/usr/bin/env python

import sys
import os
import subprocess
import pexpect
import py_compile
import logging as log

from subprocess import Popen, PIPE
from pexpect import *


# Set the Debug Mode On or Off
if str(sys.argv).find('-d') != -1:

    DEBUG = True

else:

    DEBUG = False

def main():

    MAIN_DIR = str(sys.argv[0]).replace("compiler.py", "")

    FILE_USER_IN_DIR = str(sys.argv[1])

    JUDGE_DIR = MAIN_DIR + "tojudge/"

    JUDGED_FILE_DIR = MAIN_DIR + "judged/"

    LOG_DIR = MAIN_DIR + "logs/"

    TEMP_DIR = JUDGE_DIR + "temp/"

    FILE_USER_IN = FILE_USER_IN_DIR.replace(JUDGE_DIR, "")

    EXERCISES_DIR = MAIN_DIR + "exercises/"

    EXERCISE_NUMBER = FILE_USER_IN[:4]

    LOG_FILE = LOG_DIR + FILE_USER_IN.split('.')[0] + ".judgelog"

    EXERCISE_IN = EXERCISES_DIR + "input/" + EXERCISE_NUMBER + ".exercisein" 

    EXERCISE_OUT = EXERCISES_DIR + "output/" + EXERCISE_NUMBER + ".exerciseout"

    FILE_USER_ANSWER_OUT = TEMP_DIR + FILE_USER_IN.split('.')[0] + ".useranswerout"

    FILE_USER_JUDGED_RESULT = TEMP_DIR + FILE_USER_IN.split('.')[0] + ".judgeresult"

    log.basicConfig(filename=LOG_FILE, level=log.DEBUG, format='%(asctime)s - %(levelname)s: %(message)s')

    WITHDETAIL = True

    log.info("---------------- Start of Judgement -----------------\n")

    log.info("Language selected: " + str(FILE_USER_IN.split('.')[1]))

    #Search for the language choose
    if FILE_USER_IN.split('.')[1] == 'c':

        LANGUAGE = 'c'

        FILE_USER_COMPILED = FILE_USER_IN.split('.')[0] + ".gcctemp"

    elif FILE_USER_IN.split('.')[1] == 'py':

        LANGUAGE = 'python'

        FILE_USER_COMPILED = JUDGE_DIR + FILE_USER_IN.split('.')[0] + ".pyc"

    log.info("Starting 'Status 1' treatment")
    
    #Search for Status 1
    status = firstStatus(LANGUAGE, FILE_USER_IN_DIR, FILE_USER_COMPILED)

    moveFile(FILE_USER_IN_DIR, JUDGED_FILE_DIR)

    log.info("Status 1: " + str(status))

    if status:

        return "Status 1"

    log.info("Starting 'Status 2, 3 and 4' treatment")

    #Search for Status 2, 3 or 4
    userCodeStatus = testUserCode(LANGUAGE, EXERCISE_IN, FILE_USER_COMPILED, FILE_USER_ANSWER_OUT)
    
    deleteFile(FILE_USER_COMPILED)

    if userCodeStatus == "Status 3" or userCodeStatus == "Status 4":

        return userCodeStatus

    else:

        status = compareValues(EXERCISE_OUT, FILE_USER_ANSWER_OUT, WITHDETAIL)

        deleteFile(FILE_USER_ANSWER_OUT)

        if status == "Status 5":

            log.info("Status 2, 3 and 4: any problem was found.")

            log.info("The user code was succesfully accepted.")          

            return status

        return status


def firstStatus(language, fileInput, fileCompiled):

    log.info("Compiling the file: " + str(fileInput))

    if language == "c":

        log.info("Printing the .c file in: " + str(fileInput))

        cmd = ["gcc", fileInput, "-o", fileCompiled]

        log.info("Printing the .c file out: " + str(fileCompiled))

    elif language == "python":

        log.info("Printing the .py file in: " + str(fileInput))

        cmd = ["python", "-m", "py_compile", fileInput]

        log.info("Printing the .py file out: " + str(fileCompiled))

    log.info("Printing the command: " + str(cmd))

    try:

        subprocess.check_call(cmd)

        return False

    except subprocess.CalledProcessError, c:

        log.info(str(c))

        return True

    except py_compile.PyCompileError, p:

        log.info("[EXCEPTION] " + str(p))

        return True

    except Exception, e:

        log.error("[EXCEPTION] " + str(e))

        return True


def testUserCode(language, exercise_in, compiledFile, fileUserAnswerOut):

    try:

        with open(exercise_in, 'r') as fileInReaded:

            fileInRows = fileInReaded.read().splitlines()

        fileInReaded.close

        log.info("File readed: " + str(fileInRows))

        answerOut = []

        #Check if is necessary to put some parameter at user code
        if len(fileInRows) != 0:

            log.info("Found case test in exercise in files")

            #Each line is a case to test with the user code
            for line in fileInRows:

                print "Line readed for exercise in: %s\n" % line

                #Check for empty value - if yes, loop to next line
                if line == "empty":

                    log.info("Empty line readed. Loop to next iterator")

                    continue

                log.info("Line: " + str(line))

                splitter = line.split(' ')

                log.info("Splitter: " + str(splitter))

                if language == 'c':

                    cmd = ('./' + compiledFile)

                elif language == 'python':

                    cmd = ('python ' + compiledFile)

                child = pexpect.spawn(cmd, timeout=10)

                for item in splitter:

                    log.info("Item splitted putted: " + str(item))

                    child.sendline(item)

                checkexpectout = child.expect([pexpect.EOF, pexpect.TIMEOUT])

                if checkexpectout == 1:

                    return "Status 3"

                log.info("Child before: " + str(child.before))

                splitout = child.before.split('\n')

                log.info("Pexpect out: " + str(splitout))

                if language == 'c':

                    searchnewline = splitout[len(splitout)-1]

                elif language == 'python':

                    if splitout[len(splitout)-2] == '\r': #\n at print function

                        return "Status 4"

                    searchnewline = splitout[len(splitout)-1]

                if searchnewline != "":

                    return "Status 4"

                child.close()

                finalout = splitout[len(splitout)-2].replace('\r', '')

                answerOut.append(finalout)

        else:

            log.info("Any input was found at exercise in files")

            #Check the language to compile
            if language == 'c':

                cmd = ('./' + compiledFile)

            elif language == 'python':

                cmd = ('python ' + compiledFile)

            #Execute the user code
            child = pexpect.spawn(cmd, timeout=5)

            #Check for user code output
            checkexpectout = child.expect([pexpect.EOF, pexpect.TIMEOUT])

            if checkexpectout == 1:

                return "Status 3"

            log.info("Child before: " + str(child.before))

            splitout = child.before.split('\n')

            log.info("Pexpect out: " + str(splitout))

            if language == 'c':

                searchnewline = splitout[len(splitout)-1]

            elif language == 'python':

                if splitout[len(splitout)-2] == '\r': #\n at print function

                    return "Status 4"

                searchnewline = splitout[len(splitout)-1]

            if searchnewline != "":

                return "Status 4"

            child.close()

            finalout = splitout[len(splitout)-2].replace('\r', '')

            answerOut.append(finalout)

        generatefileout = open(fileUserAnswerOut, 'w')

        for item in answerOut:

            log.info("Answer out: " + str(item))

            generatefileout.write(item + "\n")

        generatefileout.close

        return True

    except Exception, e:

        log.error("[EXCEPTION] " + str(e))

        return False


def compareValues(exercise_out, fileUserAnswerOut, withDetail):

    try:

        log.info("Comparing the files: " + str(exercise_out) + "\nwith: " + str(fileUserAnswerOut))

        log.info("With output detail? " + str(withDetail))

        if not withDetail:

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

                if our == user:

                    result = "Status 5"

                else:

                    tempOur = our.replace(" ", "")

                    tempUser = user.replace(" ", "")

                    if tempOur != tempUser:

                        result = "Status 2"

                    else:

                        result = "Status 4"                        
        
                resultOut.append("Line " + str(aux) + ": '" + str(result) + "'; Expected result: '" + str(our) + "'; Your result: '" + str(user) + "';\n")

                aux += 1

            for item in resultOut:

                log.info(str(item))

        return result

    except Exception, e:

        log.error("[EXCEPTION] " + str(e))

        return False


def deleteFile(fileInput):

    log.info("Deleting the file: " + str(fileInput))

    try:

        cmd = ["rm", fileInput]

        subprocess.Popen(cmd, shell=False)

        log.info("Deleted successfully.")

        return True

    except Exception, e:

        log.error("[EXCEPTION] " + str(e))

        return False


def moveFile(fileInput, destiny):

    log.info("Moving the file: " + str(fileInput) + " to: " + str(destiny))

    try:

        cmd = ["mv", fileInput, destiny]

        subprocess.Popen(cmd, shell=False);        

        log.info("Moved successfully.")

        return True

    except Exception, e:

        log.error("[EXCEPTION] " + str(e))

        return False

if __name__ == '__main__':

    result = main()

    log.info(str(result))

    log.info("---------------- End of Judgement ----------------\n")

    print result
