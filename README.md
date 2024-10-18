<h1>Project 4 - Bankers Algorithm </h1>
  by: Xander Palermo

<h2>Background </h2>
This program is coded using python.

In my solution for this project, I created a main function located within banker.py that creates an ProcessManager object that handles the computation and formating required for this project


<h2>Required Files </h2>
Place banker.py , ProcessManager.py , and s1.txt into the same directory (preferably on the lovelace server)

(you can also you the git clone command for this repository, and that will load all the files necessary)

https://github.com/aPalermooo/CSC360-ProjectFour.BankersAlgorithm

<h2>Running the program</h2>
The following command generates a Log file:

> python3 banker.py
>


The program defaults to searching for s1.txt when no parameters are given


However the program can take attributes to read a different file, if desired

> python3 banker.py s1.txt
> 
> python3 banker.py s2.txt

..and so on

<h2>Checking output</h2>
The program will generate a new log file upon running in the format of a txt file, located in the same directory as banker.py

This can be accessed like any other text file, but throughout development, I've been checking it using

>vim bankerLog.txt
>

If there already exists a bankerLog.txt when the program runs, it will attempt to delete it so it can create a new one under the same name
