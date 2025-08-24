"A Program to Run Several Subsequent Trials of Genetic Program"
#from GeneticProgram import yamlInitialize as YAML_INIT
import yaml
import sys
import os
from Integer_Helper import CheckWhetherStringIsIntegerOrFloat as CIF

Run_Count:int = 1
Config_File:str = ""
target_file:str = ""
PDFFile:str = "Report"
Arguments = sys.argv
for Argument in Arguments:
    if Argument.startswith("--CONFIG:"):
        Config_File:str = Argument[len("--CONFIG:")::]
    elif Argument.startswith("--COUNT:") and  (x := CIF(Argument[len("--COUNT:")::]))!="Null":
        Run_Count:int= x.__ceil__()
    else:
        target_file:str = Argument

try:
    with open(f"{Config_File}","r") as Yamlfile:
        Data = yaml.safe_load(Yamlfile)
        PDFFile:str = Data["RESULT"]
        #FSET,PDFFile,MAX_DEPTH,GENSIZE,MAXGEN,XOP,MAXXO,MUTP,MAXMUT,Verbose = YAML_INIT(Data)
        #del FSET,MAX_DEPTH,GENSIZE,MAXGEN,XOP,MAXXO,MUTP,MAXMUT,Verbose
except FileNotFoundError as err:
    for eta in range(0,Run_Count):
        os.system(f"python GeneticProgram.py --REPORT:{PDFFile}{eta+1} {target_file}")
    exit()

for eta in range(0,Run_Count):
    os.system(f"python GeneticProgram.py --CONFIG:{Config_File} -m --REPORT:{PDFFile}{eta+1} {target_file}")
    