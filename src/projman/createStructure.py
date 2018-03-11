"""
Has the functions to create the folder structures as per the given yaml file.
"""

import os
import re

def checkFolder(name):
    """Checks if the given name is folder or files and returns True if its folder."""
    if re.search("\.",name):
        return False
    else:
        return True

def getOctCode(per):
    """Converts the given string to octal number."""
    peroct = int(per,8)
    return peroct

def createFile(path,name,per):
    """Creates the empty file name at the given path with the permissions per."""
    with open (os.path.join(path,name),'a'):
        pass
    try:
        os.chmod(os.path.join(path,name),per)
    except:
        os.chmod(os.path.join(path,name),getOctCode(per))

def operation(path,name,per):
    """Creates the folder name at path with the permission per if the given name is folder else calls the createFile function to create the file."""
    if checkFolder(name):
        try:
            os.mkdir(os.path.join(path,name),per)
        except:
            os.mkdir(os.path.join(path,name),getOctCode(per))
    else:
        createFile(path,name,per)

def lis(folders,per,path):
    """Iterates the yaml data through the provided folders list and pass the next data to structure function."""
    for items in folders:
        structure(items,per,path)

def dic(folders,per,path):
    """Iterates the yaml data through the provided folders dictionary and pass the next data to structure function. Also calls operation function to create file/folder"""
    for apps in folders.keys():
        if apps=='permission':
            per=folders[apps]
        elif apps=='value':
            if(type(folders[apps]) != type({})):
                operation(path,folders[apps],per)
            else:
                structure(folders[apps],per,path)
        else:
            operation(path,apps,per)
            path = os.path.join(path,apps)
            structure(folders[apps],per,path)

def structure(folders,per,path):
    """Function to create the structure based on the yaml data at path."""
    if (type(folders) == type([])):
        lis(folders,per,path)
    elif (type(folders) == type({})):
        dic(folders,per,path)
