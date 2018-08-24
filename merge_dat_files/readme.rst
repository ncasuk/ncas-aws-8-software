=========================================================
COMBINE ALL CAMPBELL DAT FILES TO YEARLY FILES
=========================================================

This script will read in all .dat files in the source directory and combine them into one file. It will then sort them into date order and remove duplicate entries. 
It will then create a file per year in the output directory.

Usage
=====

To run the script you are required to have a source and output directory 

You will then need to copy or symlink campbell dat files into the source directory and run 

``./sort_dat_files``

this calls the combined.py and then the split_by_year.py
