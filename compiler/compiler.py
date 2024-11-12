#!/usr/bin/env python

import sys
import os
import subprocess
import pexpect
import py_compile
import logging as log
import time

from subprocess import Popen, PIPE
from pexpect import *

start_time = time.time()

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

    log.basicConfig(filename=LOG_FILE, level=log.DEBUG, \
    format='%(asctime)s - %(levelname)s: %(message)s')

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
        return {
            'Status': 'Status 1'
        }

    log.info("Starting 'Status 2, 3 and 4' treatment")

    status = testUserCode(LANGUAGE, EXERCISE_IN, EXERCISE_OUT, \
    FILE_USER_COMPILED, FILE_USER_ANSWER_OUT)

    deleteFile(FILE_USER_COMPILED)

    return status

def firstStatus(language, fileInput, fileCompiled):

    log.info("Compiling the file: " + str(fileInput))

    if language == "c":

        log.info("Printing the .c file in: " + str(fileInput))

        cmd = ["gcc", fileInput, "-o", fileCompiled, "-lm"]

        log.info("Printing the .c file out: " + str(fileCompiled))

    elif language == "python":

        log.info("Printing the .py file in: " + str(fileInput))

        cmd = ["python", "-m", "py_compile", fileInput]

        log.info("Printing the .py file out: " + str(fileCompiled))

    log.info("Printing the command: " + str(cmd))

    try:
        subprocess.check_call(cmd)
        return False
    except subprocess.CalledProcessError as c:
        log.info("[EXCEPTION] " + str(c))
        return True
    except py_compile.PyCompileError as p:
        log.info("[EXCEPTION] " + str(p))
        return True
    except Exception as e:
        log.error("[EXCEPTION] " + str(e))
        return True

def testUserCode(language, exercise_in, exercise_out, compiledFile, fileUserAnswerOut):

    try:
        with open(exercise_in, 'r') as fh_input:
            fileInRows = fh_input.read().splitlines()

        fh_input.close

        with open(exercise_out, 'r') as fh_output:
            fileOutRows = fh_output.read().splitlines()

        fh_output.close

        if language == 'c':
            cmd = ('./' + compiledFile)
        elif language == 'python':
            cmd = ('python ' + compiledFile)

        list_out = []

        #Each line is a case to test with the user code
        for lineIn, lineOut in zip(fileInRows, fileOutRows):
            caseIn = lineIn.split("|")
            caseOut = lineOut.split("|")
            child = pexpect.spawn(cmd, timeout=5)

            for pin, pout in zip(caseIn, caseOut):
                log.info("pin: " + str(pin))
                log.info("pout: " + str(pout))

                #Check if is necessary to put some parameter at user code
                if pin != "empty":
                    splitter = pin.split(';')
                    for item in splitter:
                        log.info("Item splitted putted: " + str(item))
                        child.sendline(item)

                #Search for empty value at exercise output file
                if pout == "empty":
                    log.info("Line out readed is empty. Loop to next line.")
                    continue

                checkexpectout = child.expect([pexpect.EOF, pexpect.TIMEOUT])

                if checkexpectout == 1:
                    return {
                        'Status': 'Status 3'
                    }

                pexpectout = []

                for item in child.before.split("\n"):
                    pexpectout.append(item)

                #Close the child process spawned
                child.close()

                log.info("pexpect array out: " + str(pexpectout))

                # Start to search for Status 2 or 4
                if language == 'c':
                    searchnewline = pexpectout[len(pexpectout)-1]
                elif language == 'python':
                    # Search for \n at python print function
                    if pexpectout[len(pexpectout)-2] == '\r':
                        return "Status 4"

                    searchnewline = pexpectout[len(pexpectout)-1]

                if searchnewline != "":
                    return {
                        'Status': 'Status 4',
                        'Data': searchnewline
                    }

                finalout = pexpectout[len(pexpectout)-2].replace('\r', '')

                log.info("Pexpect out: " + str(finalout))
                log.info("Our expected output: " + str(pout))

                if finalout != pout:
                    clearPexpectOut = finalout.strip()
                    if clearPexpectOut != pout:
                        return {
                            'Status': 'Status 2',
                            'Data': finalout
                        }

                    else:
                        return {
                            'Status': 'Status 4',
                            'Data': finalout
                        }

                else:
                    list_out.append(str(finalout))

        return {
            'Status': 'Status 5',
            'Data': list_out
        }

    except Exception as e:
        log.error("[EXCEPTION] " + str(e))
        return False

def deleteFile(fileInput):
    log.info("Deleting the file: " + str(fileInput))

    try:
        cmd = ["rm", fileInput]
        subprocess.Popen(cmd, shell=False)
        log.info("Deleted successfully.")
        return True
    except Exception as e:
        log.error("[EXCEPTION] " + str(e))
        return False

def moveFile(fileInput, destiny):
    log.info("Moving the file: " + str(fileInput) + " to: " + str(destiny))

    try:
        cmd = ["mv", fileInput, destiny]
        subprocess.Popen(cmd, shell=False)
        log.info("Moved successfully.")
        return True
    except Exception as e:
        log.error("[EXCEPTION] " + str(e))
        return False

if __name__ == '__main__':
    result = main()
    log.info(result)

    if result.has_key('Status'):
        status = result['Status']
        log.info("Status: " + str(status))

    else:
        status = ""

    if result.has_key('Data'):
        data = result['Data']
        log.info("Data: " + str(data))
    else:
        data = ""

    end_time = str((time.time() - start_time))[0:5]

    if status and data:
        dict_result = {
            'Status': status,
            'Data': data,
            'Time': end_time
        }
    elif status:
        dict_result = {
            'Status': status,
            'Time': end_time
        }

    print(dict_result)

    log.info(dict_result)
    log.info("Execution time: %s\n" % end_time)
    log.info("---------------- End of Judgement ----------------\n")
