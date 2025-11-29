import os
import tkinter as tk
from tkinter import messagebox,filedialog,ttk
import core.data
import core.config
from core.Integer_Helper import CheckWhetherStringIsIntegerOrFloat as CIF
from core.programs import Program
from core.evolution import *
import Reload
import core.nodes as Node

def Display(Input_Param:list[dict[str,int|float]],Output_Param:list[int|float],Predict_Param:list[int|float],
            Error:int|float,GenNum:int,ProgramNum:int) -> None:

    global Table
    Table.destroy()
    Table = ttk.Frame(root,border=2,relief=tk.SOLID)
    Table.grid(row=2,column=1,padx=10,pady=20)
    tk.Label(Table,text=f"Generation: {GenNum+1}   Program: {ProgramNum}").grid(row=0,column=0,columnspan=5,padx=50)
    columns = ("Sr No.", "Input Data", "Required Output", "Predicted Output")
    tree = ttk.Treeview(Table, columns=columns, show="headings")
    
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=120)
    for i,_ in enumerate(Output_Param):
            tree.insert("", tk.END, values=[i+1,list(Input_Param[i].values()),Output_Param[i],Predict_Param[i] ] )

    tree.grid(row=1,column=0,columnspan=4)

    tk.Label(Table,text=f"The Total Error is {Error}").grid(row=2,column=0,columnspan=4)
    root.update_idletasks()
    root.update()


def Open_csv(filepath:str) -> None:
    global InputData,OutputData,ReloadInProgress
    try:
        InputData,OutputData = core.data.FormatCsv(filepath)
        ReloadInProgress = False
        Start.config(state=tk.ACTIVE)
        Status_Label.config(text="Ready")
        Display(Input_Param=InputData,Output_Param=OutputData,Predict_Param=OutputData,Error=0,GenNum=0,ProgramNum=0)
    except FileNotFoundError as err:
        messagebox.showerror(title="Data File Not Found",message=err)
    except Exception as err:
        messagebox.showerror(title="Unknown Exception Has Occured",message=err)

def Open_reload(filepath: str) -> None:
    global ReloadInProgress
    try:
        ReloadInProgress = True
        Start.config(state=tk.ACTIVE)
        Status_Label.config(text="Ready")
    except Exception as err:
        messagebox.showerror("Reload Failed", str(err))

def Open_input_file(filepath:str) -> None:
    if filepath.endswith(".csv"):
        Open_csv(filepath)
    elif filepath.endswith(".reload"):
        Open_reload(filepath)

def Select_input_file(dataFileEntry: tk.Entry) -> None:
    filepath = filedialog.askopenfilename(
        initialdir="./CSV/",
        title="Select Input File",
        defaultextension=".csv",
        filetypes=[("CSV File", "*.csv"),("Saved State","*.reload")]
    )
    dataFileEntry.delete(0, tk.END)
    dataFileEntry.insert(0, filepath)
    Open_input_file(filepath)

def SetOutputFile(filepath:str):
    global pdfFILE
    if not filepath: 
        messagebox.showerror(title="Invalid File Name",message="File Name is not Valid.",detail="Please Give Another file name")
        pdfFILE = "Report"
        return
    pdfFILE = filepath

def Select_pdf(OutputFileEntry:tk.Entry):
    filepath:str = filedialog.asksaveasfilename(confirmoverwrite=True,filetypes=[("PDF File","*.pdf")],initialdir=".",initialfile="Report.pdf",title="Save Output As")
    filepath = filepath.rstrip(".pdf")
    OutputFileEntry.delete(0,tk.END)
    OutputFileEntry.insert(0,filepath)
    SetOutputFile(filepath)

def SetReloadFile(filepath:str):
    global reloadFILE
    if not filepath: 
        messagebox.showerror(title="Invalid File Name",message="File Name is not Valid.",detail="Please Give Another file name")
        reloadFILE = "Report"
        return
    reloadFILE = filepath

def Select_reload(reloadFileEntry:tk.Entry):
    filepath:str = filedialog.asksaveasfilename(confirmoverwrite=True,filetypes=[("Saved State","*.reload")],initialdir=".",initialfile="Report.reload",title="Save State As")
    filepath = filepath.rstrip(".reload")
    reloadFileEntry.delete(0,tk.END)
    reloadFileEntry.insert(0,filepath)
    SetOutputFile(filepath)

def ImportConfig() -> None:
    global pdfFILE
    filepath:str = filedialog.askopenfilename(title="Open Saved Configurations",defaultextension=".yaml",initialdir="./Config/",initialfile="Sample.yaml",filetypes=[("YAML File","*.yaml")])
    config:dict =core.config.import_config(filepath)
    Func_Set,pdfFILE,max_depth,gen_size,max_gen,xop,max_xo,mutp,max_mut,newp,max_new,verbose,_ = core.config.yamlInitialize(config)
    
    MaxDepth.delete(0,tk.END)
    MaxDepth.insert(0,max_depth)

    Verbose.set(verbose)
    
    XOP.set(xop)
    MaxXO.delete(0,tk.END)
    MaxXO.insert(0,max_xo)

    MUTP.set(mutp)
    MaxMut.delete(0,tk.END)
    MaxMut.insert(0,max_mut)

    NEWP.set(newp)
    MaxNew.delete(0,tk.END)
    MaxNew.insert(0,max_new)

    GenSize.delete(0,tk.END)
    GenSize.insert(0,gen_size)

    MaxGen.delete(0,tk.END)
    MaxGen.insert(0,max_gen)

    OutputFile.delete(0,tk.END)
    OutputFile.insert(0,pdfFILE)
    
    FSET_E.set(True if "E" in Func_Set or "e" in Func_Set else False)
    FSET_L.set(True if "L" in Func_Set or "l" in Func_Set else False)
    FSET_P.set(True if "P" in Func_Set or "p" in Func_Set else False)
    FSET_T.set(True if "T" in Func_Set or "t" in Func_Set else False)
    FSET_R.set(True if "R" in Func_Set or "r" in Func_Set else False)

def ExportConfig() -> None:
    filepath:str = filedialog.asksaveasfilename(confirmoverwrite=True,defaultextension=".yaml",filetypes=[("YAML File","*.yaml")],initialdir="./Config/",initialfile="Saved.yaml",title="Save Configuration as")
    if not filepath:
        messagebox.showerror(title="Invalid File Name",message="File Name is not Valid.",detail="Please Give Another file name")
        return
    Func_Set:str = ""
    if FSET_E.get(): Func_Set += "E"
    if FSET_L.get(): Func_Set += "L"
    if FSET_P.get(): Func_Set += "P"
    if FSET_T.get(): Func_Set += "T"
    if FSET_R.get(): Func_Set += "R"
    try:
        config:dict = {
            "RELOAD": True,
            "MAXDEPTH": int(MaxDepth.get()),
            "VERBOSE": Verbose.get(),
            "XOP": XOP.get(),
            "MAXXO": int(MaxXO.get()),
            "MUTP": MUTP.get(),
            "MAXMUT": int(MaxMut.get()),
            "NEWP": NEWP.get(),
            "MAXNEW": int(MaxNew.get()),
            "GENSIZE": int(GenSize.get()),
            "MAXGEN": int(MaxGen.get()),
            "RESULT": OutputFile.get() ,
            "FSET": Func_Set 
            }
        core.config.export_config(config,filepath)
    except Exception as err:
        messagebox.showerror("Invalid Configuration Data",err)
        return

def main() -> None:
    disabledList = [dataFileEntry,dataFileOpenButton,dataFileSelectButton,
                         MaxDepth,MaxGen,GenSize,VerboseBox,ImportConfig_Button, ExportConfig_button,
                         MaxXO,MaxMut,MaxNew,
                         XOP_Slider,MUTP_Slider,NEWP_Slider,
                         FSET_R_Box,FSET_E_Box,FSET_L_Box,FSET_P_Box,FSET_T_Box,
                         OutputFile,OutputFileOpenButton,OutputFileSelectButton,
                         ReloadFileSelectButton,ReloadFileOpenButton,ReloadFile,Start]
    
    for Every_Object in disabledList:
        Every_Object.config(state=tk.DISABLED)
    
    global InputData,OutputData,reloadFILE

    Status_Label.config(text="Running...")
    if not ReloadInProgress:
        filepath:str = "Temp.yaml"
        Func_Set:str = ""
        if FSET_E.get(): Func_Set += "E"
        if FSET_L.get(): Func_Set += "L"
        if FSET_P.get(): Func_Set += "P"
        if FSET_T.get(): Func_Set += "T"
        if FSET_R.get(): Func_Set += "R"
        try:
            if OutputFile.get() == "": raise FileNotFoundError("Invalid Name For Output File.")
            config:dict = {
                "RELOAD": True,
                "MAXDEPTH": int(MaxDepth.get()),
                "VERBOSE": Verbose.get(),
                "XOP": XOP.get(),
                "MAXXO": int(MaxXO.get()),
                "MUTP": MUTP.get(),
                "MAXMUT": int(MaxMut.get()),
                "NEWP": NEWP.get(),
                "MAXNEW": int(MaxNew.get()),
                "GENSIZE": int(GenSize.get()),
                "MAXGEN": int(MaxGen.get()),
                "RESULT": OutputFile.get() ,
                "FSET": Func_Set ,
                }
            print(config)
            core.config.export_config(config,filepath)
        except Exception as err:
            messagebox.showerror("Invalid Configuration Data",err)
            return
        config,MAX_DEPTH,GEN_SIZE,MAX_GEN,RELOADPROGRESS,Master,Source_File,PDFFILE,FSET,Total_Error,Min_Error,Terminal_Set,Current_Gen = core.config.Initialize(["","--CONFIG:Temp.yaml",dataFileEntry.get()])
        os.remove("Temp.yaml")
    else: 
        config,MAX_DEPTH,GEN_SIZE,MAX_GEN,RELOADPROGRESS,Master,Source_File,PDFFILE,FSET,Total_Error,Min_Error,Terminal_Set,Current_Gen = core.config.Initialize(["","-r",dataFileEntry.get()])
        InputData,OutputData = core.data.FormatCsv(Source_File)

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

    Union_List:list[Node.Node] = Function_Set + Terminal_Set  #Set of All Nodes
    if not RELOADPROGRESS: Current_Gen:list[Program] = [Program.CreateRandom(MAX_DEPTH,Terminal_Set,Union_List) for _ in range(GEN_SIZE)] #First random Generation

    for i in range(MAX_GEN):Current_Gen,Total_Error,Min_Error=Iterate(ThisGen=Current_Gen,GenNum=i,InputData=InputData,OutputData=OutputData,Total_Error=Total_Error,Min_Error=Min_Error,HyperParas=config,Terminal_Set=Terminal_Set,Union_List=Union_List,Display=Display)   #Main Generation Loop
    Current_Gen,Total_Error,Min_Error=Iterate(ThisGen=Current_Gen,GenNum=i,InputData=InputData,OutputData=OutputData,Total_Error=Total_Error,Min_Error=Min_Error,HyperParas=config,Terminal_Set=Terminal_Set,Union_List=Union_List,Display=Display)  #Display Last Generation
    Current_Gen.sort(key= lambda x:x.error)

    Status_Label.config(text="Saving Reload Data,Compiling PDF...")
    root.update_idletasks()
    root.update()

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
    if not reloadFILE: Reload.save(InputFile=Source_File,HParams=config,Min_Error=Min_Error,Total_Error=Total_Error,lastGen=Current_Gen)
    else:              Reload.save(InputFile=Source_File,HParams=config,Min_Error=Min_Error,Total_Error=Total_Error,lastGen=Current_Gen,ReloadFile=reloadFILE)
    
    print("Generating Report.")
    CreateTex.Create(filepath=PDFFILE,equation=CodeList,NumberOfCode=GEN_SIZE,  
                     TotalError=Total_Error,MinError=Min_Error,Input=[list(i.values()) for i in InputData],Output=OutputData,
                     Predict=[[ProgramX.Compute(Operand=Ops) for Ops in InputData] for ProgramX in BestProgram],ErrorList=ErrorList,HParams=config) #Create Report
    Status_Label.config(text="Report Saved.")
    for Every_Object in disabledList:
        Every_Object.config(state=tk.NORMAL)


def run_gui():
    global root,dataFileEntry,Table,pdfFILE,MaxDepth,Verbose,XOP,MUTP,NEWP,MaxXO,MaxMut,MaxNew,GenSize,MaxGen,OutputFile,FSET_E,FSET_L,FSET_P,FSET_T,FSET_R,Start, \
    dataFileOpenButton,dataFileSelectButton,OutputFile,OutputFileOpenButton,OutputFileSelectButton,XOP_Slider,MUTP_Slider,NEWP_Slider, \
    FSET_E_Box,FSET_L_Box,FSET_P_Box,FSET_T_Box,FSET_R_Box,VerboseBox,ImportConfig_Button,ExportConfig_button,Status_Label,reloadFILE, ReloadFile,ReloadFileOpenButton,ReloadFileSelectButton
    reloadFILE = ""
    root = tk.Tk()
    root.title("Genetic Program")
    icon = tk.PhotoImage(file="Logo.png")
    root.iconphoto(False, icon)
    #root.geometry("1137x750")
    root.geometry("1325x757")


    dataFileFrame = tk.Frame(root)
    dataFileFrame.grid(row=1,column=0,columnspan=7,pady=20)

    dataFileLabel = tk.Label(dataFileFrame,text="Input Data: ",relief=tk.SUNKEN)
    dataFileLabel.grid(row=0,column=0)

    dataFileEntry = tk.Entry(dataFileFrame)
    dataFileEntry.grid(row=0,column=1,columnspan=5,ipadx=200)

    dataFileOpenButton = tk.Button(dataFileFrame,text="Open File",command=lambda : Open_input_file(dataFileEntry.get()))
    dataFileOpenButton.grid(row=0,column=6,ipadx=50)

    dataFileSelectButton = tk.Button(dataFileFrame,text="Browse",command= lambda : Select_input_file(dataFileEntry) )
    dataFileSelectButton.grid(row=0,column=7,ipadx=50)

    HyperParasFrame = ttk.Labelframe(root,text="Set Hyper Parameters",border=2,relief=tk.SOLID)
    HyperParasFrame.grid(row=2,column=0,pady=20,ipadx=10,ipady=10,rowspan=2,sticky=tk.W)

    MaxDepthLabel = tk.Label(HyperParasFrame,text="Maximum Depth: ")
    MaxDepthLabel.grid(row=1,column=0)
    MaxDepth = tk.Entry(HyperParasFrame)
    MaxDepth.grid(row=1,column=1)

    GenSizeLabel = tk.Label(HyperParasFrame,text="Generation Size: ")
    GenSizeLabel.grid(row=2,column=0)
    GenSize = tk.Entry(HyperParasFrame)
    GenSize.grid(row=2,column=1)
    
    MaxGenLabel = tk.Label(HyperParasFrame,text="Maximum Generation: ")
    MaxGenLabel.grid(row=3,column=0)
    MaxGen = tk.Entry(HyperParasFrame)
    MaxGen.grid(row=3,column=1)

    XoverFrame = tk.Frame(HyperParasFrame,bd=1,relief=tk.SOLID)
    XoverFrame.grid(row=4,column=0,columnspan=2,padx=10,pady=5)
    XoverLabel = tk.Label(XoverFrame,text="Crossover")
    XoverLabel.grid(row=0,column=0,columnspan=2)

    MaxXO_Label = tk.Label(XoverFrame,text="Maximum Crossovers: ")
    MaxXO_Label.grid(row=1,column=0)
    MaxXO = tk.Entry(XoverFrame)
    MaxXO.grid(row=1,column=1)

    XOP = tk.DoubleVar()
    XOP_Label = tk.Label(XoverFrame,text="Crossover Probability")
    XOP_Label.grid(row=2,column=0)
    XOP_Slider = tk.Scale(XoverFrame,from_=0,to=1,resolution=0.01,orient=tk.HORIZONTAL,variable=XOP)
    XOP_Slider.grid(row=2,column=1)

    MutFrame = tk.Frame(HyperParasFrame,bd=1,relief=tk.SOLID)
    MutFrame.grid(row=5,column=0,columnspan=2,padx=10,pady=5)
    MutLabel = tk.Label(MutFrame,text="Mutation")
    MutLabel.grid(row=0,column=0,columnspan=2)

    MaxMut_Label = tk.Label(MutFrame,text="Maximum Mutations: ")
    MaxMut_Label.grid(row=1,column=0)
    MaxMut = tk.Entry(MutFrame)
    MaxMut.grid(row=1,column=1)

    MUTP = tk.DoubleVar()
    MUTP_Label = tk.Label(MutFrame,text="Mutation Probability")
    MUTP_Label.grid(row=2,column=0)
    MUTP_Slider = tk.Scale(MutFrame,from_=0,to=1,resolution=0.01,orient=tk.HORIZONTAL,variable=MUTP)
    MUTP_Slider.grid(row=2,column=1)

    NewFrame = tk.Frame(HyperParasFrame,bd=1,relief=tk.SOLID)
    NewFrame.grid(row=6,column=0,columnspan=2,padx=10,pady=5)
    NewLabel = tk.Label(NewFrame,text="New Introduction")
    NewLabel.grid(row=0,column=0,columnspan=2)

    MaxNew_Label = tk.Label(NewFrame,text="Maximum New Introduction: ")
    MaxNew_Label.grid(row=1,column=0)
    MaxNew = tk.Entry(NewFrame)
    MaxNew.grid(row=1,column=1)

    NEWP = tk.DoubleVar()
    NEWP_Label = tk.Label(NewFrame,text="New Introduction Probability")
    NEWP_Label.grid(row=2,column=0)
    NEWP_Slider = tk.Scale(NewFrame,from_=0,to=1,resolution=0.01,orient=tk.HORIZONTAL,variable=NEWP)
    NEWP_Slider.grid(row=2,column=1)

    FSET_Frame = tk.Frame(HyperParasFrame,bd=1,relief=tk.SOLID)
    FSET_Frame.grid(row=7,column=0,columnspan=2,padx=10,pady=5)
    FSET_Label = tk.Label(FSET_Frame,text="Function Set")
    FSET_Label.grid(row=0,column=0,columnspan=2)

    FSET_M = tk.BooleanVar()
    FSET_M.set(True)
    FSET_E = tk.BooleanVar()
    FSET_L = tk.BooleanVar()
    FSET_P = tk.BooleanVar()
    FSET_R = tk.BooleanVar()
    FSET_T = tk.BooleanVar()
    
    FSET_M_Box = tk.Checkbutton(FSET_Frame,text="Addition,Subtraction\nMultiplication,Division",variable=FSET_M,onvalue=True,offvalue=False,state=tk.DISABLED)
    FSET_E_Box = tk.Checkbutton(FSET_Frame,text="Power",variable=FSET_E,onvalue=True,offvalue=False)
    FSET_L_Box = tk.Checkbutton(FSET_Frame,text="Logrithm and Exponentation",variable=FSET_L,onvalue=True,offvalue=False)
    FSET_P_Box = tk.Checkbutton(FSET_Frame,text="Square and Cube",variable=FSET_P,onvalue=True,offvalue=False)
    FSET_R_Box = tk.Checkbutton(FSET_Frame,text="Square root and Cube root",variable=FSET_R,onvalue=True,offvalue=False)
    FSET_T_Box = tk.Checkbutton(FSET_Frame,text="sin,cos and tan",variable=FSET_T,onvalue=True,offvalue=False)
    
    FSET_M_Box.grid(row=1,column=0)
    FSET_E_Box.grid(row=2,column=0)
    FSET_L_Box.grid(row=3,column=0)
    FSET_P_Box.grid(row=4,column=0)
    FSET_R_Box.grid(row=5,column=0)
    FSET_T_Box.grid(row=6,column=0)

    Verbose = tk.BooleanVar()
    VerboseBox = tk.Checkbutton(HyperParasFrame,text="Verbose",variable=Verbose,onvalue=True,offvalue=False)
    VerboseBox.grid(row=8,column=0)

    ImportConfig_Button = tk.Button(HyperParasFrame,text="Import Config",command=ImportConfig)
    ImportConfig_Button.grid(row=9,column=0)
    ExportConfig_button = tk.Button(HyperParasFrame,text="Export Config",command=ExportConfig)
    ExportConfig_button.grid(row=9,column=1)

    Table = tk.Frame(root,bd=2,relief=tk.SOLID)
    Table.grid(row=2,column=1,padx=10,pady=20)

    OutputFrame = ttk.Labelframe(root,text="Output Details",relief=tk.SOLID)
    OutputFrame.grid(row=2,column=8,pady=20,ipadx=10,ipady=10,sticky=tk.E)
    
    OutputFile_Label = tk.Label(OutputFrame,text="Result: ")
    OutputFile_Label.grid(row=1,column=0)
    OutputFile = tk.Entry(OutputFrame)
    OutputFile.grid(row=1,column=1)
    OutputFileType_Label = tk.Label(OutputFrame,text=".pdf")
    OutputFileType_Label.grid(row=1,column=2)

    OutputFileOpenButton = tk.Button(OutputFrame,text="Set Path",command= lambda : SetOutputFile(OutputFile.get()))
    OutputFileOpenButton.grid(row=2,column=1,ipadx=35,sticky=tk.E)
    OutputFileSelectButton = tk.Button(OutputFrame,text="Browse",command= lambda : Select_pdf(OutputFile))
    OutputFileSelectButton.grid(row=2,column=2)

    ReloadFile_Label = tk.Label(OutputFrame,text="Reload: ")
    ReloadFile_Label.grid(row=3,column=0)
    ReloadFile = tk.Entry(OutputFrame)
    ReloadFile.grid(row=3,column=1)
    ReloadFileType_Label = tk.Label(OutputFrame,text=".reload")
    ReloadFileType_Label.grid(row=3,column=2)

    ReloadFileOpenButton = tk.Button(OutputFrame,text="Set Path",command= lambda : SetReloadFile(ReloadFile.get()))
    ReloadFileOpenButton.grid(row=4,column=1,ipadx=35,sticky=tk.E)
    ReloadFileSelectButton = tk.Button(OutputFrame,text="Browse",command= lambda : Select_reload(ReloadFile))
    ReloadFileSelectButton.grid(row=4,column=2)

    Status_Label = tk.Label(root,text="Open Data")
    Status_Label.grid(row=3,column=0,sticky=tk.W+tk.S)

    Start = tk.Button(root,text="Start",state=tk.DISABLED,command=main)
    Start.grid(row=3,column=8,ipadx=10,sticky=tk.E + tk.S)
    root.mainloop()
