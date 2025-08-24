"""Writes Result of Genetic Program to Tex File and Creates its PDF."""


from io import TextIOWrapper
import os
import GeneticProgram as GP

def PickSubTree(Code:GP.Program,FirstIndex:int) -> int:
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

def WriteTexEquation(Equation:list[GP.Node],Nested:bool = False) -> str:
    """
    Coverts Postfix Equation to a Latex Infix Equation
    """
    match Equation[0].symbol:

        case "+":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            LastIndex2:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=LastIndex+1)
            if not Nested:return f"{WriteTexEquation(Equation[1:LastIndex+1],Nested=True)} + {WriteTexEquation(Equation[LastIndex+1:LastIndex2+1],Nested=True)}"
            else: return f"({WriteTexEquation(Equation[1:LastIndex+1],Nested=True)} + {WriteTexEquation(Equation[LastIndex+1:LastIndex2+1],Nested=True)})"
        case "-":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            LastIndex2:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=LastIndex+1)
            if not Nested:return f"{WriteTexEquation(Equation[LastIndex+1:LastIndex2+1],Nested=True)} - {WriteTexEquation(Equation[1:LastIndex+1],Nested=True)}"
            else: return f"({WriteTexEquation(Equation[LastIndex+1:LastIndex2+1],Nested=True)} - {WriteTexEquation(Equation[1:LastIndex+1],Nested=True)})"
        case "*":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            LastIndex2:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=LastIndex+1)
            if not Nested:return f"{WriteTexEquation(Equation[1:LastIndex+1],Nested=True)} \\cdot {WriteTexEquation(Equation[LastIndex+1:LastIndex2+1],Nested=True)}"
            else: return f"({WriteTexEquation(Equation[1:LastIndex+1],Nested=True)} \\cdot {WriteTexEquation(Equation[LastIndex+1:LastIndex2+1],Nested=True)})"
        case "^":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            LastIndex2:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=LastIndex+1)
            if not Nested:return f"{{{WriteTexEquation(Equation[LastIndex+1:LastIndex2+1],Nested=True)}}} ^ {{{WriteTexEquation(Equation[1:LastIndex+1],Nested=True)}}}"
            else: return f"({{{WriteTexEquation(Equation[LastIndex+1:LastIndex2+1],Nested=True)}}} ^ {{{WriteTexEquation(Equation[1:LastIndex+1],Nested=True)}}})"
        case "/":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            LastIndex2:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=LastIndex+1)
            if not Nested:return f"\\frac{{{WriteTexEquation(Equation[LastIndex+1:LastIndex2+1],Nested=True)}}}{{{WriteTexEquation(Equation[1:LastIndex+1],Nested=True)}}} "
            else: return f"(\\frac{{{WriteTexEquation(Equation[LastIndex+1:LastIndex2+1],Nested=True)}}}{{{WriteTexEquation(Equation[1:LastIndex+1],Nested=True)}}})"
        case "S":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            if not Nested: return f"{WriteTexEquation(Equation[1:LastIndex+1],Nested=True)}^2"
            else: return f"({WriteTexEquation(Equation[1:LastIndex+1],Nested=True)}^2)"
        case "C":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            if not Nested: return f"{WriteTexEquation(Equation[1:LastIndex+1],Nested=True)}^3"
            else: return f"({WriteTexEquation(Equation[1:LastIndex+1],Nested=True)}^3)"
        case "R":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            if not Nested: return f"\\sqrt{{{WriteTexEquation(Equation[1:LastIndex+1],Nested=True)}}}"
            else: return f"\\sqrt{{{WriteTexEquation(Equation[1:LastIndex+1],Nested=True)}}}"
        case "T":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            if not Nested: return f"\\sqrt[3]{{{WriteTexEquation(Equation[1:LastIndex+1],Nested=True)}}}"
            else: return f"\\sqrt[3]{{{WriteTexEquation(Equation[1:LastIndex+1],Nested=True)}}}"
        case "$":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            if not Nested: return f"\\sin({{{WriteTexEquation(Equation[1:LastIndex+1],Nested=True)}}})"
            else: return f"\\sin({{{WriteTexEquation(Equation[1:LastIndex+1],Nested=True)}}})"
        case "&":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            if not Nested: return f"\\cos({{{WriteTexEquation(Equation[1:LastIndex+1],Nested=True)}}})"
            else: return f"\\cos({{{WriteTexEquation(Equation[1:LastIndex+1],Nested=True)}}})"
        case "@":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            if not Nested: return f"\\tan({{{WriteTexEquation(Equation[1:LastIndex+1],Nested=True)}}})"
            else: return f"\\tan({{{WriteTexEquation(Equation[1:LastIndex+1],Nested=True)}}})"
        case _:
            if Equation[0].symbol.startswith("var"): return f"X_{{{Equation[0].symbol[len("var")::]}}}" 
            return Equation[0].symbol
    
    return ""

def WriterPythonCode(Equation:list[GP.Node],CodeList:list[str],Depth:int=1) -> list[str]:
    '''
    Converts a Postfix Equation into a Function Code for Python 
    '''
    match Equation[0].symbol:

        case "+":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            LastIndex2:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=LastIndex+1)
            if LastIndex==1:
                Term_1 = Equation[1].symbol
            else:
                Term_1 = f"Step{(Depth*10)+1}"
                CodeList=WriterPythonCode(Equation[1:LastIndex+1],CodeList,(Depth*10)+1)
            if LastIndex2==LastIndex+1:
                Term_2 = Equation[LastIndex+1].symbol
            else:
                Term_2 = f"Step{(Depth*10)+2}"
                CodeList=WriterPythonCode(Equation[LastIndex+1:LastIndex2+1],CodeList,(Depth*10)+2)
            CodeList.append(f" Step{Depth} = {Term_1} + {Term_2}")
            return CodeList
        case "-":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            LastIndex2:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=LastIndex+1)
            if LastIndex==1:
                Term_1 = Equation[1].symbol
            else:
                Term_1 = f"Step{(Depth*10)+1}"
                CodeList=WriterPythonCode(Equation[1:LastIndex+1],CodeList,(Depth*10)+1)
            if LastIndex2==LastIndex+1:
                Term_2 = Equation[LastIndex+1].symbol
            else:
                Term_2 = f"Step{(Depth*10)+2}"
                CodeList=WriterPythonCode(Equation[LastIndex+1:LastIndex2+1],CodeList,(Depth*10)+2)
            CodeList.append(f" Step{Depth} = {Term_2} - {Term_1}")
            return CodeList
        case "*":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            LastIndex2:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=LastIndex+1)
            if LastIndex==1:
                Term_1 = Equation[1].symbol
            else:
                Term_1 = f"Step{(Depth*10)+1}"
                CodeList=WriterPythonCode(Equation[1:LastIndex+1],CodeList,(Depth*10)+1)
            if LastIndex2==LastIndex+1:
                Term_2 = Equation[LastIndex+1].symbol
            else:
                Term_2 = f"Step{(Depth*10)+2}"
                CodeList=WriterPythonCode(Equation[LastIndex+1:LastIndex2+1],CodeList,(Depth*10)+2)
            CodeList.append(f" Step{Depth} = {Term_1} * {Term_2}")
            return CodeList
        case "^":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            LastIndex2:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=LastIndex+1)
            if LastIndex==1:
                Term_1 = Equation[1].symbol
            else:
                Term_1 = f"Step{(Depth*10)+1}"
                CodeList=WriterPythonCode(Equation[1:LastIndex+1],CodeList,(Depth*10)+1)
            if LastIndex2==LastIndex+1:
                Term_2 = Equation[LastIndex+1].symbol
            else:
                Term_2 = f"Step{(Depth*10)+2}"
                CodeList=WriterPythonCode(Equation[LastIndex+1:LastIndex2+1],CodeList,(Depth*10)+2)
            CodeList.append(f" try: Step{Depth} = {Term_2} ** {Term_1}")
            CodeList.append(f" except OverflowError as err: Step{Depth} = 10000000")
            return CodeList
        case "/":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            LastIndex2:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=LastIndex+1)
            if LastIndex==1:
                Term_1 = Equation[1].symbol
            else:
                Term_1 = f"Step{(Depth*10)+1}"
                CodeList=WriterPythonCode(Equation[1:LastIndex+1],CodeList,(Depth*10)+1)
            if LastIndex2==LastIndex+1:
                Term_2 = Equation[LastIndex+1].symbol
            else:
                Term_2 = f"Step{(Depth*10)+2}"
                CodeList=WriterPythonCode(Equation[LastIndex+1:LastIndex2+1],CodeList,(Depth*10)+2)
            CodeList.append(f" try: Step{Depth} = {Term_2} / {Term_1}")
            CodeList.append(f" except ZeroDivisionError as err: Step{Depth} = 0")
            return CodeList
        case "S":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            if LastIndex==1:
                Term_1 = Equation[1].symbol
            else:
                Term_1 = f"Step{(Depth*10)+1}"
                CodeList=WriterPythonCode(Equation[1:LastIndex+1],CodeList,(Depth*10)+1)
            CodeList.append(f" Step{Depth} = {Term_1} ** 2")
            return CodeList
        case "C":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            if LastIndex==1:
                Term_1 = Equation[1].symbol
            else:
                Term_1 = f"Step{(Depth*10)+1}"
                CodeList=WriterPythonCode(Equation[1:LastIndex+1],CodeList,(Depth*10)+1)
            CodeList.append(f" Step{Depth} = {Term_1} ** 3")
            return CodeList
        case "R":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            if LastIndex==1:
                Term_1 = Equation[1].symbol
            else:
                Term_1 = f"Step{(Depth*10)+1}"
                CodeList=WriterPythonCode(Equation[1:LastIndex+1],CodeList,(Depth*10)+1)
            CodeList.append(f" try: Step{Depth} = math.sqrt({Term_1})")
            CodeList.append(f" except ValueError as err: Step{Depth} = {Term_1}")
            return CodeList
        case "T":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            if LastIndex==1:
                Term_1 = Equation[1].symbol
            else:
                Term_1 = f"Step{(Depth*10)+1}"
                CodeList=WriterPythonCode(Equation[1:LastIndex+1],CodeList,(Depth*10)+1)
            CodeList.append(f" Step{Depth} = math.cbrt({Term_1})")
            return CodeList
        case "$":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            if LastIndex==1:
                Term_1 = Equation[1].symbol
            else:
                Term_1 = f"Step{(Depth*10)+1}"
                CodeList=WriterPythonCode(Equation[1:LastIndex+1],CodeList,(Depth*10)+1)
            CodeList.append(f" try: Step{Depth} = math.sin({Term_1})")
            CodeList.append(f" except ValueError as err: Step{Depth} = 0")
            return CodeList
        case "&":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            if LastIndex==1:
                Term_1 = Equation[1].symbol
            else:
                Term_1 = f"Step{(Depth*10)+1}"
                CodeList=WriterPythonCode(Equation[1:LastIndex+1],CodeList,(Depth*10)+1)
            if Depth==0: CodeList.append(f' return Step_{Depth}')
            CodeList.append(f" try: Step{Depth} = math.cos({Term_1})")
            CodeList.append(f" except ValueError as err: Step{Depth} = 1")
            return CodeList
        case "@":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            if LastIndex==1:
                Term_1 = Equation[1].symbol
            else:
                Term_1 = f"Step{(Depth*10)+1}"
                CodeList=WriterPythonCode(Equation[1:LastIndex+1],CodeList,(Depth*10)+1)
            CodeList.append(f" try: Step{Depth} = math.tan({Term_1})")
            CodeList.append(f" except ValueError as err: Step{Depth} = 0")
            return CodeList
        case _:
            return [f" Step{Depth} = {Equation[0].symbol}"]

def WriterC_Code(Equation:list[GP.Node],CodeList:list[str],Depth:int=1) -> list[str]:
    '''
    Converts a Postfix Equation into a Function Code for C/C++
    '''
    match Equation[0].symbol:

        case "+":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            LastIndex2:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=LastIndex+1)
            if LastIndex==1:
                Term_1 = Equation[1].symbol
            else:
                Term_1 = f"Step{(Depth*10)+1}"
                CodeList=WriterC_Code(Equation[1:LastIndex+1],CodeList,(Depth*10)+1)
            if LastIndex2==LastIndex+1:
                Term_2 = Equation[LastIndex+1].symbol
            else:
                Term_2 = f"Step{(Depth*10)+2}"
                CodeList=WriterC_Code(Equation[LastIndex+1:LastIndex2+1],CodeList,(Depth*10)+2)
            CodeList.append(f" double Step{Depth} = {Term_1} + {Term_2};")
            return CodeList
        case "-":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            LastIndex2:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=LastIndex+1)
            if LastIndex==1:
                Term_1 = Equation[1].symbol
            else:
                Term_1 = f"Step{(Depth*10)+1}"
                CodeList=WriterC_Code(Equation[1:LastIndex+1],CodeList,(Depth*10)+1)
            if LastIndex2==LastIndex+1:
                Term_2 = Equation[LastIndex+1].symbol
            else:
                Term_2 = f"Step{(Depth*10)+2}"
                CodeList=WriterC_Code(Equation[LastIndex+1:LastIndex2+1],CodeList,(Depth*10)+2)
            CodeList.append(f" double Step{Depth} = {Term_2} - {Term_1};")
            return CodeList
        case "*":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            LastIndex2:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=LastIndex+1)
            if LastIndex==1:
                Term_1 = Equation[1].symbol
            else:
                Term_1 = f"Step{(Depth*10)+1}"
                CodeList=WriterC_Code(Equation[1:LastIndex+1],CodeList,(Depth*10)+1)
            if LastIndex2==LastIndex+1:
                Term_2 = Equation[LastIndex+1].symbol
            else:
                Term_2 = f"Step{(Depth*10)+2}"
                CodeList=WriterC_Code(Equation[LastIndex+1:LastIndex2+1],CodeList,(Depth*10)+2)
            CodeList.append(f" double Step{Depth} = {Term_1} * {Term_2};")
            return CodeList
        case "^":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            LastIndex2:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=LastIndex+1)
            if LastIndex==1:
                Term_1 = Equation[1].symbol
            else:
                Term_1 = f"Step{(Depth*10)+1}"
                CodeList=WriterC_Code(Equation[1:LastIndex+1],CodeList,(Depth*10)+1)
            if LastIndex2==LastIndex+1:
                Term_2 = Equation[LastIndex+1].symbol
            else:
                Term_2 = f"Step{(Depth*10)+2}"
                CodeList=WriterC_Code(Equation[LastIndex+1:LastIndex2+1],CodeList,(Depth*10)+2)
            CodeList.append(f" double Step{Depth} = pow({Term_2}, {Term_1});")
            #CodeList.append(f" except OverflowError as err: Step{Depth} = 10000000")
            return CodeList
        case "/":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            LastIndex2:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=LastIndex+1)
            if LastIndex==1:
                Term_1 = Equation[1].symbol
            else:
                Term_1 = f"Step{(Depth*10)+1}"
                CodeList=WriterC_Code(Equation[1:LastIndex+1],CodeList,(Depth*10)+1)
            if LastIndex2==LastIndex+1:
                Term_2 = Equation[LastIndex+1].symbol
            else:
                Term_2 = f"Step{(Depth*10)+2}"
                CodeList=WriterC_Code(Equation[LastIndex+1:LastIndex2+1],CodeList,(Depth*10)+2)
            CodeList.append(f" double Step{Depth} = {Term_2} / {Term_1};")
            #CodeList.append(f" except ZeroDivisionError as err: Step{Depth} = 0")
            return CodeList
        case "S":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            if LastIndex==1:
                Term_1 = Equation[1].symbol
            else:
                Term_1 = f"Step{(Depth*10)+1}"
                CodeList=WriterC_Code(Equation[1:LastIndex+1],CodeList,(Depth*10)+1)
            CodeList.append(f" double Step{Depth} = {Term_1} * {Term_1};")
            return CodeList
        case "C":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            if LastIndex==1:
                Term_1 = Equation[1].symbol
            else:
                Term_1 = f"Step{(Depth*10)+1}"
                CodeList=WriterC_Code(Equation[1:LastIndex+1],CodeList,(Depth*10)+1)
            CodeList.append(f" double Step{Depth} = {Term_1} * {Term_1} * {Term_1};")
            return CodeList
        case "R":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            if LastIndex==1:
                Term_1 = Equation[1].symbol
            else:
                Term_1 = f"Step{(Depth*10)+1}"
                CodeList=WriterC_Code(Equation[1:LastIndex+1],CodeList,(Depth*10)+1)
            CodeList.append(f" double Step{Depth} = sqrt({Term_1});")
            #CodeList.append(f" except ValueError as err: Step{Depth} = {Term_1}")
            return CodeList
        case "T":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            if LastIndex==1:
                Term_1 = Equation[1].symbol
            else:
                Term_1 = f"Step{(Depth*10)+1}"
                CodeList=WriterC_Code(Equation[1:LastIndex+1],CodeList,(Depth*10)+1)
            CodeList.append(f" double Step{Depth} = cbrt({Term_1});")
            return CodeList
        case "$":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            if LastIndex==1:
                Term_1 = Equation[1].symbol
            else:
                Term_1 = f"Step{(Depth*10)+1}"
                CodeList=WriterC_Code(Equation[1:LastIndex+1],CodeList,(Depth*10)+1)
            CodeList.append(f" double Step{Depth} = sin({Term_1});")
            #CodeList.append(f" except ValueError as err: Step{Depth} = 0")
            return CodeList
        case "&":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            if LastIndex==1:
                Term_1 = Equation[1].symbol
            else:
                Term_1 = f"Step{(Depth*10)+1}"
                CodeList=WriterC_Code(Equation[1:LastIndex+1],CodeList,(Depth*10)+1)
            if Depth==0: CodeList.append(f' return Step_{Depth}')
            CodeList.append(f" double Step{Depth} = cos({Term_1});")
            #CodeList.append(f" except ValueError as err: Step{Depth} = 1")
            return CodeList
        case "@":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            if LastIndex==1:
                Term_1 = Equation[1].symbol
            else:
                Term_1 = f"Step{(Depth*10)+1}"
                CodeList=WriterC_Code(Equation[1:LastIndex+1],CodeList,(Depth*10)+1)
            CodeList.append(f" double Step{Depth} = tan({Term_1});")
            #CodeList.append(f" except ValueError as err: Step{Depth} = 0")
            return CodeList
        case _:
            return [f" double Step{Depth} = {Equation[0].symbol}"]

def DescribeEq(TargetFile:TextIOWrapper,Equation: list[GP.Node],InputData:list[list[int|float]],Req_Output:list[int|float],Pre_Output:list[int|float],i:int,ProgramError:int|float) -> None:
    """
    Writes Predicted Result Table and Equation to Tex File
    """
    
    TexEquation:str = WriteTexEquation(Equation=Equation)
    TargetFile.write(f'''\\section{{Result For Best Performance No. {i}}}''')
    TargetFile.write('''
\\subsection{Data}
The Genetic Program Was Executed On Following Data
\n
'''    #\\begin{table}[h]
                     '''
        \\begin{center}
        \\begin{longtable}{|c|c|c|c|}
            \\hline
            No. & Input Data & Output Data & Predicted Data  \\\\
            \\hline\n''')
    for j,Value in enumerate(start=1,iterable=InputData):
            TargetFile.write(f"            {j}. & {Value} & {Req_Output[j-1]} & {Pre_Output[j-1]} \\\\\n            \\hline\n")
    TargetFile.write(
    f'''            
            \\caption{{Given Data With Best Prediction.}} 
            \\label{{tab:data{i}}}       
        \\end{{longtable}}
        \\end{{center}}
''')               
#\\end{{table}}''')
    TargetFile.write('''
\\subsection{Equation}
The Equation with minimum error was''')
    if len(Equation) >10 : TargetFile.write(f"\\begin{{equation}}\n\\resizebox{{0.95\\linewidth}}{{!}}{{$\nY={TexEquation}\n$}}\n\\end{{equation}}\n\nWith a Minimum Error of {ProgramError}\n")
    else: TargetFile.write(f"\\[\nY={TexEquation}\\]\n\nWith a Minimum Error of {ProgramError}\n")

def Create(filepath:str,equation: list[list[GP.Node]],NumberOfCode:int,TotalError:list[float],ErrorList:list[int|float],MinError:list[float],Input:list[list[int|float]],Output:list[int|float],Predict:list[list[int|float]],HParams:dict) -> None:
    """
    Creates a Tex File for the execution of 
    Genetic Program and Compile into PDF File.
    """
    
    with open(f"{filepath}.tex","w") as TexFile:
        TexFile.write('''\\documentclass{article}
\\usepackage{amsmath}
\\usepackage{longtable}
\\usepackage{graphicx}
\\usepackage{minted}
                      
\\title{Report On Genetic Programs Execution}
\\author{Mustufa Ghadiyali}
\\date{\\today}
\\begin{document}
\\definecolor{cbg}{rgb}{0.1,0.1,0.3}
\\definecolor{pygb}{rgb}{0.02,0.02,0.05}
\\setminted[python3]{style=rrt,bgcolor=pygb}
\\setminted[c]{style=fruity,bgcolor=cbg}
\\maketitle
An Auto Generated Report for the Execution\n and Operation of Genetic Program
\\newpage
\\tableofcontents
\\newpage''')
        TexFile.write(f'''
\\section{{Values of Hyper Parameters}}
The Values of Hyper Parameters Were set as Follow for this run of\nGenetic Program.
\\begin{{itemize}}
    \\item Maximum Depth of Equation Tree = {HParams["MAXDEPTH"]}
    \\item Maximum Size of Generation = {HParams["GENSIZE"]}
    \\item Maximum Number of Generation = {HParams["MAXGEN"]}
    \\item Crossover Probability = {HParams["XOP"]}
    \\item Maximum Crossover per Generation = {HParams["MAXXO"]}
    \\item Mutation Probability = {HParams["MUTP"]}    
    \\item Maximum Mutation per Generation = {HParams["MAXMUT"]}
    \\item Verbose Output = {HParams["VERBOSE"]}
    \\item Function Set = {HParams["FSET"]} 
\\end{{itemize}}
''')

        for i in range(len(equation)): 
            DescribeEq(TargetFile=TexFile,Equation=equation[i],i=(i+1),InputData=Input,Req_Output=Output,Pre_Output=Predict[i],ProgramError=ErrorList[i])
            Program:list[str]=WriterPythonCode(Equation=equation[i],CodeList=[])
            Param_list = [f"var{para_num+1}" for para_num in range(len(Input[0]))]
            Header:str = "def func("+ ",".join(Param_list) + "):"
            Return_Statement = " return Step1"
            Program.insert(0,Header)
            Program.append(Return_Statement)
            TexFile.write('''\\subsection{Python Code}

\\begin{minted}{python3}
''')
            for line in Program:
                TexFile.write(line + '\n')
            TexFile.write("\\end{minted}\n")

            Program:list[str]=WriterC_Code(Equation=equation[i],CodeList=[])
            Param_list = [f"double var{para_num+1}" for para_num in range(len(Input[0]))]
            Header:str = "double func("+ ",".join(Param_list) + "){"
            Return_Statement = ''' return Step1;
}'''
            Program.insert(0,Header)
            Program.append(Return_Statement)
            TexFile.write('''\\subsection{C/C++ Code}

\\begin{minted}{c}
''')
            for line in Program:
                TexFile.write(line + '\n')
            TexFile.write("\\end{minted}\n")
        #TexFile.write('''
#\\section{Data}
#The Genetic Program Was Executed On Following Data
#\n
#\\begin{table}[h]
#    \\centering
#    \\begin{tabular}{|c|c|c|c|}
#        \\hline
#        No. & Input Data & Output Data & Predicted Data  \\\\
#        \\hline\n''')
#        for i,Value in enumerate(start=1,iterable=Input):
#            TexFile.write(f"{i}. & {Value} & {Output[i-1]} & {Predict[i-1]} \\\\\n\\hline\n")
#        TexFile.write(
#   '''\\end{tabular}
#    \\caption{Given Data With Best Prediction.}
#    \\label{tab:data}
#\\end{table}''')
#        TexFile.write('''
#\\section{Equation}
#The Equation with minimum error was''')
#       TexFile.write(f"\\[Y={TexEquation}\\]\\\\\n\nWith a Minimum Error of {MinError[-1]}\n")
        TexFile.write('''\\section{Error Table}
    \\centering
    \\begin{longtable}{|c|c|c|c|}
        \\hline
        Gen No. & Total Error & Average Error & Min Error  \\\\
        \\hline\n''')
        for i,Value in enumerate(start=1,iterable=TotalError):
            TexFile.write(f"Gen {i} & {Value} & {Value/NumberOfCode} & {MinError[i-1]} \\\\\n\\hline\n")
        TexFile.write(
    '''
\\caption{Generation wise Total,Average and Minimum Error.}
\\label{tab:errors}
\\end{longtable}\n''')
        TexFile.write("\\end{document}")
    os.system(f"pdflatex {filepath}.tex")
    os.system(f"pdflatex {filepath}.tex")


if __name__ == "__main__":
    Plus:GP.Node = GP.Node("+",2)
    Minus:GP.Node = GP.Node("-",2)
    Mul:GP.Node = GP.Node("*",2)
    Divide:GP.Node = GP.Node("/",2)
    Function_Set: list[GP.Node] =[Plus,Minus,Mul,Divide]
    Num9:GP.Node = GP.Node("9")
    Var1:GP.Node = GP.Node("var1")
    # GP.Terminal_Set = [GP.Node("Const")]
    #for i in range(1,2):
    #    GP.Terminal_Set.append(GP.Node(f"var{i}"))
    
    Equation:list[GP.Node] = [Plus,Var1,Num9]
    print(WriterPythonCode(Equation,[]))
    '''GP.Union_List= Function_Set + GP.Terminal_Set
    GP.MAX_DEPTH = 2
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
    Master:bool = False
    filename:str = input("File Name: ")
    SomeList: list[GP.Node] = [Divide,Mul,GP.Terminal_Set[1],GP.Terminal_Set[0],GP.Node("5")]
    config = {"RESULT":PDFfile,"MAXDEPTH":max_depth,"GENSIZE":gen_size,"MAXGEN":max_gen,"XOP":xop,"MAXXO":max_xo,"MUTP":mutp,"MAXMUT":max_mut,"VERBOSE":verbose,"FSET":Fset}
    #Create(filepath=filename,equation=GP.Program.RandomCode(S=Plus,Depth=1))
    #Create(filepath="Sample",equation=[SomeList],NumberOfCode=1,TotalError=[1,2,3,4,5,6],MinError=[0,1,2,3,4,5],Input=[[1],[2],[3],[4]],Output=[2,3,4,5],Predict=[[2,3,4,5]],ErrorList=[0],HParams={})
    os.system(f"pdflatex {filename}.tex")'''