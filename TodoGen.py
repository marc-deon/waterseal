#!/usr/bin/env python3

from os import listdir
from os.path import isfile, join
from sys import argv

def Main(argv):
    if len(argv) < 2:
        print("Itterate non-recursively through files in given folders and print TODO and FIXMEs.\
            -x can be repeated any number of times, and must specify files, not directories.\
            -X will exclude extensions (case insensitive)\
            \n\nUsage: TodoGen.py [-x fileToExclude] [-X extensionToExclude] (folderPaths)\n\te.g. TodoGen.py -x todo.txt -X png src include")
        return

    excludes = []
    extensionExcludes = []

    while argv[1] == "-x" or argv[1] == "-X":

        if argv[1] == "-x":
            # If the path to exclude wasn't specified as absolute or relative, assume relative
            if (argv[2][0] != '/') and (argv[2][0:2] != "./"):
                argv[2] = "./" + argv[2]

            excludes.append(argv[2])
        
        elif argv[1] == "-X":
            extensionExcludes.append(argv[2])

        argv = argv[0:1] + argv[3:]
    
    extensionExcludes = tuple(extensionExcludes)

    for path in argv[1:]:

        onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
        onlyfiles = [f for f in onlyfiles if not f.endswith(extensionExcludes)]
        paths = [join(path, fullpath) for fullpath in onlyfiles]
        
        firstFile = True
        for fullpath in paths:
            
            if fullpath in excludes:
                continue

            with open(fullpath, 'r') as f:
                lineNum = 0
                lastPrinted = -1
                line = None
                # try:
                try:
                    line = f.readline()
                except UnicodeDecodeError:
                    print(f"Skipping reading file [{fullpath}]. Is it a text file?")
                    continue
                    
                while line:
                    lineNum+=1
                    if "TODO:" in line or "FIXME:" in line:
                        if lastPrinted < 0:
                            #  Print filename only once per file; only seperate with newlines after the first file
                            print(("" if firstFile else "\n") + fullpath.strip(" \t/.;#"), ":", sep="")
                            firstFile = False
                        # Strip leading whitespace and punctuation of line
                        print(f"  {lineNum:<6}", line.strip(" \n\t/.;#"), sep="")
                        lastPrinted = lineNum
                    line = f.readline()


Main(argv)
