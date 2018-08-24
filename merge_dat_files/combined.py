#!/usr/bin/python
#Version V1.0
#create a list of dat files in current directory

import os
import glob

# This is the path where you want to search
path = os.path.abspath('./source')

open('combined.csv', 'w').close()
nf = open ("combined.csv" , 'w+')

print path
for file in os.listdir(path):
    if file.endswith(".dat"):
        print(os.path.join("./source", file))
        file = open (os.path.join("./source", file))
        file_contents = file.readlines()
        nf.write(''.join(file_contents[4:]))
        file.close()



