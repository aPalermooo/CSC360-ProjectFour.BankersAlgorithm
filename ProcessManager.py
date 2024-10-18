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


class ProcessManager:
    def __init__(self, numProcesses: int, numResources: int, allocated: list[list[int]], maxNeed: list[list[int]], current: list[int], request: list[int]):


        self.__numProcesses = numProcesses
        self.__numResources = numResources
        self.__allocated = allocated
        self.__maxNeed = maxNeed
        self.__current = []
        self.__current.append(current)
        self.__request = request

        self.__currentNeed = []
        for process in range(numProcesses):
            processNeeds = []
            for resource in range(numResources):
                processNeeds.append(self.__maxNeed[process][resource] - self.__allocated[process][resource])
            self.__currentNeed.append(processNeeds)

        self.__safeInitial = self.__attemptAllocation()
        self.__safeRequest = True
        for resource in range(self.__numResources):
            if self.__request[resource] > self.__current[0][resource]:
                self.__safeRequest = False
                break
        if self.__safeRequest:
            self.__allocatedAfterRequest = self.__current[0]
            for resource in range(self.__numResources):
                self.__allocatedAfterRequest[resource] -= self.__request[resource]



    def __attemptAllocation(self) -> bool:
        time = 0
        safe = True

        # Make list of Processes to be allocated
        processesWaiting = []
        for process in range(self.__numProcesses):
            processesWaiting.append(process)


        index = 0
        allocatable = True
        path = []
        # While processesWaiting !empty and is safe
        while safe and processesWaiting:
            # print(f"{time}----------------------------------")
            for index, process in enumerate(processesWaiting):

                #Attempting to deallocate a process in Waiting
                # print("Attempting process: " + str(process))
                allocatable = True

                #Check to see if resources are available
                for resource in range(self.__numResources):

                    if self.__currentNeed[process][resource] > self.__current[time][resource]: # If need more resources than available, it is not allocatable; move on to next process
                        allocatable = False
                        # print(f"{self.__currentNeed[process][resource]} !> {self.__current[resource]} = {allocatable}")
                        break
                if allocatable: #If resources are available, dont check other processes
                    # print(f"{process} / {self.__numProcesses - 1} - Allocated")
                    break

                # else:

                    # print(f"{process} / {self.__numProcesses - 1} - Not Allocated")
            time += 1
            if allocatable:
                # print(f"\t\tProcess {processesWaiting[index]} can be allocated\n"
                #       f"\t\tDeallocating Resources...")
                deallocatedProcess = processesWaiting[index]
                path.append(deallocatedProcess)

                # Deallocate a Process
                # print(f"\nAllocated Resources: {self.__allocated[deallocatedProcess]}")
                # self.__current.append(self.__allocated[index])
                self.__current.append([])
                for resource in range(self.__numResources):
                    self.__current[time].append(self.__current[time-1][resource] + self.__allocated[deallocatedProcess][resource])
                processesWaiting.pop(index)
                # print(f"Initial Allocation:  {self.__current[0]}")
                # print(f"Current Allocation:  {self.__current[time]}")
                # print(f"Queue:               {processesWaiting}")
                continue
            safe = False
        # print(str(path))
        return safe


    def __str__(self):

        allocationMatrix = "   A B C D\n"
        for process in range(self.__numProcesses):
            allocations = ""
            for resource in range(self.__numResources):
                allocations += str(self.__allocated[process][resource]) + " "
            allocationMatrix = allocationMatrix + f"{process}: {allocations}" + "\n"


        maxMatrix = "   A B C D\n"
        for process in range(self.__numProcesses):
            worseCase = ""
            for resource in range(self.__numResources):
                worseCase += str(self.__maxNeed[process][resource]) + " "
            maxMatrix = maxMatrix + f"{process}: {worseCase}" + "\n"


        needMatrix = "   A B C D\n"
        for process in range(self.__numProcesses):
            resourcesNeeded = ""
            for resource in range(self.__numResources):
                resourcesNeeded += str(self.__currentNeed[process][resource]) + " "
            needMatrix = needMatrix + f"{process}: {resourcesNeeded}" + "\n"


        availablePre = " ".join(str(x) for x in self.__current[0])


        if self.__safeInitial:
            outputSafety = "THE SYSTEM IS IN A SAFE STATE!"
        else:
            outputSafety = "THE SYSTEM IS IN AN UNSAFE STATE!"

        requestVector = "1:" + " ".join(str(x) for x in self.__request)

        if self.__safeRequest:
            outputRequest = "THE REQUEST CAN BE GRANTED!"
        else:
            outputRequest = "THE REQUEST CANNOT BE GRANTED!"

        availablePost = " ".join(str(x) for x in self.__allocatedAfterRequest)

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


