#!/usr/bin/python
#Version V1.0
#create a list of dat files in current directory

import os
import glob
import sys

# This is the path where you want to search
inpath = os.path.abspath(sys.argv[1])

open('combined.csv', 'w').close()
with open ("combined.csv" , 'wt+') as nf:

    print(inpath)
    for infile in os.listdir(inpath):
        if infile.endswith(".dat"):
            print(os.path.join(inpath, infile))
            with open(os.path.join(inpath, infile),'rb') as readfile:
                #skip four lines
                for _ in range(4):
                    next(readfile)
                #write remainder
                for line in readfile:
                    nf.write(str(line))
            readfile.close()



