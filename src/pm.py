#!usr/bin/env python
"""Executable file to run the PROJECT MANAGER program."""
import argparse
import yaml
import os
import re
import sys
from projman import structure, otherOperations

#default project path and permission for file/folder structure
proj_path = ""
perm="0751"

#Defining arguments for the CLI
parser = argparse.ArgumentParser()
parser.add_argument("-t","--type",help="The type of the project created from a specific template.")
parser.add_argument("-p","--path",help="The base path to create the project. Default path: PROJMAN_LOCATION.")
parser.add_argument("SUBCMD", help="Enter the subcommnad to execute.")
parser.add_argument("NAME",nargs='?',help="Name of the project to perform subcommnad.")
args = parser.parse_args()

# def getYaml():
#     """Gets yaml file"""
#     if 'PROJMAN_TEMPLATES' in os.environ.keys():
#         yaml_path = os.environ.get('PROJMAN_TEMPLATES')
#     else:
#         yaml_path = 'de.yaml'
#
#     with open (yaml_path,'r') as ymlfile:
#         try:
#             yd = yaml.load(ymlfile)
#         except yaml.YAMLError as er:
#             sys.stderr.write(er)
#             raise SystemExit(4)
#     return yd

def getYaml():
    """Gets yaml file"""
    #Creates empty yaml file
    fn = 'inputDDIsunyl.yaml'
    with open(os.path.join(os.getcwd(),fn),'w') as yaml_file:
        pass
    # yaml_paths = os.environ.get("PROJMAN_TEMPLATES")
    yaml_paths ='/Users/sunilhn/Documents/python_learning/DDI_Hackathon/src:/Users/sunilhn/Documents/python_learning/skillenza'
    for path in yaml_paths.split(':'):
        try:
            for files in os.listdir(path):
                if re.search("\.yaml",files) and files != fn:
                    #Reading the yaml data
                    with open(os.path.join(path,files),'r') as yaml_file:
                        yd = yaml_file.read()
                    #Writing the yaml data to temperorary yaml file created
                    with open(os.path.join(os.getcwd(),fn),'a') as yaml_file:
                        yaml_file.write(yd)
        except FileNotFoundError:
            pass

    with open(os.path.join(os.getcwd(),fn),'r') as ymlfile:
        try:
            yd = yaml.load(ymlfile)
        except yaml.YAMLError as er:
            sys.stderr.write(er)
            raise SystemExit(4)
    return yd

def checkPath():
    """Checks if the path has provided and assigned to variable."""
    global proj_path
    if args.path:
        if args.SUBCMD=='describe':
            sys.stderr.write("INVALID INPUT: path is not required to perfom {} operation\n".format(args.SUBCMD))
            raise SystemExit(4)
        else:
            proj_path = args.path
    else:
        if 'PROJMAN_LOCATION' in os.environ.keys():
            proj_path = os.environ.get('PROJMAN_LOCATION')
        else:
            proj_path = os.path.join(os.path.dirname(os.getcwd()),"PROJECTS")

def checkType(yaml_data):
    """Validation for the given type argument."""
    flag = 0
    for types in yaml_data:
        if args.type in types['value'].keys():
            flag=1
            break
    if flag==0:
        sys.stderr.write("INVALID TYPE: Please enter the valid type as per the yaml.")
        raise SystemExit(4)

def validations(yd):
    """Validates the input arguments for all the conditions"""
    checkPath()
    if args.SUBCMD not in ["list","create","delete","types","describe"]:
        sys.stderr.write("INVALID SUBCMD: SUBCMD should be any one of create, delete, types, describe")
        raise SystemExit(4)
    if args.SUBCMD=='list' or args.SUBCMD=='describe':
        if args.NAME:
            sys.stderr.write("INVALID INPUT: For listing and describe project name should not be passed")
            raise SystemExit(4)
    else:
        if not args.NAME:
            sys.stderr.write("INVALID INPUT: Project name is required to perfom {} operation\n".format(args.SUBCMD))
            raise SystemExit(4)
    if args.SUBCMD=='describe' and args.type:
        sys.stderr.write("INVALID INPUT: types is not required to perfom {} operation\n".format(args.SUBCMD))
        raise SystemExit(4)
    if args.SUBCMD == 'types' and args.type:
        sys.stderr.write("INVALID INPUT: For sub command 'types' there should not be -t argument present")
        raise SystemExit(4)
    if args.SUBCMD in ['delete','types']:
        if args.NAME not in os.listdir(proj_path):
            sys.stderr.write("INVALID PROJECT: The given project is not present to perform sub command.")
            raise SystemExit(4)
    if args.SUBCMD =='create' and args.NAME in os.listdir(proj_path):
        sys.stderr.write("The given project is already exists, please provide diff project name.")
        raise SystemExit(4)
    if args.type:
        checkType(yd)

if __name__ == '__main__':
    yaml_data = getYaml()
    validations(yaml_data)

    #Setting the given project name to the path
    if args.NAME:
        proj_path = os.path.join(proj_path,args.NAME)

    #Calling function for list sub command
    if args.SUBCMD == 'list':
        otherOperations.listProjects(yaml_data,proj_path,args.type)

    #Calling function for create sub command
    if args.SUBCMD == 'create':
        #Creating project folder with the given project name
        os.mkdir(proj_path)
        if args.type:
            pass
            for item in yaml_data:
                if args.type in item['value'].keys():
                    per = item['permission']
                    yaml_data = item['value']
                    break
            structure.structure(yaml_data,perm,args.SUBCMD,proj_path)
        else:
            structure.structure(yaml_data,perm,args.SUBCMD,proj_path)

    #Calling function for delete sub command
    if args.SUBCMD == 'delete':
        if args.type:
            otherOperations.deleteProject(proj_path,args.type)
        else:
            otherOperations.deleteProject(proj_path)

    #Calling function for types sub command
    if args.SUBCMD == 'types':
        otherOperations.listTypes(proj_path)

    #Calling function for describe sub command
    if args.SUBCMD == 'describe':
        # otherOperations.describe(proj_path)
        structure.structure(yaml_data,perm,args.SUBCMD)
