import sys
import time
from core.Integer_Helper import CheckWhetherStringIsIntegerOrFloat as CIF
from core.programs import Program
import interface.CreateTex as CreateTex
import Reload
from core.evolution import *
from core.config import *
import core.nodes as Node

    
def Display(Input_Param:list[dict[str,int|float]],Output_Param:list[int|float],Predict_Param:list[int|float],
            Error:int|float,GenNum:int,ProgramNum:int) -> None:
    """
    Display The Program's Stats in a Pseudo-Tabular Format
    """
    print("-"*len("Sr No.    Input Data        Required Output        Predicted Output"))
    print(f"Generation: {GenNum}   Program: {ProgramNum}")
    for i,_ in enumerate(Output_Param):
        if i==0:
            print("Sr No.\tInput Data\t\tRequired Output\t\tPredicted Output")
        InputList: list[int|float] = list(Input_Param[i].values())
        print(f"{i+1}.\t{InputList}\t\t\t\t{Output_Param[i]}\t\t{Predict_Param[i]}")
    print("-"*len("Sr No.    Input Data        Required Output        Predicted Output"))
    print(f"The Total Error is {Error}")

def run_cli(argv:list[str]):
    if not len(argv)>1:         #Check If Sufficient Arguments
        print(f'''Invalid Usage
            Usage: python {argv[0]} <filename>.csv
                   python {argv[0]} -r <filename>.reload
            
            The Following Options can be Specified:
            --gui: Launch GUI Mode  

            --CONFIG: Path to a yaml Config file to Set Parameters

            --REPORT: Path to Results pdf file (Without Extension)
            --MAXDEPTH:  Max Depth of Program tree
            --VERBOSE or -v: For verbose Output
            --RELOAD or -R: For Saving Data For Reload
            --XOP: Crossover probability
            --MAXXO: Max Crossover Per Generation
            --MUTP: Mutation probability
            --MAXMUT: Max Mutation Per Generation
            --NEWP: New Introduction Probability
            --MAXNEW: Max New Introduction Per Generation
            --GENSIZE: Size of Each Generation
            --MAXGEN: Maximum Generation to be Explored
            --FSET: Function Set to be Used
              Include Following Characters in FSET for following Operations
              E for Exponentiation
              L for Logrithm and Exp 
              P for Square and Cube
              R for Square Root and Cube Root
              T for Sin, Cos and Tan''')
        exit()

    #Initialize Nodes
    start:float = time.perf_counter()
    HyperParas,MAX_DEPTH,GEN_SIZE,MAX_GEN,RELOADPROGRESS,Master,Source_File,PDFFILE,FSET,Total_Error,Min_Error,Terminal_Set,Current_Gen=Initialize(argv) #Get Hyper Parameters

    InputData,OutputData=FormatCsv(Source_File)  #Get Input and Output Data
    
    Function_Set: list[Node.Node] =[Node.Plus,Node.Minus,Node.Mul,Node.Divide]   #Initialize Function Set
    if "E" in FSET or "e" in FSET: Function_Set.append(Node.Power)
    if "P" in FSET or "p" in FSET: 
        Function_Set.append(Node.Square)
        Function_Set.append(Node.Cube)
    if "R" in FSET or "r" in FSET:
        Function_Set.append(Node.Square_Root)
        Function_Set.append(Node.Cube_Root)
    if "T" in FSET or "t" in FSET: 
        Function_Set.append(Node.Sin) 
        Function_Set.append(Node.Cos) 
        Function_Set.append(Node.Tan)
    if "L" in FSET or "l" in FSET:
        Function_Set.append(Node.Exp)
        Function_Set.append(Node.Log)
    if not Terminal_Set:
        Terminal_Set: list[Node.Node] = [Node.Node("Const")]  #Initialize Terminal Set
        for i in range(1,len(InputData[0])+1):
            Terminal_Set.append(Node.Node(f"var{i}"))    #Add Required variables
        
    if not Master:
        Check:str =input("Confirm(Enter to Continue,else Stop)?")   #Confirm Parameters Values
        if Check!="": exit()

    Union_List:list[Node.Node] = Function_Set + Terminal_Set  #Set of All Nodes
    if not RELOADPROGRESS: Current_Gen:list[Program] = [Program.CreateRandom(MAX_DEPTH,Terminal_Set,Union_List) for _ in range(GEN_SIZE)] #First random Generation
    
    for i in range(MAX_GEN):Current_Gen,Total_Error,Min_Error=Iterate(ThisGen=Current_Gen,GenNum=i,InputData=InputData,OutputData=OutputData,Total_Error=Total_Error,Min_Error=Min_Error,HyperParas=HyperParas,Terminal_Set=Terminal_Set,Union_List=Union_List,Display=Display)   #Main Generation Loop
    Current_Gen,Total_Error,Min_Error=Iterate(ThisGen=Current_Gen,GenNum=i,InputData=InputData,OutputData=OutputData,Total_Error=Total_Error,Min_Error=Min_Error,HyperParas=HyperParas,Terminal_Set=Terminal_Set,Union_List=Union_List,Display=Display)  #Display Last Generation
    Current_Gen.sort(key= lambda x:x.error) #Sort Last Generation By Error.
    
    
    end:float = time.perf_counter()
    print(f"The Program With Minimum Error is:\n{Current_Gen[0]}\nWith the Total Error of {Current_Gen[0].error}\nTime Taken:{end-start:.4f} seconds")  #Print Final Result

    #Assemble Data for Report
    CodeList:list[list[Node.Node]] = []
    ErrorList:list[int|float] = []
    BestProgram:list[Program] = []
    i = 0
    for i in range(GEN_SIZE):
        if Current_Gen[i].code not in CodeList:
            CodeList.append(Current_Gen[i].code)
            ErrorList.append(Current_Gen[i].error)
            BestProgram.append(Current_Gen[i])
        i += 1
    Total_Error.pop()
    Min_Error.pop()
    print("Saving Configuration For Reload.")
    Reload.save(InputFile=Source_File,HParams=HyperParas,Min_Error=Min_Error,Total_Error=Total_Error,lastGen=Current_Gen)
    print("Generating Report.")
    CreateTex.Create(filepath=PDFFILE,equation=CodeList,NumberOfCode=GEN_SIZE,  
                     TotalError=Total_Error,MinError=Min_Error,Input=[list(i.values()) for i in InputData],Output=OutputData,
                     Predict=[[ProgramX.Compute(Operand=Ops) for Ops in InputData] for ProgramX in BestProgram],ErrorList=ErrorList,HParams=HyperParas) #Create Report
