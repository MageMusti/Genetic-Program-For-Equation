<<<<<<< HEAD
from collections.abc import Generator


def save(InputFile:str,HParams:dict[str,int|float|bool|str],Total_Error:list[float],Min_Error:list[float],lastGen:list) -> None:
    ReloadFile = HParams["RESULT"] + ".reload" # type: ignore
    with open(ReloadFile,"w") as Reloading:
        Reloading.write(f"Input File: {InputFile}\n")
        Reloading.write(f"Output File: {HParams["RESULT"]}")
        Reloading.write(f'''
Maximum Depth = {HParams["MAXDEPTH"]}
Size of Generation = {HParams["GENSIZE"]}
Maximum Number of Generation = {HParams["MAXGEN"]}
Crossover Probability = {HParams["XOP"]}
Maximum Crossover = {HParams["MAXXO"]}
Mutation Probability = {HParams["MUTP"]}    
Maximum Mutation = {HParams["MAXMUT"]}
New Introduction Probability = {HParams["NEWP"]}
Maximum New Introduction = {HParams["MAXNEW"]}
Verbose = {HParams["VERBOSE"]}
Function Set = {HParams["FSET"]}
''')
        Reloading.write(str(Total_Error)[1:-1] + "\n")
        Reloading.write(str(Min_Error)[1:-1] + '\n')
        for Program in lastGen: Reloading.write(str(Program) + "\n")


def FileReader(ReloadFile:str) -> Generator[str,None,None]:
    with open(ReloadFile,"r") as Reloading:
        NextLine = "Not a Null Thing"
        while(NextLine!=""):
            NextLine = Reloading.readline()
            yield NextLine


def load(ReloadFile:str) -> tuple[str,str,int,int,int,float,int,float,int,float,int,bool,str,list[float],list[float],list[str]]:
    ReadingInProgress: Generator[str,None,None] = FileReader(ReloadFile)
    InputFile:str = next(ReadingInProgress)[len("Input File: "):-1:]                      #1
    OutputFile:str = next(ReadingInProgress)[len("Output File: "):-1:]                    #2
    MAXDEPTH:int = int(next(ReadingInProgress)[len("Maximum Depth = ")::])              #3
    GENSIZE:int = int(next(ReadingInProgress)[len("Size of Generation = ")::])          #4
    MAXGEN:int = int(next(ReadingInProgress)[len("Maximum Number of Generation = ")::]) #5
    XOP:float = float(next(ReadingInProgress)[len("Crossover Probability = ")::])       #6
    MAX_XO:int = int(next(ReadingInProgress)[len("Maximum Crossover = ")::])            #7
    MUTP:float = float(next(ReadingInProgress)[len("Mutation Probability = ")::])       #8
    MAXMUT:int = int(next(ReadingInProgress)[len("Maximum Mutation = ")::])             #9
    NEWP:float = float(next(ReadingInProgress)[len("New Introduction Probability = ")::])#10
    MAX_NEW:int = int(next(ReadingInProgress)[len("Maximum New Introduction = ")::])    #11
    Verbose:bool = False if ((AnnoyingString:=(next(ReadingInProgress)[len("Verbose = "):-1:]))=="False") else True #12
    FSET:str = next(ReadingInProgress)[len("Function Set = "):-1:]                        #13
    Total_Error:list[float] = []
    for Index,Error in enumerate(next(ReadingInProgress).split(",")):                   #14
        if Index: Total_Error.append(float(Error[1:]))
        else: Total_Error.append(float(Error))
    Min_Error:list[float] = []
    for Index,Error in enumerate(next(ReadingInProgress).split(",")):                   #15
        if Index: Min_Error.append(float(Error[1:]))
        else: Min_Error.append(float(Error))
    Current_Gen:list[str] = []
    for i in range(GENSIZE):
        Current_Gen.append(next(ReadingInProgress)[:-1])
    return InputFile,OutputFile,MAXDEPTH,GENSIZE,MAXGEN,XOP,MAX_XO,MUTP,MAXMUT,NEWP,MAX_NEW,Verbose,FSET,Total_Error,Min_Error,Current_Gen


=======
from collections.abc import Generator
from typing import Any

import numpy as np


def save(InputFile:str,HParams:dict[str,int|float|bool|str],Total_Error:list[float],Min_Error:list[float],lastGen:list[Any],ReloadFile:str|None = None) -> None:
    """
    Saves the Progress of Genetic Program in a .reload File
    """
    if not ReloadFile: ReloadFile:str = str(HParams["RESULT"])
    with open(ReloadFile+".reload","w") as Reloading:
        Reloading.write(f"Input File: {InputFile}\n")
        Reloading.write(f"Output File: {HParams["RESULT"]}")
        Reloading.write(f'''
Maximum Depth = {HParams["MAXDEPTH"]}
Size of Generation = {HParams["GENSIZE"]}
Maximum Number of Generation = {HParams["MAXGEN"]}
Crossover Probability = {HParams["XOP"]}
Maximum Crossover = {HParams["MAXXO"]}
Mutation Probability = {HParams["MUTP"]}    
Maximum Mutation = {HParams["MAXMUT"]}
New Introduction Probability = {HParams["NEWP"]}
Maximum New Introduction = {HParams["MAXNEW"]}
Verbose = {HParams["VERBOSE"]}
Function Set = {HParams["FSET"]}
''')
        Reloading.write(str(Total_Error)[1:-1] + "\n")
        Reloading.write(str(Min_Error)[1:-1] + '\n')
        for Program in lastGen: Reloading.write(str(Program) + "\n")


def FileReader(ReloadFile:str) -> Generator[str,None,None]:
    """
    Returns a Generator for .reload File to  read File line by line.
    """
    with open(ReloadFile,"r") as Reloading:
        NextLine = "Not a Null Thing"
        while(NextLine!=""):
            NextLine = Reloading.readline()
            yield NextLine


def load(ReloadFile:str) -> tuple[str,str,int,int,int,float,int,float,int,float,int,bool,str,np.ndarray,np.ndarray,list[str]]:
    """
    Loads Data form the .reload File.
    """
    ReadingInProgress: Generator[str,None,None] = FileReader(ReloadFile)
    InputFile:str = next(ReadingInProgress)[len("Input File: "):-1:]                      #1
    OutputFile:str = next(ReadingInProgress)[len("Output File: "):-1:]                    #2
    MAXDEPTH:int = int(next(ReadingInProgress)[len("Maximum Depth = ")::])              #3
    GENSIZE:int = int(next(ReadingInProgress)[len("Size of Generation = ")::])          #4
    MAXGEN:int = int(next(ReadingInProgress)[len("Maximum Number of Generation = ")::]) #5
    XOP:float = float(next(ReadingInProgress)[len("Crossover Probability = ")::])       #6
    MAX_XO:int = int(next(ReadingInProgress)[len("Maximum Crossover = ")::])            #7
    MUTP:float = float(next(ReadingInProgress)[len("Mutation Probability = ")::])       #8
    MAXMUT:int = int(next(ReadingInProgress)[len("Maximum Mutation = ")::])             #9
    NEWP:float = float(next(ReadingInProgress)[len("New Introduction Probability = ")::])#10
    MAX_NEW:int = int(next(ReadingInProgress)[len("Maximum New Introduction = ")::])    #11
    Verbose:bool = False if ((next(ReadingInProgress)[len("Verbose = "):-1:])=="False") else True #12
    FSET:str = next(ReadingInProgress)[len("Function Set = "):-1:]                        #13
    Total_Error_List:list[str] = next(ReadingInProgress).split(",")
    Total_Error:np.ndarray = np.empty(len(Total_Error_List),dtype=np.float64)
    for Index,Error in enumerate(Total_Error_List):                   #14
        if Index: Total_Error[Index]=(float(Error[1:]))
        else: Total_Error[Index]=(float(Error))
    Min_Error_List:list[str] =next(ReadingInProgress).split(",")
    Min_Error:np.ndarray = np.empty(len(Min_Error_List),dtype=np.float64)
    for Index,Error in enumerate(Min_Error_List):                   #15
        if Index: Min_Error[Index]=(float(Error[1:]))
        else: Min_Error[Index]=(float(Error))
    Current_Gen:list[str] = []
    for _ in range(GENSIZE):
        Current_Gen.append(next(ReadingInProgress)[:-1])
    return InputFile,OutputFile,MAXDEPTH,GENSIZE,MAXGEN,XOP,MAX_XO,MUTP,MAXMUT,NEWP,MAX_NEW,Verbose,FSET,Total_Error,Min_Error,Current_Gen
>>>>>>> e7c4d3f (Added GUI (--gui) and Updated Documentation)
