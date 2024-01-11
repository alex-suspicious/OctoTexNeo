import os
import sys
import random
import asyncio

MEIPASS = ""
if( hasattr(sys,"_MEIPASS") ):
    MEIPASS = sys._MEIPASS + "/"

container = {}

def findAny( dir = "" ):
    dir = MEIPASS + dir
    files = []
    listdir = os.listdir( dir )

    for y in range(0,len(listdir)):
        file = listdir[y]
        if( "." not in file ):
            continue
           
        files.append( dir + "/" + file )

    return files;

def findDirectories( dir = "" ):
    dir = MEIPASS + dir
    directories = []

    listdir = os.listdir( dir )
    for x in range(0,len(listdir)):
        directory = listdir[x]
        if( "." in directory ):
            continue
            
        directories.append( dir + "/" + directory )
        directoriesTemp = findDirectories( dir + "/" + directory )
        directories = directories + directoriesTemp

    return directories;

def findPyFiles( dir = "" ):
    dir = MEIPASS + dir
    directories = findDirectories( dir )
    files = []

    for x in range(0,len(directories)):
        directory = directories[x]
        listdir = os.listdir( directory )

        for y in range(0,len(listdir)):
            file = listdir[y]
            if( "." not in file ):
                continue
               
            files.append( directory + "/" + file )

    return files;


def load():
    files = findAny("objects")
    print("\nLoading Objects...")
    globalsz = globals()

    savedSubdir = ""
    for x in range(0,len(files)):
        file = files[x]
        path = file.replace("objects","").split("/")[-1].replace(".py","")
        

        code_file = open(file , "r", encoding="utf-8")
        code = code_file.read()
        code_file.close()
        localz = locals()

        #if( savedSubdir != subdir ):
        #    savedSubdir = subdir
            #print( f"┌────────  {subdir}")

        print( "┌──────────────────────────────────")
        print( "│ +        " + path )


        try:
            exec( code , globalsz, localz)
        except SyntaxError as err:
            exit(err)


        tempClass = localz[path]
        variablesNeeded = []

        if( "rel_url.query" in code ):
            lines = code.split("\n")
            for y in range(len(lines)):
                if( "rel_url.query" in lines[y] ):
                    lines[y] = lines[y].replace("rel_url.query","<---->").replace("]","<---->")


            variables = "\n".join(lines).split("<---->")
            for y in range( 1, len(variables), 2 ):
                tempVar = variables[y].replace("'","").replace("\"","").replace("[","")
                variablesNeeded.append(tempVar)

        tempObject = tempClass()
        container[path] = tempObject

        #container.api_dir.append( path )
        #container.api_vars.append( variablesNeeded )
            
        #if( "Cron" in subdir_array ):
        #api(len(container.api)-1, filename, localz)

    print("└──────────────────────────────────")

