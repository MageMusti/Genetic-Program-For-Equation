import math
import random
import os
from time import sleep
from typing import Any, Callable
from core.programs import Program
from core.nodes import Node
import interface.CreateTex as CreateTex

def Softmax(Input: list[Program],GEN_SIZE:int) -> None:
    """
    Sets Probability of Selection For Programs in Given List
    Based on the Error of Each Program Using Softmax.
    """
    #exponentForm: list[float] = [math.exp(GEN_SIZE/Code.error) for Code in Input]
    exponentForm: list[float] = []
    for Code in Input:
        try: exponentForm.append(math.exp(GEN_SIZE/Code.error))
        except OverflowError: 
            exponentForm.append(1000000)
            #input(f"Too much Big Number\n{err}")
    Sum: float = sum(exponentForm)
    for i,Code in enumerate(Input):
        Code.prob = exponentForm[i]/Sum

def Selection(Generation:list[Program],GEN_SIZE:int) -> list[Program]:
    """
    Based On Error of Programs in Given Generation
    Return New Generation Using Roulette Wheel Selection
    """
    Generation.sort(key=lambda x:x.error)
    Softmax(Generation,GEN_SIZE)
    NewGeneration:list[Program] = []
    NewGeneration.append(Generation[0])
    NewGeneration.append(Generation[0])
    for _ in range(GEN_SIZE-2):
        try: Selected_Program:Program = random.choices(Generation,k=1,weights=[X.prob for X in Generation])[0]
        except ValueError: Selected_Program:Program = random.choice(Generation)
        if Selected_Program.prob > 0.5: Selected_Program.prob -=0.5
        else: Selected_Program.prob = 0
        NewGeneration.append(Selected_Program)
    return NewGeneration

def PickSubTree(Code:Program,FirstIndex:int) -> int:
    """
    Pick a Sub-Tree of a Given Program Code
    Starting at FirstIndex Given. 
    Returns the LastIndex of That Sub-Tree
    """
    LastIndex:int = 0
    if not Code.code[FirstIndex].Terminal:
        return FirstIndex
    else:
        LastIndex = FirstIndex
        for _ in range(Code.code[FirstIndex].Terminal):
            LastIndex=PickSubTree(Code=Code,FirstIndex=(LastIndex+1))
    return LastIndex

def Xover(FirstProgram:Program,SecondProgram:Program,VERBOSE:bool) -> tuple[Program,Program]:
    """
    Does A random Crossover Between Two Given Programs.
    Returns New Programs in the Same Order as Given to Function
    """
    if VERBOSE:print("A Crossover is Observed.")
    Fp = Program(Code=FirstProgram.code)
    Sp = Program(Code=SecondProgram.code)
    FP_start:int = random.randint(a=0,b=(len(Fp.code)-1))
    SP_start:int = random.randint(a=0,b=(len(Sp.code)-1))
    FP_Last:int = PickSubTree(Code=Fp,FirstIndex=FP_start)
    SP_Last:int = PickSubTree(Code=Sp,FirstIndex=SP_start)
    FirstList:list[Node.Node] = Fp.code[FP_start:FP_Last+1]
    SecondList:list[Node.Node] = Sp.code[SP_start:SP_Last+1]
    Fp.code[FP_start:FP_Last+1] = SecondList
    Sp.code[SP_start:SP_Last+1] = FirstList
    return (Fp,Sp)

def Mutation(OgProgram:Program,Terminal_Set:list[Node],Union_List:list[Node],MAX_DEPTH:int,VERBOSE:bool) -> Program:
    """
    Introduces a Random Mutation in the Given
    Program. Returns Mutated Program.
    """
    if VERBOSE:print("A Mutation is Observed")
    OgCode:list[Node.Node]=OgProgram.code.copy()
    Start:int = random.randint(a=0,b=(len(OgCode)-1))
    End:int = PickSubTree(Code=OgProgram,FirstIndex=Start)
    StartNode:Node.Node = random.choice(Union_List)
    OgCode[Start:End+1]= Program.RandomCode(StartNode,Depth=Start//2,MAX_DEPTH=MAX_DEPTH,Terminal_Set=Terminal_Set,Union_List=Union_List)
    MutProgram:Program = Program(Code=OgCode)
    return MutProgram

def Iterate(ThisGen:list[Program],GenNum:int,InputData:list[dict[str,int|float]],OutputData:list[int|float],Total_Error:list[int|float],Min_Error:list[int|float]
            ,HyperParas:dict[str,int|float|str|bool],Terminal_Set:list[Node],Union_List:list[Node],
            Display:Callable[[list[dict[str,int|float]],list[int|float],list[int|float],int|float,int,int],None],Terminate:bool =False) -> tuple[list[Program],list[int|float],list[int|float]]:
    """
    Takes a Generation with its Number And
    Returns the Next Generation After Selection,
    Crossover and Mutation if Terminate is False
    Otherwise returns Current Generation. 
    """
    GEN_SIZE:int = HyperParas["GENSIZE"]
    PDFFILE:str = HyperParas["RESULT"]
    MAX_XO:int = HyperParas["MAXXO"]
    XOP:float = HyperParas["XOP"]
    MAX_MUT:int = HyperParas["MAXMUT"]
    MUTP:float = HyperParas["MUTP"]
    MAX_NEW:int = HyperParas["MAXNEW"]
    NEWP:float = HyperParas["NEWP"]
    MAX_DEPTH:int = HyperParas["MAXDEPTH"]
    VERBOSE:bool = HyperParas["VERBOSE"]

    Prediction_List:list[list[int|float]] = []
    Error_List:list[int|float] = []
    for i,Code in enumerate(start=1,iterable=ThisGen):
        Predicted_Num:list[int|float] = []
        for Operand in InputData:
            Predicted_Num.append(Code.Compute(Operand=Operand))
#        os.system(clear)
        Error_Value:int|float = Code.Error(Required_Output=OutputData,Predicted_Output=Predicted_Num)
        Error_List.append(Error_Value)
        if min(Error_List)==Error_Value: Display(Input_Param=InputData,Output_Param=OutputData,Predict_Param=Predicted_Num,Error=Error_Value,GenNum=GenNum,ProgramNum=i)
        if not Error_Value:
            print(f"A Perfect Fit Found at {Code}")
            t:float = sum(Error_List)
            Total_Error.append(t)
            Min_Error.append(Error_Value)
            ThisGen.sort(key= lambda x:x.error)
            CodeList:list[list[Node.Node]] = []
            ErrorList:list[int|float] = []
            BestProgram:list[Program] = []
            i = 0
            for i in range(GEN_SIZE):
                if ThisGen[i].code not in CodeList:
                    CodeList.append(ThisGen[i].code)
                    ErrorList.append(ThisGen[i].error)
                    BestProgram.append(ThisGen[i])
                i += 1
            print("Generating Report.")
            CreateTex.Create(filepath=PDFFILE,equation=CodeList,NumberOfCode=GEN_SIZE,
                            TotalError=Total_Error,MinError=Min_Error,Input=[list(i.values()) for i in InputData],Output=OutputData,
                            Predict=[[ProgramX.Compute(Operand=Ops) for Ops in InputData] for ProgramX in BestProgram],ErrorList=ErrorList,HParams=HyperParas)
            #CreateTex.Create(filepath=PDFFILE,equation=Code.code,NumberOfCode=GEN_SIZE,TotalError=Total_Error,MinError=Min_Error,Input=[list(i.values()) for i in InputData],Output=OutputData,Predict=Predicted_Num)
            exit()
        Prediction_List.append(Predicted_Num)
    t:float = sum(Error_List)
    if not Terminate: Total_Error.append(t)
    print(f"Error List: {Error_List}\nGrand Total Error:{t}\nAverage Error:{t/GEN_SIZE}")
    if Terminate:
        return ThisGen,Total_Error,Min_Error
    NextGen:list[Program]=Selection(Generation=ThisGen,GEN_SIZE=GEN_SIZE)
    Min_Error.append(ThisGen[0].error)
    del ThisGen
    
    for i in range(MAX_XO):
        if random.random()<XOP:
            FirstCode,SecondCode = random.choices(NextGen[1::],k=2)
            indexFor_FC:int = NextGen.index(FirstCode,1)
            indexFor_SC:int = NextGen.index(SecondCode,1)
            FirstCode,SecondCode=Xover(FirstProgram=FirstCode,SecondProgram=SecondCode,VERBOSE=VERBOSE)
            NextGen[indexFor_FC] = SecondCode
            NextGen[indexFor_SC] = FirstCode

    for i in range(MAX_MUT):
        if random.random()<MUTP:
            SelectedCode:Program = random.choice(NextGen[1::])
            index:int = NextGen.index(SelectedCode,1)
            NextGen[index] = Mutation(SelectedCode,Terminal_Set,Union_List,MAX_DEPTH,VERBOSE)


    for i in range(MAX_NEW):
        if random.random()<NEWP:
            SelectedCodeIndex:int = random.randint(1,len(NextGen[1::])-1)
            NextGen[SelectedCodeIndex] = Program.CreateRandom(MAX_DEPTH,Terminal_Set,Union_List)
            if VERBOSE: print("A New Introduction is Observed")
    
    
    if VERBOSE:input("Proceed to New Generation?")
    return NextGen,Total_Error,Min_Error
