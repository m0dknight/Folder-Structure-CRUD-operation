"""
Has functions to do the operations like list,delete,types and describe projects.
"""

import os
import shutil


def listTypes(path):
    """Lists the types created for the given project path."""
    types = os.listdir(path)
    if types:
        for name in types:
            print(name)
    else:
        print("No types created for the given project")

def listProjects(path,ty=None):
    """Lists all the projects at the given path with the optional type ty."""
    projects = []
    if ty:
        for project in os.listdir(path):
            for type in os.listdir(os.path.join(path,project)):
                if type == ty:
                    projects.append(project)
                    break
    else:
        projects = os.listdir(path)
    if projects:
        for p in projects:
            print(p)
    else:
        print("None of the projects have the type :",ty)

def describe(pname):
    """Discribes the folder structures at the given project path pname."""
    for root, dirs, files in os.walk(pname):
        level = root.replace(pname, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))

def deleteProject(path,ty=None):
    """Deletes the project and its folder structure at the given path for the optional type ty."""
    if ty:
        path = os.path.join(path,ty)
    try:
        shutil.rmtree(path)
        print("deleted")
    except:
        print("Mentioned type is not present in the given project to delete.")
