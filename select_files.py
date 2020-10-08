"""
Script to selectively delete files from a folder.
"""

#==============
# Imports 
#==============

import os.path
import glob
from os.path import join
from collections import Counter


#==============
# Parameters
#==============


folder = join("corpora", "fra", "")
target = 3


#==============
# Functions 
#==============


def get_files(folder): 
    allfiles = {}
    for file in glob.glob(join(folder, "*txt")): 
        filename = os.path.basename(file)
        first,rest = filename.split("_")
        allfiles[filename] = first
    #print(allfiles)
    return allfiles


def select_files(folder, allfiles, target): 
    allauthors = []
    for item in allfiles.items(): 
        allauthors.append(item[1])
        #print(item[0])
    authorcounts = Counter(allauthors)
    selauthors = [item[0] for item in authorcounts.items() if item[1] >= target]
    print(selauthors)
    for item in allfiles.items(): 
        #print(item[1])
        if item[1] not in selauthors: 
            print(join(folder, item[0]))
            os.remove(join(folder, item[0]))
    
    
    

#==============
# Main 
#==============

def main(folder, target): 
    allfiles = get_files(folder)
    selection = select_files(folder, allfiles, target)   

main(folder, target)
