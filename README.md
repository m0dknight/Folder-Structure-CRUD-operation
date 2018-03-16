<!-- Documentation for the PROJECT MANAGER project. -->
The challenging part in the given problem statement is to parse the yaml data and loop through the each individual element in the yaml data. So started first writing program for the create operation since all other operations like lists, types etc don't need to iterate through inner most element.

Created structure.py file and started writing structure function inside it to loop through the inner most elements.
Initially tried to wrote whole iterate function in structure, it was getting complex. Observing the yaml structure came to know yaml data will have lists and dictionaries inside it. So in structure function, written a condition to check whether the present element is list or dictionary based on that passed that element to separate lis or dic function to iterate the element through the respective data.

At this point I was able to iterate through all the elements in yaml data successfully when to do create operation was still pending. On observing the yaml data it was pretty clear that we need to create folder/file when the dictionary with keyword 'value' has value which is not of dictionary data type and when the dictionary with keyword other than 'permission' and 'value'.

Created Operation function to do the create or describe operation.
In case of create, calling checkFolder function to check whether the provided name is of file type or not. If its file calling createFile function to create the file else creating the folder with that name.
Also created getOctCode function to returns the octal number for the given string to set permissions for the folder/file since the default permission from yaml was not supporting in python3 interpreter.
In case of describe, printing the structure by finding the level of folder structure.

Since the structure.py already had so many functions I've created another file otherOperations.py to perform the remaining operations.

For list operation created listProjects function to list all the projects at the given path with the optional type.

For delete operation created deleteProject function to delete the project and its folder structure at the given path with the optional type.

For types operation created listTypes function to list all the types created at the given project path.
