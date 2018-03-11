#!usr/bin/env python
"""Executable file to run the PROJECT MANAGER program."""
import argparse
import yaml
import os
from projman import createStructure, otherOperations

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

def getYaml():
    """Gets yaml file"""
    if 'PROJMAN_TEMPLATES' in os.environ.keys():
        yaml_path = os.environ.get('PROJMAN_TEMPLATES')
    else:
        yaml_path = 'de.yaml'

    with open (yaml_path,'r') as ymlfile:
        try:
            yd = yaml.load(ymlfile)
        except yaml.YAMLError as er:
            print(er)
    return yd

def checkPath():
    """Checks if the path has provided and assigned to variable."""
    global proj_path
    if args.path:
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
        print("INVALID TYPE: Please enter the valid type as per the yaml.")
        exit()

def validations(yd):
    """Validates the input arguments for all the conditions"""
    checkPath()
    if args.SUBCMD not in ["list","create","delete","types","describe"]:
        print("INVALID SUBCMD: SUBCMD should be any one of create, delete, types, describe")
        exit()
    if args.SUBCMD=='list':
        if args.NAME:
            print("INVALID INPUT: For listing project name should not be passed")
            exit()
    else:
        if not args.NAME:
            print("INVALID INPUT: Project name is required to perfom",args.SUBCMD,"operation.")
            exit()
    if args.SUBCMD == 'types' and args.type:
        print("INVALID INPUT: For sub command 'types' there should not be -t argument present")
        exit()
    if args.SUBCMD in ['delete','types','describe']:
        if args.NAME not in os.listdir(proj_path):
            print("INVALID PROJECT: The given project is not present to perform sub command.")
            exit()
    if args.SUBCMD =='create' and args.NAME in os.listdir(proj_path):
        print("The given project is already exists, please provide diff project name.")
        exit()
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
        otherOperations.listProjects(proj_path,args.type)

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
            createStructure.structure(yaml_data,perm,proj_path)
        else:
            createStructure.structure(yaml_data,perm,proj_path)

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
        otherOperations.describe(proj_path)
