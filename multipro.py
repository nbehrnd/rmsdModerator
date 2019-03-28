#!/usr/bin/env python3
# name:   multipro.py
# author: nbehrnd@yahoo.com
# edit:   2019-Mar-27

"""
Engage calculate_rmsd.py simultaenously on many *.xyz and multiple CPUs

Allow the concurrent, parallel run of calculate_rmsd.py.  Assumes
Python3 as the engine.  To perform well, this script and relayed
calculate_rmsd.py must reside in the same directory -- this proof
of concept does not consider an os.walk.  Launch by

python3 multipro.py
"""

import os
import sys
import subprocess as sub
from concurrent import futures
import concurrent.futures
from multiprocessing import Pool as ThreadPool
import time
fileRegister = []
testRegister = []


def fileSearch():
    """
    detects the *.xyz files
    """
    for file in os.listdir("."):
        if file.endswith(".xyz"):
            fileRegister.append(file)
    fileRegister.sort()
    return fileRegister


def constructCommand():
    """
    builds the commands eventually relayed to calculate_rmsd.py
    """
    while len(fileRegister) > 1:
        for entry in fileRegister[1:]:
            m0 = str(fileRegister[0])
            m1 = str(entry)

            command = str("python3 calculate_rmsd.py") + str(" ") +\
                      str(m0) + str(" ") + str(m1) +\
                      str(" --reorder --use-reflections")

            testRegister.append(str(command))
        del fileRegister[0]
    return testRegister


fileSearch()
constructCommand()


#def testing(data=""):
#    """
#    relay the test to calculate_rmsd.py
#
#    This is the GIL limited, linear / single CPU core approach.
#    """
#    for entry in testRegister:
#        time.sleep(0.1)
#        print(entry)
#        sub.call(entry, shell=True)


def test(testRegister):
    """
    relay the test to multiple CPU instances of calculate_rmsd.py
    """
    print(testRegister)
    sub.call(testRegister, shell=True)
pool = ThreadPool(3)  # number of tests to be performed in parallel
pool.starmap(test, zip(testRegister))
pool.close() 
pool.join()

sys.exit()
