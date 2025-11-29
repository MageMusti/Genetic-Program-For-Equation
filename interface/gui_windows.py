import customtkinter as ctk
from customtkinter import filedialog
import CTkToolTip
from tkinter import messagebox,ttk
from PIL import Image
import core.data
import core.config
import os
import Reload
from core.programs import Program
from core.evolution import *
import core.nodes as Node

C_FONT:tuple[str,int] = ("Segoe UI",12)
SUBFRAME_WIDTH = 400
SUBFRAME_HEIGHT = 125
BUTTON_FG_COLOR =  "#51b6fa"
BUTTON_HOVER_COLOR = "#033d61"
BUTTON_TEXT_COLOR = "#0f0f0f"
BUTTON_TEXT_DISABLE_COLOR = "#ffffff"
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

def Display(Input_Param:list[dict[str,int|float]],Output_Param:list[int|float],Predict_Param:list[int|float],
            Error:int|float,GenNum:int,ProgramNum:int) -> None:

    global Table
    Table.destroy()
    Table = ctk.CTkFrame(root,border_width=0,border_color=("#ffffff","#000000"),bg_color=("#000000","#ffffff"),fg_color="#ffffff",corner_radius=10)
    Table.grid(row=2, column=5, rowspan=2, padx=10, pady=20 )


    ctk.CTkLabel(Table,text=f"Generation: {GenNum+1}   Program: {ProgramNum}",fg_color="#ffffff",text_color="#000000",anchor=ctk.CENTER,font=C_FONT).grid(row=0,column=0,columnspan=5,padx=50)
    columns = ("Sr No.", "Input Data", "Required Output", "Predicted Output")
   
    tree = ttk.Treeview(Table, columns=columns, show="headings")
    
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=120)
    for i,_ in enumerate(Output_Param):
            tree.insert("", 'end', values=[i+1,list(Input_Param[i].values()),Output_Param[i],Predict_Param[i] ] )

    tree.grid(row=1,column=0,columnspan=4,sticky="nsew")

    ctk.CTkLabel(Table,text=f"The Total Error is {Error}",fg_color="#ffffff",text_color="#000000",anchor=ctk.CENTER,font=C_FONT).grid(row=2,column=0,columnspan=4)
    root.update_idletasks()
    root.update()

def ToggleTheme_Func():
    if ctk.get_appearance_mode()=="Dark":
        ctk.set_appearance_mode("light")
    else:
        ctk.set_appearance_mode("dark")

def UpdateSliderValue(Label:ctk.CTkLabel,Value:float) -> None:
    Label.configure(text=f"{Value:.2f}")
    
def EnableStart():
    global Start
    Start.configure(state=ctk.NORMAL,cursor="hand2",fg_color="#1abc9c",hover_color="#16a085")
    
def EnableExit():
    global exit_button
    exit_button.configure(state=ctk.NORMAL,cursor="hand2",fg_color="#e74c3c",hover_color="#c0392b")

def DisableButtons():
    global Start,dataFileOpenButton,dataFileSelectButton,exit_button,ImportConfig_Button,ExportConfig_button,OutputFileOpenButton,OutputFileSelectButton,ReloadFileOpenButton,ReloadFileSelectButton
    for Button in [Start,dataFileOpenButton,dataFileSelectButton,exit_button,ImportConfig_Button,ExportConfig_button,OutputFileOpenButton,OutputFileSelectButton,ReloadFileOpenButton,ReloadFileSelectButton]:
        Button.configure(state=ctk.DISABLED,fg_color="#7f8c8d",hover_color="#16a085")

def EnableButtons():
    global Start,dataFileOpenButton,dataFileSelectButton,exit_button,ImportConfig_Button,ExportConfig_button,OutputFileOpenButton,OutputFileSelectButton,ReloadFileOpenButton,ReloadFileSelectButton
    EnableStart()
    EnableExit()
    for Button in [dataFileOpenButton,dataFileSelectButton,ImportConfig_Button,ExportConfig_button,OutputFileOpenButton,OutputFileSelectButton,ReloadFileOpenButton,ReloadFileSelectButton]:
        Button.configure(state=ctk.NORMAL,fg_color=BUTTON_FG_COLOR,hover_color=BUTTON_HOVER_COLOR)

def Open_csv(filepath:str) -> None:
    global InputData,OutputData,ReloadInProgress
    try:
        InputData,OutputData = core.data.FormatCsv(filepath)
        ReloadInProgress = False
        EnableStart()
        Status_Label.configure(text="Ready")
        Display(Input_Param=InputData,Output_Param=OutputData,Predict_Param=OutputData,Error=0,GenNum=0,ProgramNum=0)
    except FileNotFoundError as err:
        messagebox.showerror(title="Data File Not Found",message=err)
    except Exception as err:
        messagebox.showerror(title="Unknown Exception Has Occured",message=err)

def Open_reload(filepath: str) -> None:
    global ReloadInProgress
    try:
        ReloadInProgress = True
        EnableStart()
        Status_Label.configure(text="Ready")
    except Exception as err:
        messagebox.showerror("Reload Failed", str(err))

def Open_input_file(filepath:str) -> None:
    if filepath.endswith(".csv"):
        Open_csv(filepath)
    elif filepath.endswith(".reload"):
        Open_reload(filepath)

def Select_input_file(dataFileEntry: ctk.CTkEntry) -> None:
    filepath = filedialog.askopenfilename(
        initialdir="./CSV/",
        title="Select Input File",
        defaultextension=".csv",
        filetypes=[("CSV File", "*.csv"),("Saved State","*.reload")]
    )
    dataFileEntry.delete(0, ctk.END)
    dataFileEntry.insert(0, filepath)
    Open_input_file(filepath)

def SetOutputFile(filepath:str):
    global pdfFILE
    if not filepath: 
        messagebox.showerror(title="Invalid File Name",message="File Name is not Valid.",detail="Please Give Another file name")
        pdfFILE = "Report"
        return
    pdfFILE = filepath

def Select_pdf(OutputFileEntry:ctk.CTkEntry):
    filepath:str = filedialog.asksaveasfilename(confirmoverwrite=True,filetypes=[("PDF File","*.pdf")],initialdir=".",initialfile="Report.pdf",title="Save Output As")
    filepath = filepath.rstrip(".pdf")
    OutputFileEntry.delete(0,ctk.END)
    OutputFileEntry.insert(0,filepath)
    SetOutputFile(filepath)

def SetReloadFile(filepath:str):
    global reloadFILE
    if not filepath: 
        messagebox.showerror(title="Invalid File Name",message="File Name is not Valid.",detail="Please Give Another file name")
        reloadFILE = "Report"
        return
    reloadFILE = filepath

def Select_reload(reloadFileEntry:ctk.CTkEntry):
    filepath:str = filedialog.asksaveasfilename(confirmoverwrite=True,filetypes=[("Saved State","*.reload")],initialdir=".",initialfile="Report.reload",title="Save State As")
    filepath = filepath.rstrip(".reload")
    reloadFileEntry.delete(0,ctk.END)
    reloadFileEntry.insert(0,filepath)
    SetOutputFile(filepath)

def ImportConfig() -> None:
    global pdfFILE
    filepath:str = filedialog.askopenfilename(title="Open Saved Configurations",defaultextension=".yaml",initialdir="./Config/",initialfile="Sample.yaml",filetypes=[("YAML File","*.yaml")])
    if not filepath:
        messagebox.showerror(title="Invalid File Name",message="File Name is not Valid.",detail="Please Give Another file name")
        return
    config:dict =core.config.import_config(filepath)
    Func_Set,pdfFILE,max_depth,gen_size,max_gen,xop,max_xo,mutp,max_mut,newp,max_new,verbose,_ = core.config.yamlInitialize(config)
    
    MaxDepth.delete(0,ctk.END)
    MaxDepth.insert(0,max_depth)

    Verbose.set(verbose)
    
    XOP.set(xop)
    UpdateSliderValue(XOP_Display,xop)
    MaxXO.delete(0,ctk.END)
    MaxXO.insert(0,max_xo)

    MUTP.set(mutp)
    UpdateSliderValue(MUTP_Display,mutp)
    MaxMut.delete(0,ctk.END)
    MaxMut.insert(0,max_mut)

    NEWP.set(newp)
    UpdateSliderValue(NEWP_Display,newp)
    MaxNew.delete(0,ctk.END)
    MaxNew.insert(0,max_new)

    GenSize.delete(0,ctk.END)
    GenSize.insert(0,gen_size)

    MaxGen.delete(0,ctk.END)
    MaxGen.insert(0,max_gen)

    OutputFile.delete(0,ctk.END)
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

def main() -> None :
    disabledList = [dataFileEntry,
                         MaxDepth,MaxGen,GenSize,VerboseBox,
                         MaxXO,MaxMut,MaxNew,
                         XOP_Slider,MUTP_Slider,NEWP_Slider,
                         FSET_R_Box,FSET_E_Box,FSET_L_Box,FSET_P_Box,FSET_T_Box,
                         OutputFile,ReloadFile]
    
    DisableButtons()
    for Every_Object in disabledList:
        Every_Object.configure(state=ctk.DISABLED)
    
    global InputData,OutputData,reloadFILE

    Status_Label.configure(text="Running...")
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
            Status_Label.configure(text="Correct your Configuration.")
            EnableButtons()
            for Every_Object in disabledList:
                Every_Object.configure(state=ctk.NORMAL)
            return
        config,MAX_DEPTH,GEN_SIZE,MAX_GEN,RELOADPROGRESS,_,Source_File,PDFFILE,FSET,Total_Error,Min_Error,Terminal_Set,Current_Gen = core.config.Initialize(["","--CONFIG:Temp.yaml",dataFileEntry.get()])
        os.remove("Temp.yaml")
    else: 
        config,MAX_DEPTH,GEN_SIZE,MAX_GEN,RELOADPROGRESS,_,Source_File,PDFFILE,FSET,Total_Error,Min_Error,Terminal_Set,Current_Gen = core.config.Initialize(["","-r",dataFileEntry.get()])
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

    for i in range(MAX_GEN):
        Status_Label.configure(text=f"Running Generation {i+1} of {MAX_GEN}")
        Current_Gen,Total_Error,Min_Error=Iterate(ThisGen=Current_Gen,GenNum=i,InputData=InputData,OutputData=OutputData,Total_Error=Total_Error,Min_Error=Min_Error,HyperParas=config,Terminal_Set=Terminal_Set,Union_List=Union_List,Display=Display)   #Main Generation Loop
    Current_Gen,Total_Error,Min_Error=Iterate(ThisGen=Current_Gen,GenNum=i,InputData=InputData,OutputData=OutputData,Total_Error=Total_Error,Min_Error=Min_Error,HyperParas=config,Terminal_Set=Terminal_Set,Union_List=Union_List,Display=Display)  #Display Last Generation
    Current_Gen.sort(key= lambda x:x.error)

    Status_Label.configure(text="Saving Reload Data,Compiling PDF...")
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
    Status_Label.configure(text="Report Saved.")
    EnableButtons()
    for Every_Object in disabledList:
        Every_Object.configure(state=ctk.NORMAL)


def run_gui():
    global root,reloadFILE,Table,dataFileEntry,dataFileOpenButton,dataFileSelectButton,MaxDepth,MaxGen,GenSize,MaxXO,XOP_Slider,MaxMut,MUTP_Slider,MaxNew,NEWP_Slider, \
        XOP,MUTP,NEWP,FSET_E,FSET_L,FSET_T,FSET_P,FSET_R,FSET_E_Box,FSET_L_Box,FSET_T_Box,FSET_P_Box,FSET_R_Box,Verbose,VerboseBox,OutputFile,XOP_Display,MUTP_Display,NEWP_Display, \
        pdfFILE,reloadFILE,ReloadFile,Start,Status_Label,ExportConfig_button,ImportConfig_Button,OutputFileOpenButton,OutputFileSelectButton,ReloadFileOpenButton,ReloadFileSelectButton, \
        exit_button
    reloadFILE = ""
    root = ctk.CTk()
    root.title("Genetic Program")
    root.iconbitmap("Logo.ico")
    root.geometry("1920x1080")
    root.attributes("-fullscreen", True)
    root.grid_rowconfigure(5, weight=1)
    root.grid_columnconfigure(5, weight=1) 
    root.grid_columnconfigure(9,weight=1)
    root.bind("<F11>", lambda e: root.attributes("-fullscreen", not root.attributes("-fullscreen")))

    ToggleThemeIcon = ctk.CTkImage(light_image=Image.open(".\\Icons\\ToggleTheme.png"),size=(32,32))
    ToggleTheme = ctk.CTkButton(root,text="Toggle Theme",image=ToggleThemeIcon,compound="right",fg_color=BUTTON_FG_COLOR,hover_color=BUTTON_HOVER_COLOR,text_color=BUTTON_TEXT_COLOR,text_color_disabled=BUTTON_TEXT_DISABLE_COLOR
                                       ,font=C_FONT,command=ToggleTheme_Func)
    ToggleTheme.grid(row=1,column=0,padx=10)
    CTkToolTip.CTkToolTip(ToggleTheme,message="Toggle Light/Dark Theme")

    dataFileFrame = ctk.CTkFrame(root, corner_radius=10, fg_color="transparent")
    dataFileFrame.grid(row=1,column=1,columnspan=7,padx=50)
    
    dataFileLabel = ctk.CTkLabel(dataFileFrame,text="Input Data: ",font=C_FONT)
    dataFileLabel.grid(row=0,column=0)

    dataFileEntry = ctk.CTkEntry(dataFileFrame,corner_radius=7,font=C_FONT,placeholder_text="Path to CSV or RELOAD File")
    dataFileEntry.grid(row=0,column=1,columnspan=5,ipadx=200)

    dataFileOpenIcon = ctk.CTkImage(light_image=Image.open(".\\Icons\\OpenFile.png"),size=(32,32))
    dataFileOpenButton = ctk.CTkButton(dataFileFrame,text="Open File",image=dataFileOpenIcon,compound="right",fg_color=BUTTON_FG_COLOR,hover_color=BUTTON_HOVER_COLOR,text_color=BUTTON_TEXT_COLOR,text_color_disabled=BUTTON_TEXT_DISABLE_COLOR
                                       ,font=C_FONT,command=lambda : Open_input_file(dataFileEntry.get()))
    dataFileOpenButton.grid(row=0,column=6,padx=10)
    CTkToolTip.CTkToolTip(dataFileOpenButton,message="Open Current File in Text Box")

    dataFileSelectIcon = ctk.CTkImage(light_image=Image.open(".\\Icons\\Browse.png"),size=(32,32))
    dataFileSelectButton = ctk.CTkButton(dataFileFrame,text="Browse",image=dataFileSelectIcon,compound="right",fg_color=BUTTON_FG_COLOR,hover_color=BUTTON_HOVER_COLOR,text_color=BUTTON_TEXT_COLOR,text_color_disabled=BUTTON_TEXT_DISABLE_COLOR
                                       ,font=C_FONT,command= lambda : Select_input_file(dataFileEntry) )
    dataFileSelectButton.grid(row=0,column=7)
    CTkToolTip.CTkToolTip(dataFileSelectButton,message="Browse For Data File")

    ControlsFrame = ctk.CTkFrame(root,fg_color="transparent")
    ControlsFrame.grid(row=1,column=10,columnspan=2,sticky="ne")
    
    fullscreen_Icon = ctk.CTkImage(light_image=Image.open(".\\Icons\\Fullscreen.png"),size=(32,32))
    fullscreen_button = ctk.CTkButton(ControlsFrame, text="",image=fullscreen_Icon,compound="right",width=40,height=40,fg_color=BUTTON_FG_COLOR,hover_color=BUTTON_HOVER_COLOR,text_color=BUTTON_TEXT_COLOR,text_color_disabled=BUTTON_TEXT_DISABLE_COLOR
                                       ,corner_radius=20,font=C_FONT, command=lambda : root.attributes("-fullscreen", not root.attributes("-fullscreen")))
    fullscreen_button.grid(row=1,column=8,sticky=ctk.E,padx=10,pady=20)
    CTkToolTip.CTkToolTip(fullscreen_button,message="Toggle Fullscreen")

    exitIcon = ctk.CTkImage(light_image=Image.open(".\\Icons\\Exit.png"),size=(32,32))
    exit_button = ctk.CTkButton(ControlsFrame,text="",image=exitIcon,compound="right",width=40,height=40,fg_color="#e74c3c",hover_color="#c0392b",text_color=BUTTON_TEXT_COLOR,text_color_disabled=BUTTON_TEXT_DISABLE_COLOR
                                       ,corner_radius=20,font=C_FONT,command=root.quit)
    exit_button.grid(row=1,column=9,sticky=ctk.E,pady=20)
    CTkToolTip.CTkToolTip(exit_button,message="Exit Program")

    HyperParasFrame = ctk.CTkFrame(root,border_width=2,corner_radius=10)
    HyperParasFrame.grid(row=2,column=0,pady=20,ipadx=10,ipady=10,rowspan=2,sticky=ctk.W)
    HyperParasLabel = ctk.CTkLabel(HyperParasFrame,text="Set Hyper Parameters",font=(C_FONT[0],14,"bold"))
    HyperParasLabel.grid(row=0,column=0,pady=5,padx=5,columnspan=2)

    MaxDepthLabel = ctk.CTkLabel(HyperParasFrame,text="Maximum Depth: ",font=C_FONT)
    MaxDepthLabel.grid(row=1,column=0,padx=5,pady=2)
    MaxDepth = ctk.CTkEntry(HyperParasFrame,font=C_FONT,corner_radius=7,placeholder_text="example: 4")
    MaxDepth.grid(row=1,column=1,pady=2)

    GenSizeLabel = ctk.CTkLabel(HyperParasFrame,text="Generation Size: ",font=C_FONT)
    GenSizeLabel.grid(row=2,column=0,padx=5,pady=2)
    GenSize = ctk.CTkEntry(HyperParasFrame,font=C_FONT,corner_radius=7,placeholder_text="example: 50")
    GenSize.grid(row=2,column=1,pady=2)
    
    MaxGenLabel = ctk.CTkLabel(HyperParasFrame,text="Maximum Generation: ",font=C_FONT)
    MaxGenLabel.grid(row=3,column=0,padx=5,pady=2)
    MaxGen = ctk.CTkEntry(HyperParasFrame,font=C_FONT,corner_radius=7,placeholder_text="example: 100")
    MaxGen.grid(row=3,column=1,padx=5,pady=2)

    XoverFrame = ctk.CTkFrame(HyperParasFrame,border_width=1,corner_radius=10,width=SUBFRAME_WIDTH,height=SUBFRAME_HEIGHT)
    XoverFrame.grid(row=4,column=0,columnspan=2,padx=5,pady=5)
    XoverFrame.grid_propagate(False)
    XoverLabel = ctk.CTkLabel(XoverFrame,text="Crossover",font=C_FONT)
    XoverLabel.grid(row=0,column=0,columnspan=2,pady=2,padx=10)

    MaxXO_Label = ctk.CTkLabel(XoverFrame,text="Maximum Crossovers: ",font=C_FONT)
    MaxXO_Label.grid(row=1,column=0,padx=10,pady=2, sticky="w")
    MaxXO = ctk.CTkEntry(XoverFrame,font=C_FONT,corner_radius=7,placeholder_text="e.g. 25(< Gen Size)")
    MaxXO.grid(row=1,column=1,pady=2,padx=5, sticky="ew")

    XOP = ctk.DoubleVar(value=0.0)
    XOP_Label = ctk.CTkLabel(XoverFrame,text="Crossover Probability",font=C_FONT)
    XOP_Label.grid(row=2,column=0,padx=10,pady=2, sticky="w")
    XOP_Display = ctk.CTkLabel(XoverFrame,text=XOP.get(),font=C_FONT)
    XOP_Display.grid(row=2,column=1,pady=2)
    XOP_Slider = ctk.CTkSlider(XoverFrame,from_=0,to=1,number_of_steps=100,orientation=ctk.HORIZONTAL,variable=XOP,
                               button_color=BUTTON_FG_COLOR,button_hover_color=BUTTON_HOVER_COLOR,
                               command= lambda Value : UpdateSliderValue(XOP_Display,Value))
    XOP_Slider.grid(row=3,column=0,columnspan=2,padx=50,pady=2, sticky="ew")

    MutFrame = ctk.CTkFrame(HyperParasFrame,border_width=1,corner_radius=10,width=SUBFRAME_WIDTH,height=SUBFRAME_HEIGHT)
    MutFrame.grid(row=5,column=0,columnspan=2,padx=5,pady=5)
    MutFrame.grid_propagate(False)
    MutLabel = ctk.CTkLabel(MutFrame,text="Mutation",font=C_FONT)
    MutLabel.grid(row=0,column=0,columnspan=2,pady=2,padx=10)

    MaxMut_Label = ctk.CTkLabel(MutFrame,text="Maximum Mutations: ",font=C_FONT)
    MaxMut_Label.grid(row=1,column=0,padx=10,pady=2, sticky="w")
    MaxMut = ctk.CTkEntry(MutFrame,font=C_FONT,corner_radius=7,placeholder_text="e.g. 20(< Gen Size)")
    MaxMut.grid(row=1,column=1,pady=2,padx=5, sticky="ew")

    MUTP = ctk.DoubleVar()
    MUTP_Label = ctk.CTkLabel(MutFrame,text="Mutation Probability",font=C_FONT)
    MUTP_Label.grid(row=2,column=0,padx=10,pady=2, sticky="w")
    MUTP_Display = ctk.CTkLabel(MutFrame,text=MUTP.get(),font=C_FONT)
    MUTP_Display.grid(row=2,column=1,pady=2)
    MUTP_Slider = ctk.CTkSlider(MutFrame,from_=0,to=1,number_of_steps=100,orientation=ctk.HORIZONTAL,variable=MUTP,
                               button_color=BUTTON_FG_COLOR,button_hover_color=BUTTON_HOVER_COLOR,
                               command= lambda Value : UpdateSliderValue(MUTP_Display,Value))
    MUTP_Slider.grid(row=3,column=0,columnspan=2,padx=50,pady=2, sticky="ew")

    NewFrame = ctk.CTkFrame(HyperParasFrame,border_width=1,corner_radius=10,width=SUBFRAME_WIDTH,height=SUBFRAME_HEIGHT)
    NewFrame.grid(row=6,column=0,columnspan=2,padx=10,pady=5)
    NewFrame.grid_propagate(False)
    NewLabel = ctk.CTkLabel(NewFrame,text="New Introduction",font=C_FONT)
    NewLabel.grid(row=0,column=0,columnspan=2,pady=2,padx=10)

    MaxNew_Label = ctk.CTkLabel(NewFrame,text="Maximum New Introduction: ",font=C_FONT)
    MaxNew_Label.grid(row=1,column=0,padx=10,pady=2, sticky="w")
    MaxNew = ctk.CTkEntry(NewFrame,font=C_FONT,corner_radius=7,placeholder_text="e.g. 5(<< Gen Size)")
    MaxNew.grid(row=1,column=1,pady=2,padx=5, sticky="ew")

    NEWP = ctk.DoubleVar()
    NEWP_Label = ctk.CTkLabel(NewFrame,text="New Introduction Probability",font=C_FONT)
    NEWP_Label.grid(row=2,column=0,padx=10,pady=2, sticky="w")
    NEWP_Display = ctk.CTkLabel(NewFrame,text=NEWP.get(),font=C_FONT)
    NEWP_Display.grid(row=2,column=1,pady=2)
    NEWP_Slider = ctk.CTkSlider(NewFrame,from_=0,to=1,number_of_steps=100,orientation=ctk.HORIZONTAL,width=212,variable=NEWP,
                               button_color=BUTTON_FG_COLOR,button_hover_color=BUTTON_HOVER_COLOR,
                               command= lambda Value : UpdateSliderValue(NEWP_Display,Value))
    NEWP_Slider.grid(row=3,column=0,columnspan=2,padx=50,pady=2, sticky="w")

    FSET_Frame = ctk.CTkFrame(HyperParasFrame,border_width=1,corner_radius=10,width=SUBFRAME_WIDTH,height=150)
    FSET_Frame.grid(row=7,column=0,columnspan=2,padx=10,pady=5)
    FSET_Frame.grid_propagate(False)
    FSET_Label = ctk.CTkLabel(FSET_Frame,text="Function Set",font=C_FONT)
    FSET_Label.grid(row=0,column=0,columnspan=2,pady=2,padx=10)

    FSET_M = ctk.BooleanVar(value=True)
    FSET_E = ctk.BooleanVar(value=False)
    FSET_L = ctk.BooleanVar(value=False)
    FSET_P = ctk.BooleanVar(value=False)
    FSET_R = ctk.BooleanVar(value=False)
    FSET_T = ctk.BooleanVar(value=False)
    
    FSET_M_Box = ctk.CTkCheckBox(FSET_Frame,text="Addition,Subtraction\nMultiplication,Division",variable=FSET_M,onvalue=True,offvalue=False,
                                 fg_color=BUTTON_FG_COLOR,hover_color=BUTTON_HOVER_COLOR,checkmark_color=BUTTON_TEXT_COLOR
                                 ,state=ctk.DISABLED,font=C_FONT,corner_radius=20)
    FSET_E_Box = ctk.CTkCheckBox(FSET_Frame,text="Power",variable=FSET_E,onvalue=True,offvalue=False,
                                 fg_color=BUTTON_FG_COLOR,hover_color=BUTTON_HOVER_COLOR,checkmark_color=BUTTON_TEXT_COLOR
                                 ,font=C_FONT,corner_radius=20)
    FSET_L_Box = ctk.CTkCheckBox(FSET_Frame,text="Logrithm and Exponentation",variable=FSET_L,onvalue=True,offvalue=False,
                                 fg_color=BUTTON_FG_COLOR,hover_color=BUTTON_HOVER_COLOR,checkmark_color=BUTTON_TEXT_COLOR
                                 ,font=C_FONT,corner_radius=20)
    FSET_P_Box = ctk.CTkCheckBox(FSET_Frame,text="Square and Cube",variable=FSET_P,onvalue=True,offvalue=False,
                                 fg_color=BUTTON_FG_COLOR,hover_color=BUTTON_HOVER_COLOR,checkmark_color=BUTTON_TEXT_COLOR
                                 ,font=C_FONT,corner_radius=20)
    FSET_R_Box = ctk.CTkCheckBox(FSET_Frame,text="Square root and Cube root",variable=FSET_R,onvalue=True,offvalue=False,
                                 fg_color=BUTTON_FG_COLOR,hover_color=BUTTON_HOVER_COLOR,checkmark_color=BUTTON_TEXT_COLOR
                                 ,font=C_FONT,corner_radius=20)
    FSET_T_Box = ctk.CTkCheckBox(FSET_Frame,text="sin,cos and tan",variable=FSET_T,onvalue=True,offvalue=False,
                                 fg_color=BUTTON_FG_COLOR,hover_color=BUTTON_HOVER_COLOR,checkmark_color=BUTTON_TEXT_COLOR
                                 ,font=C_FONT,corner_radius=20)
    
    FSET_M_Box.grid(row=1,column=0,pady=4,padx=5,sticky=ctk.W)
    FSET_E_Box.grid(row=1,column=1,pady=4,padx=5,sticky=ctk.W)
    FSET_L_Box.grid(row=3,column=0,pady=4,padx=5,sticky=ctk.W)
    FSET_P_Box.grid(row=2,column=1,pady=4,padx=5,sticky=ctk.W)
    FSET_R_Box.grid(row=2,column=0,pady=4,padx=5,sticky=ctk.W)
    FSET_T_Box.grid(row=3,column=1,pady=4,padx=5,sticky=ctk.W)

    Verbose = ctk.BooleanVar()
    VerboseBox = ctk.CTkCheckBox(HyperParasFrame,text="Verbose",variable=Verbose,onvalue=True,offvalue=False,
                                 fg_color=BUTTON_FG_COLOR,hover_color=BUTTON_HOVER_COLOR,checkmark_color=BUTTON_TEXT_COLOR
                                 ,font=C_FONT,corner_radius=20)
    VerboseBox.grid(row=8,column=0,pady=10,padx=5)

    ImportIcon = ctk.CTkImage(light_image=Image.open(".\\Icons\\Import_Style_1.png"),size=(32,32))
    ImportConfig_Button = ctk.CTkButton(HyperParasFrame,font=C_FONT,image=ImportIcon,compound="right",fg_color=BUTTON_FG_COLOR,hover_color=BUTTON_HOVER_COLOR,text_color=BUTTON_TEXT_COLOR,text_color_disabled=BUTTON_TEXT_DISABLE_COLOR
                                       ,text="Import Config",command=ImportConfig)
    ImportConfig_Button.grid(row=9,column=0,pady=10,padx=3)
    CTkToolTip.CTkToolTip(ImportConfig_Button,message="Import Hyper Parameters from YAML File")

    ExportIcon = ctk.CTkImage(light_image=Image.open(".\\Icons\\Export_Style_1.png"),size=(32,32))
    ExportConfig_button = ctk.CTkButton(HyperParasFrame,font=C_FONT,image=ExportIcon,compound="right",fg_color=BUTTON_FG_COLOR,hover_color=BUTTON_HOVER_COLOR,text_color=BUTTON_TEXT_COLOR,text_color_disabled=BUTTON_TEXT_DISABLE_COLOR
                                       ,text="Export Config",command=ExportConfig)
    ExportConfig_button.grid(row=9,column=1,pady=10,padx=3)
    CTkToolTip.CTkToolTip(ExportConfig_button,message="Export Current Hyper Parameters to YAML File")

    Table = ctk.CTkFrame(root,border_width=2,border_color=("#ffffff","#000000"),bg_color=("#000000","#ffffff"))
    Table.grid(row=2, column=5, rowspan=2, padx=10, pady=20)


    OutputFrame = ctk.CTkFrame(root,border_width=1,corner_radius=10)
    OutputFrame.grid(row=2,column=10,rowspan=2,pady=20,ipadx=10,ipady=10,sticky=ctk.E)
    OutputLabel = ctk.CTkLabel(OutputFrame,text="Output Details",font=(C_FONT[0],14,"bold"))
    OutputLabel.grid(row=0,column=0,pady=5,padx=5,columnspan=2)
    
    OutputFile_Label = ctk.CTkLabel(OutputFrame,text="Result: ",font=C_FONT)
    OutputFile_Label.grid(row=1,column=0,padx=5,pady=10)
    OutputFile = ctk.CTkEntry(OutputFrame,font=C_FONT,corner_radius=7,placeholder_text="Path to Report PDF")
    OutputFile.grid(row=1,column=1,pady=10,ipadx=35)
    OutputFileType_Label = ctk.CTkLabel(OutputFrame,text=".pdf",font=C_FONT)
    OutputFileType_Label.grid(row=1,column=2,pady=10,sticky=ctk.W)

    PDF_Icon = ctk.CTkImage(light_image=Image.open(".\\Icons\\pdfIcon.png"),size=(32,32))
    OutputFileOpenButton = ctk.CTkButton(OutputFrame,text="Set Path",image=PDF_Icon,compound="right",fg_color=BUTTON_FG_COLOR,hover_color=BUTTON_HOVER_COLOR,text_color=BUTTON_TEXT_COLOR,text_color_disabled=BUTTON_TEXT_DISABLE_COLOR
                                       ,font=C_FONT,command= lambda : SetOutputFile(OutputFile.get()))
    OutputFileOpenButton.grid(row=2,column=1,ipadx=30,pady=5)
    CTkToolTip.CTkToolTip(OutputFileOpenButton,message="Set Output PDF to current path")

    OutputFileSelectButton = ctk.CTkButton(OutputFrame,text="Browse",image=dataFileSelectIcon,compound="right",fg_color=BUTTON_FG_COLOR,hover_color=BUTTON_HOVER_COLOR,text_color=BUTTON_TEXT_COLOR,text_color_disabled=BUTTON_TEXT_DISABLE_COLOR
                                       ,font=C_FONT,command= lambda : Select_pdf(OutputFile))
    OutputFileSelectButton.grid(row=2,column=2,pady=5)
    CTkToolTip.CTkToolTip(OutputFileSelectButton,message="Save Output PDF as")

    ReloadFile_Label = ctk.CTkLabel(OutputFrame,text="Reload: ",font=C_FONT)
    ReloadFile_Label.grid(row=3,column=0,padx=5,pady=10)
    ReloadFile = ctk.CTkEntry(OutputFrame,font=C_FONT,corner_radius=7,placeholder_text="Path to Reload File")
    ReloadFile.grid(row=3,column=1,pady=10,ipadx=35)
    ReloadFileType_Label = ctk.CTkLabel(OutputFrame,text=".reload",font=C_FONT)
    ReloadFileType_Label.grid(row=3,column=2,pady=10,sticky=ctk.W)

    ReloadIcon = ctk.CTkImage(light_image=Image.open(".\\Icons\\ReloadIcon.png"),size=(32,32))
    ReloadFileOpenButton = ctk.CTkButton(OutputFrame,text="Set Path",image=ReloadIcon,compound="right",fg_color=BUTTON_FG_COLOR,hover_color=BUTTON_HOVER_COLOR,text_color=BUTTON_TEXT_COLOR,text_color_disabled=BUTTON_TEXT_DISABLE_COLOR
                                       ,font=C_FONT,command= lambda : SetReloadFile(ReloadFile.get()))
    ReloadFileOpenButton.grid(row=4,column=1,ipadx=30,pady=5)
    CTkToolTip.CTkToolTip(ReloadFileOpenButton,message="Set Output Reload to current path")

    ReloadFileSelectButton = ctk.CTkButton(OutputFrame,text="Browse",image=dataFileSelectIcon,compound="right",fg_color=BUTTON_FG_COLOR,hover_color=BUTTON_HOVER_COLOR,text_color=BUTTON_TEXT_COLOR,text_color_disabled=BUTTON_TEXT_DISABLE_COLOR
                                       ,font=C_FONT,command= lambda : Select_reload(ReloadFile))
    ReloadFileSelectButton.grid(row=4,column=2,pady=5)
    CTkToolTip.CTkToolTip(ReloadFileSelectButton,message="Save Output Reload as")

    BottomFrame = ctk.CTkFrame(root,fg_color="transparent")
    BottomFrame.grid(row=6, column=0, columnspan=12, sticky="ews")
    BottomFrame.grid_columnconfigure(0, weight=1)
    BottomFrame.grid_columnconfigure(1, weight=1)

    Status_Label = ctk.CTkLabel(BottomFrame,text="Open Data",font=C_FONT)
    Status_Label.grid(row=0,column=0,sticky=ctk.W)

    StartIcon = ctk.CTkImage(light_image=Image.open(".\\Icons\\StartOut.png"),size=(32,32))
    Start = ctk.CTkButton(BottomFrame,text="Start",image=StartIcon,compound="right",state=ctk.DISABLED,fg_color="#7f8c8d",hover_color="#34495e",text_color_disabled=BUTTON_TEXT_DISABLE_COLOR,text_color=BUTTON_TEXT_COLOR
                                       ,font=C_FONT,command=main)
    Start.grid(row=0,column=1,ipadx=10,sticky=ctk.E)
    CTkToolTip.CTkToolTip(Start,message="Start Genetic Program",y_offset=-20)


    root.mainloop()