"""
"
"   File:       ProcessManager.py
"   Author:     Xander Palermo <ajp2s@missouristate.edu>
"   Course:     CSC360 - Operating Systems
"   Instructor: Dr. Siming Liu
"   Project:    4 - Implementation of Banker's Algorithm
"   Date:       21 October 2024
"
"""

"""
General Notes:
for loops that iterate over Processes navigate through matrices through the y-axis
for loops that iterate over Resources navigate through matrices the x-axis
"""


class ProcessManager:
    """
    :class ProcessManager:
        A class that applies the banker algorithm to a given set of data and evaluates if a request for resources made by
         a new Process can be fulfilled.

    ...
    Attributes
    -------------
    __numProcesses : int                        Number of processes that already have resources allocated to them
    __numResources : int                        Number of resources that the processes are competing for
    __allocationMatrix : list[list[int]]        A matrix of processes and the resources that are currently allocated to them
    __maxMatrix : list[list[int]]               A matrix of processes and the resources that they require in their worse case scenario
    __currentMatrix : list[list[int]]           A matrix of the current number of resources available over time
    __requestVector : list[int]                 A list of resources a new process is requesting to be allocated to it
    __needMatrix : list[list[int]]              A matrix of processes and the resources they still need to be allocated to them to fulfill their worst case scenario needs
    __isSafeInitial : bool                      can a deadlock occur with the current resources allocated as they are
    __isSafeRequest : bool                      can the requestVector be filled (there are more resources available than are requested
    __allocatedAfterRequest : list[int]         A list of resources that remain after resources are allocated to the worst case scenario of the requestVector

    ...
    Methods
    -------------
    __attemptAllocation(self)
        applies the banker algorithm to the given set of data to determine if the current allocation is safe
    """


    def __init__(self, numProcesses: int, numResources: int, allocationMatrix: list[list[int]], maxMatrix: list[list[int]], currentVector: list[int], requestVector: list[int]):
        """"
        __init__
            Creates a new instance of ProcessManager
        :param numProcesses: Number of processes that already have resources allocated to them
        :param numResources: Number of resources that the processes are competing for
        :param allocationMatrix: A matrix of processes and the resources that are currently allocated to them
        :param maxMatrix: A matrix of processes and the resources that they require in their worse case scenario
        :param currentVector: A list of the current number of resources available after allocating to the current processes running
        :param requestVector: A list of the resources a new process is requesting to be allocated to it
        :return ProcessManager: Object
        """

        self.__numProcesses = numProcesses
        self.__numResources = numResources
        self.__allocationMatrix = allocationMatrix
        self.__maxMatrix = maxMatrix
        self.__currentMatrix = []
        self.__currentMatrix.append(currentVector)
        self.__requestVector = requestVector

        self.__needMatrix = []
        for process in range(numProcesses):
            processNeeds = []
            for resource in range(numResources):
                processNeeds.append(self.__maxMatrix[process][resource] - self.__allocationMatrix[process][resource])
            self.__needMatrix.append(processNeeds)

        self.__isSafeInitial = self.__attemptAllocation()
        self.__isSafeRequest = True

        # Check if resources are available
        for resource in range(self.__numResources):
            if self.__requestVector[resource] > self.__currentMatrix[0][resource]:
                self.__isSafeRequest = False
                break

        # if resources are available set, allocate them and compute remaining resources
        if self.__isSafeRequest:
            self.__allocatedAfterRequest = self.__currentMatrix[0]
            for resource in range(self.__numResources):
                self.__allocatedAfterRequest[resource] -= self.__requestVector[resource]
        else:
            self.__allocatedAfterRequest = None



    def __attemptAllocation(self) -> bool:
        """
        __attemptAllocation
            Will apply the banker algorithm to the given set of data to determine if it is currently in a safe state
        :return bool: True if the system is in a safe state; false if not
        """
        # Preconditions
        time = 0
        safe = True         #Optimistically set

        # Make list of Processes to be allocated
        processesWaiting = []
        for process in range(self.__numProcesses):
            processesWaiting.append(process)


        index = 0  #index of a process within processesWaiting
        allocatable = True  #Optimistically set

        #For as long as there are processes waiting and the system has not been proven unsafe
        while safe and processesWaiting:
            for index, process in enumerate(processesWaiting):

                #Attempting to deallocate a process in Waiting
                allocatable = True #Optimistically set

                #Check to see if resources are available
                for resource in range(self.__numResources):

                    if self.__needMatrix[process][resource] > self.__currentMatrix[time][resource]: # If need more resources than available, it is not allocatable; move on to next process
                        allocatable = False
                        break
                if allocatable: #If resources are available, dont check other processes
                    break

            time += 1
            if allocatable: #Deallocate a Process (add its resources back to the pool)
                deallocatedProcess = processesWaiting[index]

                self.__currentMatrix.append([])
                for resource in range(self.__numResources):
                    self.__currentMatrix[time].append(self.__currentMatrix[time - 1][resource] + self.__allocationMatrix[deallocatedProcess][resource])
                processesWaiting.pop(index)
                continue

            # if not allocatable
            safe = False
        return safe


    def __str__(self) -> str:
        """
        __str__
            Creates a string representation of the ProcessManager object and its current attributes to display to a user
        :return: a string representation of the ProcessManager object
        """

        # Format __allocationMatrix
        allocationMatrix = "   A B C D\n"
        for process in range(self.__numProcesses):
            allocations = ""
            for resource in range(self.__numResources):
                allocations += str(self.__allocationMatrix[process][resource]) + " "
            allocationMatrix = allocationMatrix + f"{process}: {allocations}" + "\n"

        # Format __maxMatrix
        maxMatrix = "   A B C D\n"
        for process in range(self.__numProcesses):
            worseCase = ""
            for resource in range(self.__numResources):
                worseCase += str(self.__maxMatrix[process][resource]) + " "
            maxMatrix = maxMatrix + f"{process}: {worseCase}" + "\n"

        # Format __needMatrix
        needMatrix = "   A B C D\n"
        for process in range(self.__numProcesses):
            resourcesNeeded = ""
            for resource in range(self.__numResources):
                resourcesNeeded += str(self.__needMatrix[process][resource]) + " "
            needMatrix = needMatrix + f"{process}: {resourcesNeeded}" + "\n"

        # Format __currentVector
        availablePre = " ".join(str(x) for x in self.__currentMatrix[0])

        # Format __isSafeInitial
        if self.__isSafeInitial:
            outputSafety = "THE SYSTEM IS IN A SAFE STATE!"
        else:
            outputSafety = "THE SYSTEM IS IN AN UNSAFE STATE!"

        requestVector = "1:" + " ".join(str(x) for x in self.__requestVector)

        # Format __isSafeRequest
        if self.__isSafeRequest:
            outputRequest = "THE REQUEST CAN BE GRANTED!"
        else:
            outputRequest = "THE REQUEST CANNOT BE GRANTED!"

        # Format __allocatedAfterRequest
        availablePost = " ".join(str(x) for x in self.__allocatedAfterRequest)

        # Compile all variables into a string format using an f string
        return (f"There are {self.__numProcesses} process in the system.\n"
                f"\n"
                f"There are {self.__numResources} resource types.\n"
                f"\n"
                f"The Allocation Matrix is...\n"
                f"{allocationMatrix}\n"
                f"The Max Matrix is...\n"
                f"{maxMatrix}\n"
                f"The Need Matrix is...\n"
                f"{needMatrix}\n"
                f"The Available Vector is...\n"
                f"A B C D\n"
                f"{availablePre}\n"
                f"\n"
                f"{outputSafety}\n"
                f"\n"
                f"The Request Vector is...\n"
                f"  A B C D\n"
                f"{requestVector}\n"
                f"\n"
                f"{outputRequest}\n"
                f"\n"
                f"The Available Vector is...\n"
                f"A B C D\n"
                f"{availablePost}\n"
                )


