"""
"   
"   File:       banker.py
"   Author:     Xander Palermo <ajp2s@missouristate.edu>
"   Course:     CSC360
"   Instructor: Siming Liu
"   Project:    4 - Implementation of Banker's Algorithm
"   Date:       21 October 2024
" 
"""
import os

from ProcessManager import ProcessManager
import sys

def readFile(filename: str) -> ProcessManager:
    # Open File
    file = open(filename, 'r')

    # Retrieve parameters
    numProcesses = file.readline()
    file.readline()
    numResources = file.readline()

    numProcesses = int(numProcesses)
    numResources = int(numResources)


    file.readline()

    # Retrieve allocation matrix
    allocation = []
    for i in range(numProcesses):
        allocation.append(file.readline().split())
        allocation[i] = list(map(int, allocation[i]))


    file.readline()

    # Retrieve max matrix
    maxMatrix = []
    for i in range(numProcesses):
        maxMatrix.append(file.readline().split())
        maxMatrix[i] = list(map(int, maxMatrix[i]))


    file.readline()

    # Retrieve current
    current = file.readline().split()
    current = list(map(int, current))

    file.readline()

    # Retrieve request
    request = file.readline().split()
    request[0] = request[0].split(":")
    request[0] = request[0][1]
    request = list(map(int, request))


    pManager = ProcessManager(numProcesses, numResources, allocation, maxMatrix, current, request)
    return pManager

def createLog(message: str) -> None:
    try:
        os.remove("banker.txt")
    except OSError:
        pass
    file = open("banker.txt", "w")
    file.write(message)
    return

def main() -> int:
    if not sys.argv[1:]:
        arg = "s1.txt"
    else:
        arg = sys.argv[1]
    pManager = readFile(arg)
    createLog(str(pManager))
    return 0
main()