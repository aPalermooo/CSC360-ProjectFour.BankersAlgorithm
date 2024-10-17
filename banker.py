def readFile(filename):
    # Open File
    file = open(filename, 'r')

    # Retrieve parameters
    numProcesses = file.readline()
    file.readline()
    numResources = file.readline()

    numProcesses = int(numProcesses)
    numResources = int(numResources)

    print(numResources)
    print(numProcesses)

    file.readline()

    # Retrieve allocation matrix
    allocation = []
    for i in range(numProcesses):
        allocation.append(file.readline())
        allocation[i] = allocation[i].split()
        allocation[i] = list(map(int, allocation[i]))

    print(allocation)
    print(type(allocation[0][0]))

    file.readline()

    # Retrieve max matrix
    max = []
    for i in range(numProcesses):
        max.append(file.readline())
        max[i] = max[i].split()
        max[i] = list(map(int, max[i]))

    print(max)
    print(type(max[0][0]))

    # Retrieve current



def main():
    readFile("s1.txt")
    print("Done")

main()