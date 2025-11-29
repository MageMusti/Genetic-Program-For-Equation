import yaml
import sys
from core.nodes import Node
from core.programs import Program
import Reload
from core.data import FormatCsv

def export_config(config:dict,filepath:str) -> None:
    with open(filepath,"w") as YamlFile:
        yaml.dump(config,YamlFile)

def import_config(filepath:str) -> dict:
    with open(filepath) as YamlFile:
        return yaml.safe_load(YamlFile)


def yamlInitialize(Data:dict[str,int|float|bool|str]) -> tuple[str,str,int,int,int,float,int,float,int,float,int,bool,bool]:
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
    newp:float = 0.1
    max_new: int = gen_size//10
    verbose:bool = False
    PDFfile:str = "Result"
    Fset:str  = ""
    reloadable:bool = False
    if "RESULT" in Data:
        PDFfile = str(Data["RESULT"])
        print(f"Report Location set to {PDFfile}.pdf") 

    if "FSET" in Data: 
        Fset = str(Data["FSET"])
        print(f"Function Set set to {Fset}") 

    if "MAXDEPTH" in Data:    
        max_depth = int(Data["MAXDEPTH"])
        print(f"Max Depth Set to {max_depth}")

    if "GENSIZE" in Data: 
        gen_size = int(Data["GENSIZE"])
        print(f"Generation Size Set to {gen_size}")

    if "MAXGEN" in Data: 
        max_gen = int(Data["MAXGEN"])
        print(f"Maximum Generation Set to {max_gen}")

    if "XOP" in Data: 
        xop = float(Data["XOP"])
        if xop<0: xop = xop.__abs__()
        if xop>1: xop = xop/(2*xop.__ceil__())
        print(f"Crossover Probability Set to {xop}") 
        
    if "MAXXO" in Data: 
        max_xo = int(Data["MAXXO"])
        print(f"Max Crossovers Set to {max_xo}")
        
    if "MUTP" in Data: 
        mutp = float(Data["MUTP"])
        if mutp<0: mutp = mutp.__abs__()
        if mutp>1: mutp = mutp/(2*mutp.__ceil__())
        print(f"Mutation Probability Set to {mutp}")
         
    if "MAXMUT" in Data: 
        max_mut = int(Data["MAXMUT"])
        print(f"Max Mutations Set to {max_mut}")

    if "NEWP" in Data: 
        newp = float(Data["NEWP"])
        if newp<0: newp = newp.__abs__()
        if newp>1: newp = newp/(2*newp.__ceil__())
        print(f"New Introduction Probability Set to {newp}")
        
    if "MAXNEW" in Data: 
        max_new = int(Data["MAXNEW"])
        print(f"Max New Introduction Set to {max_new}")

    if "VERBOSE" in Data:  
        verbose = bool(Data["VERBOSE"])
        print(f"Verbose Output Set to {verbose}")
    
    if "RELOAD" in Data:  
        reloadable = bool(Data["RELOAD"])
        print(f"Reload Set to {reloadable}")

    return(Fset,PDFfile,max_depth,gen_size,max_gen,xop,max_xo,mutp,max_mut,newp,max_new,verbose,reloadable)

def Initialize(argv:list[str]) -> tuple[dict[str,int|float|str|bool],int,int,int,bool,bool,str,str,str,list[float],list[float],list[Node],list[Program]]:
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
    newp:float = 0.1
    max_new: int = gen_size//10
    verbose:bool = False
    filepath:str = ''
    PDFfile:str = "Result"
    Fset:str = ""
    Master:bool = False
    Reloadable:bool = False
    ReloadingProgress:bool = False
    Anime:bool = False
    Total_Error:list[float] = []
    Min_Error:list[float] =[]
    Last_Gen:list[Program] = []
    global clear
    Terminal_Set:list[Node] = []
    try: 
        sys.getwindowsversion() # type: ignore
        clear = "cls"
    except AttributeError:
        clear = "clear"
    
    for i,arg in enumerate(argv,start=1):
        if i==1:
            continue
        
        if ReloadingProgress:
            filepath,PDFfile,max_depth,gen_size,max_gen,xop,max_xo,mutp,max_mut,newp,max_new,verbose,Fset,Total_Error_,Min_Error_,Current_Gen=Reload.load(arg)
            Total_Error = Total_Error_.tolist()
            Min_Error = Min_Error_.tolist()
            InputData,_ = FormatCsv(filepath=filepath)
            Terminal_Set = [Node("Const")]  #Initialize Terminal Set
            for i in range(1,len(InputData[0])+1):
                Terminal_Set.append(Node(f"var{i}"))    #Add Required variables
            Last_Gen:list[Program] = Program.ParseCode(Terminal_Set,Current_Gen)
            if ("-A" in argv) or ("-a" in argv) or ("--Anime" in argv): Anime = True
            config:dict[str,int|float|bool|str] = {"RESULT":PDFfile,"MAXDEPTH":max_depth,"GENSIZE":gen_size,"MAXGEN":max_gen,"XOP":xop,"MAXXO":max_xo,"MUTP":mutp,"MAXMUT":max_mut,"VERBOSE":verbose,"RELOAD":Reloadable,"FSET":Fset,"NEWP":newp,"MAXNEW":max_new,"Anime":Anime}
            return(config,max_depth,gen_size,max_gen,ReloadingProgress,Master,filepath,PDFfile,Fset,Total_Error,Min_Error,Terminal_Set,Last_Gen)

        if arg.startswith("-r"):
            ReloadingProgress = True
            continue

        
        if arg.startswith("--CONFIG:"):
            try:
                YamlFile:str = arg[len("--CONFIG:")::]
                Fset,PDFfile,max_depth,gen_size,max_gen,xop,max_xo,mutp,max_mut,newp,max_new,verbose,Reloadable = yamlInitialize(import_config(YamlFile))
            except FileNotFoundError:
                print(f"Configuration File not Found. Using Default Values.")
            except TypeError:
                print("Invalid Configuration File")
        if arg.startswith("--MAXDEPTH:"):
            try:
                max_depth:int = int(arg[len("--MAXDEPTH:")::])
                print(f"Max Depth Set to {max_depth}")
            except TypeError:
                print("Invalid Value for Max Depth.Taking Max Depth as 2")
            finally: continue

        if arg.startswith("--VERBOSE:") or arg.startswith("-v"):
            verbose:bool = True
            print(f"Verbose Output Set to {verbose}")
            continue
        
        
        if arg.startswith("--RELOAD:") or arg.startswith("-R"):
            Reloadable:bool = True
            print(f"Reload Set to {Reloadable}")
            continue
        
        if arg.startswith("--Anime:") or arg.startswith("-A"):
            Anime:bool = True
            continue


        if arg.startswith("--MASTER:") or arg.startswith("-m"):
            Master:bool = True
            #print(f"Verbose Output Set to {verbose}")
            continue
            
        if arg.startswith("--XOP:"):
            try:
                xop:float = float(arg[len("--XOP:")::])
                if xop<0: xop = xop.__abs__()
                if xop>1: xop = xop/(2*xop.__ceil__())
                print(f"Crossover Probability Set to {xop}")
            except TypeError:
                print("Invalid Value for Crossover Probability.Taking Crossover Probability as 0.8")
            finally: continue
    
        if arg.startswith("--MAXXO:"):
            try:
                max_xo:int = int(arg[len("--MAXXO:")::])
                print(f"Max Crossovers Set to {max_xo}")
            except TypeError:
                print("Invalid Value for Max Crossovers.Taking Max Crossovers as Generation Size//5")
            finally: continue

        if arg.startswith("--MAXNEW:"):
            try:
                max_new:int = int(arg[len("--MAXNEW:")::])
                print(f"Max New Introduction Set to {max_new}")
            except TypeError:
                print("Invalid Value for Max New Introduction.Taking Max New Introduction as Generation Size//10")
            finally: continue

        if arg.startswith("--NEWP:"):
            try:
                newp:float = float(arg[len("--NEWP:")::])
                if newp<0: newp = newp.__abs__()
                if newp>1: newp = newp/(2*newp.__ceil__())
                print(f"New Introduction Probability Set to {newp}")
            except TypeError:
                print("Invalid Value for New Introduction Probability.Taking New Introduction Probability as 0.1")
            finally: continue
    
        if arg.startswith("--REPORT:"):
            try:
                PDFfile:str = arg[len("--REPORT:")::]
                print(f"Report Location set to {PDFfile}.pdf")
            except TypeError:
                print("Invalid Value for Report Location .Taking Report Location as Result.pdf")
            finally: continue
    
        if arg.startswith("--FSET:"):
            try:
                Fset:str = arg[len("--FSET:")::]
                print(f"Function Set Set to {Fset}")
            except TypeError:
                print("Invalid Value for Function Set.Taking Function Set as ")
            finally: continue
            
        if arg.startswith("--MUTP:"):
            try:
                mutp:float = float(arg[len("--MUTP:")::])
                if mutp<0: mutp =mutp.__abs__()
                if mutp>1: mutp = mutp/(2*mutp.__ceil__())
                print(f"Mutation Probability Set to {mutp}")
            except TypeError:
                print("Invalid Value for Mutation Probability.Taking Mutation Probability as 0.5")
            finally: continue
    
        if arg.startswith("--MAXMUT:"):
            try:
                max_mut:int = int(arg[len("--MAXMUT:")::])
                print(f"Max Mutations Set to {max_mut}")
            except TypeError:
                print("Invalid Value for Max Mutations.Taking Max Mutations as Generation Size//10")
            finally: continue 
            
        if arg.startswith("--GENSIZE:"):
            try:
                gen_size:int = int(arg[len("--GENSIZE:")::])
                print(f"Generation Size Set to {gen_size}")
            except TypeError:
                print("Invalid Value for Generation Size.Taking Generation Size as 10")
            finally: continue
        
        if arg.startswith("--MAXGEN:"):
            try:
                max_gen:int = int(arg[len("--MAXGEN:")::])
                print(f"Max Generation Set to {max_gen}")
            except TypeError:
                print("Invalid Value for Max Generation.Taking Max Generation as 20")
            finally: continue

        filepath = arg
    config = {"RESULT":PDFfile,"MAXDEPTH":max_depth,"GENSIZE":gen_size,"MAXGEN":max_gen,"XOP":xop,"MAXXO":max_xo,"MUTP":mutp,"MAXMUT":max_mut,"VERBOSE":verbose,"RELOAD":Reloadable,"FSET":Fset,"NEWP":newp,"MAXNEW":max_new,"Anime":Anime}
    return(config,max_depth,gen_size,max_gen,ReloadingProgress,Master,filepath,PDFfile,Fset,Total_Error,Min_Error,Terminal_Set,Last_Gen)
