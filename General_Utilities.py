#!/usr/bin/python
'''
Created on 11-Nov-2016

@author: aklab
'''
#!/usr/bin/python
import os, sys

def check_folder(folder_to_create):
    if(os.path.isdir(folder_to_create)==False):
        mkdir="mkdir %s"%(folder_to_create)
        os.system(mkdir)

def check_file(file_to_check):
    if(os.path.isfile(file_to_check)==False):
        #mkdir="mkdir %s"%(folder_to_create)
        #os.system(mkdir)
        print "Could not find file %s. Exiting"%(file_to_check)
        exit()
