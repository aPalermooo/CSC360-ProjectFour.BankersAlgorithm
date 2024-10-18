"""
"   
"   File:       banker.py
"   Author:     Xander Palermo <ajp2s@missouristate.edu>
"   Course:     CSC360 - Operating Systems
"   Instructor: Dr. Siming Liu
"   Project:    4 - Implementation of Banker's Algorithm
"   Date:       21 October 2024
" 
"""
import os
import sys
from ProcessManager import ProcessManager


def readFile(filename: str) -> ProcessManager:
    """
    :function readFile:
    Opens a specified file and formats the data contained in it into a ProcessManager Object
    :param filename: the name of the file to be opened
    :return: a ProcessManager Object containing the data from the text file
    """
    # Open File
    file = open(filename, 'r')

    # Retrieve arguments
    numProcesses = file.readline()
    file.readline()
    numResources = file.readline()

    numProcesses = int(numProcesses)
    numResources = int(numResources)


    file.readline()

    # Retrieve allocation matrix
    allocationMatrix = []
    for i in range(numProcesses):
        allocationMatrix.append(file.readline().split())
        allocationMatrix[i] = list(map(int, allocationMatrix[i]))


    file.readline()

    # Retrieve max matrix
    maxMatrix = []
    for i in range(numProcesses):
        maxMatrix.append(file.readline().split())
        maxMatrix[i] = list(map(int, maxMatrix[i]))


    file.readline()

    # Retrieve current vector
    currentVector = file.readline().split()
    currentVector = list(map(int, currentVector))

    file.readline()

    # Retrieve request vector
    requestVector = file.readline().split()
    requestVector[0] = requestVector[0].split(":")
    requestVector[0] = requestVector[0][1]
    requestVector = list(map(int, requestVector))


    pManager = ProcessManager(numProcesses, numResources, allocationMatrix, maxMatrix, currentVector, requestVector)
    return pManager

def createLog(message: str) -> None:
    """
    :function createLog:
    Creates a file called bankerLog.txt that contains the output of the program
    :pre: If a bankerLog.txt file exists, it will be deleted and a new one will be created in its place
    :param message: the message to be logged
    :return: None
    """
    try:
        os.remove("bankerLog.txt")
    except OSError:
        pass
    file = open("bankerLog.txt", "w")
    file.write(message)
    return

def main() -> int:
    """
    :function main:
    Driver of banker algorithm.
    :param arg: The file that contains the data to apply the Bankers Algorithm to
                If no args are given, the program defaults to trying to open s1.txt
    :return: 0 for success
    """
    if not sys.argv[1:]:
        arg = "s1.txt"
    else:
        arg = sys.argv[1]
    pManager = readFile(arg)
    createLog(str(pManager))
    return 0
main()