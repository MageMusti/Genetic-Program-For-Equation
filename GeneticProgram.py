import csv
import os
import math
import sys
import random
import time
from Integer_Helper import CheckWhetherStringIsIntegerOrFloat as CIF
import PostEva
import yaml
import CreateTex

class Node:
    """
    A Node is either a Operator or Operand in the Program.
    """
    
    def __init__(self,Symbol:str,OperatorRequired:int = 0,IsNum:bool = False,Value:int|float|None = None) -> None:
        """
        Symbol:Symbol or Name of Node
        OperatorRequired: How many Operands does the Operator Work on,
        e.g. for 2 for add and 0 for Operands.
        IsNum: is the Node a Constant Value.
        Value: If Constant Value, then Provide it's Value
        """
        self.symbol:str = Symbol
        self.Terminal:int = OperatorRequired
        self.IsNum:bool = IsNum
        if self.IsNum and (z:=CIF(Value))!="Null":
            self.Value: int|float = z

    def __str__(self) -> str:
        return f"{self.symbol} takes {self.Terminal} arguments"
    
    def __repr__(self) -> str:
        return f"{self.symbol}"
    
class Program:
    """
    A Set of Instructions to Be Executed.
    """
    
    def __init__(self,Code:list[Node]) -> None:
        """
        Give list of Nodes as Prefix Instructions.
        """
        self.code: list[Node] = []
        self.prob: float = 0
        self.error: int|float = math.inf
        for Elem in Code:
            if Elem.symbol!="Const":
                self.code.append(Elem)
                continue
            if random.choice([True,False]):
                RandomNumF:float = random.random()
                self.code.append(Node(f"{RandomNumF:.4f}",OperatorRequired=0,IsNum=True,Value=RandomNumF))
            else:
                RandomNum:int = random.randint(a=-100,b=100)
                self.code.append(Node(f"{RandomNum}",OperatorRequired=0,IsNum=True,Value=RandomNum))


    def __str__(self) -> str:
        return f"{self.code}"
    
    def __repr__(self) -> str:
        return f"{self.code}"

    def Compute(self,Operand:dict[str,int|float]) -> int|float:
        """
        Computes the Value of Code for Given Values of Operands
        """
        
        Code:list[str] = [Elem.symbol for Elem in self.code ]
        Code.reverse()
        Operand2 = Operand.copy()
        for Parts in Code:
            if (z:=CIF(Parts))!="Null":
                Operand2[Parts]=z
        Result:int|float = PostEva.ComputeEq(' '.join(Code),Operand2)
        return Result
    
    def Error(self,Required_Output:list[int|float],Predicted_Output:list[int|float]) -> int|float:
        """
        Calculates Sum of All Error Between Required_Output and Predicted_Output.
        Stores it in self.error .
        """
        
        Sum:int|float = 0
        for ReqOut,PreOut in zip(Required_Output,Predicted_Output):
            Sum += (ReqOut-PreOut).__abs__()
        self.error = Sum.__abs__()
        return self.error
    
    @staticmethod
    def RandomCode(S:Node,Depth:int) -> list[Node]:
        """
        Generate Random Code.
        """
        
        Random:list[Node] = [S]
        if not Random[-1].Terminal:
            return Random
        if Depth>=MAX_DEPTH:
            for i in range(0,Random[-1].Terminal):
                NewNode:Node = random.choice(Terminal_Set)
                Random.extend(Program.RandomCode(NewNode,Depth+1))
            return Random
        
        for i in range(0,Random[-1].Terminal):
            NewNode:Node = random.choice(Union_List)
            Random.extend(Program.RandomCode(NewNode,Depth+1))
        return Random

            
    
    @staticmethod
    def CreateRandom(SomeList:list[Node]|None = None) -> 'Program':
        """
        Return A Random Program
        """
        
        CodeList:list[Node] = []
        if not SomeList: Random_Node:Node = random.choice(Union_List)
        else: Random_Node:Node = random.choice(SomeList)
        CodeList.extend(Program.RandomCode(Random_Node,Depth=1))
        return Program(Code=CodeList)

def yamlInitialize(Data:dict) -> tuple[str,str,int,int,int,float,int,float,int,bool]:
    """
    Initialize Hyper Parameters Form a Yaml File
    """
    max_depth:int = 2
    gen_size:int = 10
    max_gen:int = 20
    xop:float = 0.8
    max_xo:int = gen_size//5
    mutp:float = 0.5
    max_mut:int = gen_size//10
    verbose:bool = False
    PDFfile:str = "Result"
    Fset:str  = ""
    try: 
        PDFfile = Data["RESULT"]
        print(f"Report Location set to {PDFfile}.pdf") 
    except KeyError as err:...
    except TypeError as err:print(f"Invalid Type of Report File Path\nReport File Path Set to {PDFfile}")
    try: 
        Fset = Data["FSET"]
        print(f"Function Set set to {Fset}") 
    except KeyError as err:...
    except TypeError as err:print(f"Invalid Type of Fset\nFset Set to {Fset}")
    try: 
        max_depth = Data["MAXDEPTH"]
        print(f"Max Depth Set to {max_depth}") 
    except KeyError as err:...
    except TypeError as err:print(f"Invalid Type of max depth\nMax Depth Set to {max_depth}")
    try: 
        gen_size = Data["GENSIZE"]
        print(f"Generation Size Set to {gen_size}")
    except KeyError as err:...
    except TypeError as err:print("Invalid Value for Generation Size.Taking Generation Size as 10")
    try: 
        max_gen = Data["MAXGEN"]
        print(f"Maximum Generation Set to {max_gen}")
    except KeyError as err:...
    except TypeError as err:print("Invalid Value for Maximum Generation.Taking Maximum Generation as 20")
    try: 
        xop = Data["XOP"]
        if xop<0:xop.__abs__()
        if xop>1: xop = xop/(2*xop.__ceil__())
        print(f"Crossover Probability Set to {xop}") 
    except KeyError as err:...
    except TypeError as err:print("Invalid Value for Crossover Probability.Taking Crossover Probability as 0.8")
    try: 
        max_xo = Data["MAXXO"]
        print(f"Max Crossovers Set to {max_xo}")
    except KeyError as err:...
    except TypeError as err:print("Invalid Value for Max Crossovers.Taking Max Crossovers as Generation Size//5")
    try: 
        mutp = Data["MUTP"]
        if mutp<0:mutp.__abs__()
        if mutp>1: mutp = mutp/(2*mutp.__ceil__())
        print(f"Mutation Probability Set to {mutp}")
    except KeyError as err:...
    except TypeError as err:print("Invalid Value for Mutation Probability.Taking Mutation Probability as 0.5")
    try: 
        max_mut = Data["MAXMUT"]
        print(f"Max Mutations Set to {max_mut}")
    except KeyError as err:...
    except TypeError as err:print("Invalid Value for Max Mutations.Taking Max Mutations as Generation Size//10")
    try: 
        verbose = Data["VERBOSE"]
        print(f"Verbose Output Set to {verbose}")
    except KeyError as err:...
    except TypeError as err:print(f"Invalid Type of Verbose\nVerbose Output Set to {verbose}")
    return(Fset,PDFfile,max_depth,gen_size,max_gen,xop,max_xo,mutp,max_mut,verbose)

def Initialize(argv:list[str]) -> tuple[dict,int,int,int,float,int,float,int,bool,str,str,str]:
    """
    Initialize Hyper Parameters Form CLI
    """
    max_depth:int = 2
    gen_size:int = 10
    max_gen:int = 20
    xop:float = 0.8
    max_xo:int = gen_size//5
    mutp:float = 0.5
    max_mut:int = gen_size//10
    verbose:bool = False
    filepath:str = ''
    PDFfile:str = "Result"
    Fset:str = ""
    global clear
    try: 
        sys.getwindowsversion()
        clear = "cls"
    except AttributeError as err:
        clear = "clear"
    for i,arg in enumerate(argv,start=1):
        if i==1:
            continue
        if arg.startswith("--CONFIG:"):
            try:
                YamlFile:str = arg[len("--CONFIG:")::]
                with open(YamlFile,"r") as File:
                    config = yaml.safe_load(File)
                    Fset,PDFfile,max_depth,gen_size,max_gen,xop,max_xo,mutp,max_mut,verbose = yamlInitialize(config)
            except FileNotFoundError as err:
                print(f"Configuration File not Found. Using Default Values.")
            except TypeError as err:
                print("Invalid Configuration File")
        if arg.startswith("--MAXDEPTH:"):
            try:
                max_depth:int = int(arg[len("--MAXDEPTH:")::])
                print(f"Max Depth Set to {max_depth}")
            except TypeError as err:
                print("Invalid Value for Max Depth.Taking Max Depth as 2")
            finally: continue

        if arg.startswith("--VERBOSE:") or arg.startswith("-v"):
            verbose:bool = True
            print(f"Verbose Output Set to {verbose}")
            continue
            
        if arg.startswith("--XOP:"):
            try:
                xop:float = float(arg[len("--XOP:")::])
                if xop<0:xop.__abs__()
                if xop>1: xop = xop/(2*xop.__ceil__())
                print(f"Crossover Probability Set to {xop}")
            except TypeError as err:
                print("Invalid Value for Crossover Probability.Taking Crossover Probability as 0.8")
            finally: continue
    
        if arg.startswith("--MAXXO:"):
            try:
                max_xo:int = int(arg[len("--MAXXO:")::])
                print(f"Max Crossovers Set to {max_xo}")
            except TypeError as err:
                print("Invalid Value for Max Crossovers.Taking Max Crossovers as Generation Size//5")
            finally: continue
    
        if arg.startswith("--REPORT:"):
            try:
                PDFfile:str = arg[len("--REPORT:")::]
                print(f"Report Location set to {PDFfile}.pdf")
            except TypeError as err:
                print("Invalid Value for Report Location .Taking Report Location as Result.pdf")
            finally: continue
    
        if arg.startswith("--FSET:"):
            try:
                Fset:str = arg[len("--FSET:")::]
                print(f"Function Set Set to {Fset}")
            except TypeError as err:
                print("Invalid Value for Function Set.Taking Function Set as ")
            finally: continue
            
        if arg.startswith("--MUTP:"):
            try:
                mutp:float = float(arg[len("--MUTP:")::])
                if mutp<0:mutp.__abs__()
                if mutp>1: mutp = mutp/(2*mutp.__ceil__())
                print(f"Mutation Probability Set to {mutp}")
            except TypeError as err:
                print("Invalid Value for Mutation Probability.Taking Mutation Probability as 0.5")
            finally: continue
    
        if arg.startswith("--MAXMUT:"):
            try:
                max_mut:int = int(arg[len("--MAXMUT:")::])
                print(f"Max Mutations Set to {max_mut}")
            except TypeError as err:
                print("Invalid Value for Max Mutations.Taking Max Mutations as Generation Size//10")
            finally: continue 
            
        if arg.startswith("--GENSIZE:"):
            try:
                gen_size:int = int(arg[len("--GENSIZE:")::])
                print(f"Generation Size Set to {gen_size}")
            except TypeError as err:
                print("Invalid Value for Generation Size.Taking Generation Size as 10")
            finally: continue
        
        if arg.startswith("--MAXGEN:"):
            try:
                max_gen:int = int(arg[len("--MAXGEN:")::])
                print(f"Max Generation Set to {max_gen}")
            except TypeError as err:
                print("Invalid Value for Max Generation.Taking Max Generation as 20")
            finally: continue

        filepath = arg
    config = {"RESULT":PDFfile,"MAXDEPTH":max_depth,"GENSIZE":gen_size,"MAXGEN":max_gen,"XOP":xop,"MAXXO":max_xo,"MUTP":mutp,"MAXMUT":max_mut,"VERBOSE":verbose,"FSET":Fset}
    return(config,max_depth,gen_size,max_gen,xop,max_xo,mutp,max_mut,verbose,filepath,PDFfile,Fset)

def FormatCsv(filepath:str) -> tuple[list[dict[str,int|float]],list[int|float]]:
    """
    This Function takes a Path to a csv file and returns
    a list of list of Integers and floats as Input for all elements except
    the last in each and the Output as list of all last elements of each row.
    """
    
    with open(file=filepath,mode="r") as csv_file:
        csv_reader = csv.reader(csv_file)
        Output:list[int|float] = []
        Input:list[dict[str,int|float]] = []
        for row in csv_reader:
            list_row: list = row.copy()
            OutputNum:str = list_row.pop()
            if (x:=CIF(OutputNum))=="Null":
                raise TypeError(f"Last Element in row {row} is not a Number")    
            Output.append(x)
            Input.append({f"var{i}":CIF(Num) for i,Num in enumerate(start=1,iterable=list_row) if CIF(Num)!="Null"}) # type: ignore

    return (Input,Output)

def Display(Input_Param:list[dict[str,int|float]],Output_Param:list[int|float],Predict_Param:list[int|float],
            Error:int|float,GenNum:int,ProgramNum:int) -> None:
    """
    Display The Program's Stats in a Pseudo-Tabular Format
    """
    print("-"*len("Sr No.    Input Data        Required Output        Predicted Output"))
    print(f"Generation: {GenNum}   Program: {ProgramNum}")
    for i,Something in enumerate(Output_Param):
        if i==0:
            print("Sr No.\tInput Data\t\tRequired Output\t\tPredicted Output")
        InputList: list[int|float] = list(Input_Param[i].values())
        print(f"{i+1}.\t{InputList}\t\t\t\t{Output_Param[i]}\t\t{Predict_Param[i]}")
    print("-"*len("Sr No.    Input Data        Required Output        Predicted Output"))
    print(f"The Total Error is {Error}")

def Softmax(Input: list[Program]) -> None:
    """
    Sets Probability of Selection For Programs in Given List
    Based on the Error of Each Program Using Softmax.
    """
    #exponentForm: list[float] = [math.exp(GEN_SIZE/Code.error) for Code in Input]
    exponentForm: list[float] = []
    for Code in Input:
        try: exponentForm.append(math.exp(GEN_SIZE/Code.error))
        except OverflowError as err: 
            exponentForm.append(1000000)
            input(f"Too much Big Number\n{err}")
    Sum: float = sum(exponentForm)
    for i,Code in enumerate(Input):
        Code.prob = exponentForm[i]/Sum

def Selection(Generation:list[Program]) -> list[Program]:
    """
    Based On Error of Programs in Given Generation
    Return New Generation Using Roulette Wheel Selection
    """
    Generation.sort(key=lambda x:x.error)
    Softmax(Generation)
    NewGeneration:list[Program] = []
    NewGeneration.append(Generation[0])
    for i in range(GEN_SIZE-1):
        try: Selected_Program:Program = random.choices(Generation,k=1,weights=[X.prob for X in Generation])[0]
        except ValueError as err: Selected_Program:Program = random.choice(Generation)
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
        for i in range(Code.code[FirstIndex].Terminal):
            LastIndex=PickSubTree(Code=Code,FirstIndex=(LastIndex+1))
    return LastIndex

def Xover(FirstProgram:Program,SecondProgram:Program) -> tuple[Program,Program]:
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
    FirstList:list[Node] = Fp.code[FP_start:FP_Last+1]
    SecondList:list[Node] = Sp.code[SP_start:SP_Last+1]
    Fp.code[FP_start:FP_Last+1] = SecondList
    Sp.code[SP_start:SP_Last+1] = FirstList
    return (Fp,Sp)

def Mutation(OgProgram:Program) -> Program:
    """
    Introduces a Random Mutation in the Given
    Program. Returns Mutated Program.
    """
    if VERBOSE:print("A Mutation is Observed")
    OgCode:list[Node]=OgProgram.code.copy()
    Start:int = random.randint(a=0,b=(len(OgCode)-1))
    End:int = PickSubTree(Code=OgProgram,FirstIndex=Start)
    StartNode:Node = random.choice(Union_List)
    OgCode[Start:End+1]= Program.RandomCode(StartNode,Depth=Start//2)
    MutProgram:Program = Program(Code=OgCode)
    return MutProgram

def Iterate(ThisGen:list[Program],GenNum:int,Terminate:bool =False,) -> list[Program]:
    """
    Takes a Generation with its Number And
    Returns the Next Generation After Selection,
    Crossover and Mutation if Terminate is False
    Otherwise returns Current Generation. 
    """
    Prediction_List:list[list[int|float]] = []
    Error_List:list[int|float] = []
    for i,Code in enumerate(start=1,iterable=ThisGen):
        Predicted_Num:list[int|float] = []
        for Operand in InputData:
            Predicted_Num.append(Code.Compute(Operand=Operand))
        os.system(clear)
        Error_Value:int|float = Code.Error(Required_Output=OutputData,Predicted_Output=Predicted_Num)
        Error_List.append(Error_Value)
        Display(Input_Param=InputData,Output_Param=OutputData,Predict_Param=Predicted_Num,Error=Error_Value,GenNum=GenNum,ProgramNum=i)
        if not Error_Value:
            print(f"A Perfect Fit Found at {Code}")
            t:float = sum(Error_List)
            Total_Error.append(t)
            Min_Error.append(Error_Value)
            Current_Gen.sort(key= lambda x:x.error)
            CodeList:list[list[Node]] = []
            ErrorList:list[int|float] = []
            BestProgram:list[Program] = []
            i = 0
            while len(CodeList)!=5:
                if Current_Gen[i].code not in CodeList:
                    CodeList.append(Current_Gen[i].code)
                    ErrorList.append(Current_Gen[i].error)
                    BestProgram.append(Current_Gen[i])
                i += 1
            print("Generating Report.")
            CreateTex.Create(filepath=PDFFILE,equation=CodeList,NumberOfCode=GEN_SIZE,
                            TotalError=Total_Error,MinError=Min_Error,Input=[list(i.values()) for i in InputData],Output=OutputData,
                            Predict=[[ProgramX.Compute(Operand=Ops) for Ops in InputData] for ProgramX in BestProgram],ErrorList=ErrorList,HParams=HyperParas)
            #CreateTex.Create(filepath=PDFFILE,equation=Code.code,NumberOfCode=GEN_SIZE,TotalError=Total_Error,MinError=Min_Error,Input=[list(i.values()) for i in InputData],Output=OutputData,Predict=Predicted_Num) 
            exit()
        Prediction_List.append(Predicted_Num)
    t:float = sum(Error_List)
    Total_Error.append(t)
    print(f"Error List: {Error_List}\nGrand Total Error:{t}\nAverage Error:{t/GEN_SIZE}")
    if Terminate:
        Min_Error.append(ThisGen[0].error) 
        return ThisGen
    NextGen:list[Program]=Selection(Generation=ThisGen)
    Min_Error.append(ThisGen[0].error)
    del ThisGen
    
    for i in range(MAX_XO):
        if random.random()<XOP:
            FirstCode,SecondCode = random.choices(NextGen[1::],k=2)
            indexFor_FC:int = NextGen.index(FirstCode,1)
            indexFor_SC:int = NextGen.index(SecondCode,1)
            FirstCode,SecondCode=Xover(FirstProgram=FirstCode,SecondProgram=SecondCode)
            NextGen[indexFor_FC] = SecondCode
            NextGen[indexFor_SC] = FirstCode

    for i in range(MAX_MUT):
        if random.random()<MUTP:
            SelectedCode:Program = random.choice(NextGen[1::])
            index:int = NextGen.index(SelectedCode,1)
            NextGen[index] = Mutation(SelectedCode)
    if VERBOSE:input("Proceed to New Generation?")
    return NextGen

if __name__ =="__main__":
    argv:list[str] = sys.argv #Get Arguments List
    if not len(argv)>1:         #Check If Sufficient Arguments
        print(f'''Invalid Usage
            Usage: python {argv[0]} <filename>.csv
            
            The Following Options can be Specified:
              
            --CONFIG: Path to a yaml Config file to Set Parameters

            --REPORT: Path to Results pdf file (Without Extension)
            --MAXDEPTH:  Max Depth of Program tree
            --VERBOSE or -v: For verbose Output
            --XOP: Crossover probability
            --MAXXO: Max Crossover Per Generation
            --MUTP: Mutation probability
            --MAXMUT: Max Mutation Per Generation
            --GENSIZE: Size of Each Generation
            --MAXGEN: Maximum Generation to be Explored
            --FSET: Function Set to be Used
              Include Following Characters in FSET for following Operations
              E for Exponentiation
              P for Square and Cube
              R for Square Root and Cube Root
              T for Sin, Cos and Tan''')
        exit()

#Initialize Nodes
    start:float = time.perf_counter()
    Plus:Node = Node("+",2)
    Minus:Node = Node("-",2)
    Mul:Node = Node("*",2)
    Divide:Node = Node("/",2)
    Power:Node = Node("^",2)
    Square:Node = Node("S",1)
    Cube:Node = Node("C",1)
    Square_Root:Node = Node("R",1)
    Cube_Root:Node = Node("T",1)
    Sin:Node = Node("$",1)
    Cos:Node = Node("&",1)
    Tan:Node = Node("@",1)
    HyperParas,MAX_DEPTH,GEN_SIZE,MAX_GEN,XOP,MAX_XO,MUTP,MAX_MUT,VERBOSE,arg,PDFFILE,FSET=Initialize(argv) #Get Hyper Parameters

    InputData,OutputData=FormatCsv(arg)  #Get Input and Output Data
    
    Function_Set: list[Node] =[Plus,Minus,Mul,Divide]   #Initialize Function Set
    if "E" in FSET or "e" in FSET: Function_Set.append(Power)
    if "P" in FSET or "p" in FSET: 
        Function_Set.append(Square)
        Function_Set.append(Cube)
    if "R" in FSET or "r" in FSET:
        Function_Set.append(Square_Root)
        Function_Set.append(Cube_Root)
    if "T" in FSET or "t" in FSET: 
        Function_Set.append(Sin) 
        Function_Set.append(Cos) 
        Function_Set.append(Tan)
    Terminal_Set: list[Node] = [Node("Const")]  #Initialize Terminal Set
        
    Check:str =input("Confirm(Enter to Continue,else Stop)?")   #Confirm Parameters Values
    if Check!="": exit()
    Total_Error:list[float] = []
    Min_Error:list[float] = []

    for i in range(1,len(InputData[0])+1):
        Terminal_Set.append(Node(f"var{i}"))    #Add Required variables
    Union_List:list[Node] = Function_Set + Terminal_Set #Set of All Nodes
    Current_Gen:list[Program] = [Program.CreateRandom() for i in range(GEN_SIZE)] #First random Generation
    for i in range(MAX_GEN):Current_Gen=Iterate(ThisGen=Current_Gen,GenNum=i)   #Main Generation Loop
    Current_Gen=Iterate(ThisGen=Current_Gen,Terminate=True,GenNum=MAX_GEN)  #Display Last Generation
    Current_Gen.sort(key= lambda x:x.error) #Sort Last Generation By Error.
    end:float = time.perf_counter()
    print(f"The Program With Minimum Error is:\n{Current_Gen[0]}\nWith the Total Error of {Current_Gen[0].error}\nTime Taken:{end-start:.4f} seconds")  #Print Final Result

    #Assemble Data for Report
    CodeList:list[list[Node]] = []
    ErrorList:list[int|float] = []
    BestProgram:list[Program] = []
    i = 0
    while len(CodeList)!=5:
        if Current_Gen[i].code not in CodeList:
            CodeList.append(Current_Gen[i].code)
            ErrorList.append(Current_Gen[i].error)
            BestProgram.append(Current_Gen[i])
        i += 1
    print("Generating Report.")
    CreateTex.Create(filepath=PDFFILE,equation=CodeList,NumberOfCode=GEN_SIZE,  
                     TotalError=Total_Error,MinError=Min_Error,Input=[list(i.values()) for i in InputData],Output=OutputData,
                     Predict=[[ProgramX.Compute(Operand=Ops) for Ops in InputData] for ProgramX in BestProgram],ErrorList=ErrorList,HParams=HyperParas) #Create Report
