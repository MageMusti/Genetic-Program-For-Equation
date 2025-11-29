"""Writes Result of Genetic Program to Tex File and Creates its PDF."""


from io import TextIOWrapper
import os
import core.programs as GP
import matplotlib.pyplot as plt
import numpy as np
import math
from typing import Any

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
        for _ in range(Code.code[FirstIndex].Terminal):
            LastIndex=PickSubTree(Code=Code,FirstIndex=(LastIndex+1))
    return LastIndex

def WriteTexEquation(Equation:list[Any],Nested:bool = False,HasPower:bool=False) -> str:
    """
    Coverts Postfix Equation to a Latex Infix Equation
    """
    match Equation[0].symbol:

        case "+":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            LastIndex2:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=LastIndex+1)
            if not Nested:return f"{WriteTexEquation(Equation[1:LastIndex+1],Nested=False)} + {WriteTexEquation(Equation[LastIndex+1:LastIndex2+1],Nested=False)}"
            else: return f"({WriteTexEquation(Equation[1:LastIndex+1],Nested=False)} + {WriteTexEquation(Equation[LastIndex+1:LastIndex2+1],Nested=False)})"
        case "-":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            LastIndex2:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=LastIndex+1)
            if not Nested:return f"{WriteTexEquation(Equation[LastIndex+1:LastIndex2+1],Nested=True)} - {WriteTexEquation(Equation[1:LastIndex+1],Nested=True)}"
            else: return f"({WriteTexEquation(Equation[LastIndex+1:LastIndex2+1],Nested=True)} - {WriteTexEquation(Equation[1:LastIndex+1],Nested=True)})"
        case "*":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            LastIndex2:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=LastIndex+1)
            if not HasPower:return f"{WriteTexEquation(Equation[1:LastIndex+1],Nested=True)} \\cdot {WriteTexEquation(Equation[LastIndex+1:LastIndex2+1],Nested=True)}"
            else: return f"({WriteTexEquation(Equation[1:LastIndex+1],Nested=True)} \\cdot {WriteTexEquation(Equation[LastIndex+1:LastIndex2+1],Nested=True)})"
        case "^":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            LastIndex2:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=LastIndex+1)
            if not Nested:return f"{{{WriteTexEquation(Equation[LastIndex+1:LastIndex2+1],Nested=True,HasPower=True)}}} ^ {{{WriteTexEquation(Equation[1:LastIndex+1],Nested=True)}}}"
            elif HasPower:return f"{{{{{WriteTexEquation(Equation[LastIndex+1:LastIndex2+1],Nested=True,HasPower=True)}}} ^ {{{WriteTexEquation(Equation[1:LastIndex+1],Nested=True)}}}}}"
            else: return f"{{{WriteTexEquation(Equation[LastIndex+1:LastIndex2+1],Nested=True,HasPower=True)}}} ^ {{({WriteTexEquation(Equation[1:LastIndex+1],Nested=True)})}}"
        case "/":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            LastIndex2:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=LastIndex+1)
            if not HasPower:return f"\\frac{{{WriteTexEquation(Equation[LastIndex+1:LastIndex2+1],Nested=True)}}}{{{WriteTexEquation(Equation[1:LastIndex+1],Nested=True)}}}"
            else: return f"(\\frac{{{WriteTexEquation(Equation[LastIndex+1:LastIndex2+1],Nested=True)}}}{{{WriteTexEquation(Equation[1:LastIndex+1],Nested=True)}}})"
        case "S":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            if not HasPower: return f"{WriteTexEquation(Equation[1:LastIndex+1],Nested=True,HasPower=True)}^2"
            else: return f"({WriteTexEquation(Equation[1:LastIndex+1],Nested=True,HasPower=True)}^{{2}})"
        case "C":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            if not HasPower: return f"{WriteTexEquation(Equation[1:LastIndex+1],Nested=True,HasPower=True)}^3"
            else: return f"({WriteTexEquation(Equation[1:LastIndex+1],Nested=True,HasPower=True)}^{{3}})"
        case "R":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            if not Nested: return f"\\sqrt{{{WriteTexEquation(Equation[1:LastIndex+1],Nested=False)}}}"
            else: return f"\\sqrt{{{WriteTexEquation(Equation[1:LastIndex+1],Nested=False)}}}"
        case "T":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            if not Nested: return f"\\sqrt[3]{{{WriteTexEquation(Equation[1:LastIndex+1],Nested=False)}}}"
            else: return f"\\sqrt[3]{{{WriteTexEquation(Equation[1:LastIndex+1],Nested=False)}}}"
        case "$":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            if not Nested: return f"\\sin({{{WriteTexEquation(Equation[1:LastIndex+1],Nested=False)}}})"
            else: return f"\\sin({{{WriteTexEquation(Equation[1:LastIndex+1],Nested=False)}}})"
        case "&":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            if not Nested: return f"\\cos({{{WriteTexEquation(Equation[1:LastIndex+1],Nested=False)}}})"
            else: return f"\\cos({{{WriteTexEquation(Equation[1:LastIndex+1],Nested=False)}}})"
        case "@":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            if not Nested: return f"\\tan({{{WriteTexEquation(Equation[1:LastIndex+1],Nested=False)}}})"
            else: return f"\\tan({{{WriteTexEquation(Equation[1:LastIndex+1],Nested=False)}}})"
        case "E":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            if not HasPower: return f"e^{{{WriteTexEquation(Equation[1:LastIndex+1],Nested=False)}}}"
            else: return f"{{e^{{({WriteTexEquation(Equation[1:LastIndex+1],Nested=False)})}}}}"
        case "L":
            
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            if not Nested: return f"\\ln({{{WriteTexEquation(Equation[1:LastIndex+1],Nested=False)}}})"
            else: return f"\\ln({{{WriteTexEquation(Equation[1:LastIndex+1],Nested=False)}}})"
        case _:
            if Equation[0].symbol.startswith("var"): return f"X_{{{Equation[0].symbol[len("var")::]}}}"
            if float(Equation[0].symbol) < 0 and (Nested or HasPower): return f"({Equation[0].symbol})"
            return Equation[0].symbol
    
    return ""

def HandleNegativeConstant(Term:str) -> str:
    """
    Add parenthesis Around Negative Constants in Equations
    else Returns the Term as it is.
    """
    Value = GP.CIF(Term)
    if Value=="Null" or Value>=0: return Term
    else: return f'({Term})'

def WriterPythonCode(Equation:list[Any],CodeList:list[str],Depth:int=1) -> list[str]:
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
                Term_1 = f"Step{(Depth*2)+1}"
                CodeList=WriterPythonCode(Equation[1:LastIndex+1],CodeList,(Depth*2)+1)
            if LastIndex2==LastIndex+1:
                Term_2 = Equation[LastIndex+1].symbol
            else:
                Term_2 = f"Step{(Depth*2)+2}"
                CodeList=WriterPythonCode(Equation[LastIndex+1:LastIndex2+1],CodeList,(Depth*2)+2)
            CodeList.append(f" Step{Depth} = {Term_1} + {Term_2}")
            return CodeList
        case "-":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            LastIndex2:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=LastIndex+1)
            if LastIndex==1:
                Term_1 = Equation[1].symbol
            else:
                Term_1 = f"Step{(Depth*2)+1}"
                CodeList=WriterPythonCode(Equation[1:LastIndex+1],CodeList,(Depth*2)+1)
            if LastIndex2==LastIndex+1:
                Term_2 = Equation[LastIndex+1].symbol
            else:
                Term_2 = f"Step{(Depth*2)+2}"
                CodeList=WriterPythonCode(Equation[LastIndex+1:LastIndex2+1],CodeList,(Depth*2)+2)
            CodeList.append(f" Step{Depth} = {Term_2} - {Term_1}")
            return CodeList
        case "*":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            LastIndex2:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=LastIndex+1)
            if LastIndex==1:
                Term_1 = Equation[1].symbol
            else:
                Term_1 = f"Step{(Depth*2)+1}"
                CodeList=WriterPythonCode(Equation[1:LastIndex+1],CodeList,(Depth*2)+1)
            if LastIndex2==LastIndex+1:
                Term_2 = Equation[LastIndex+1].symbol
            else:
                Term_2 = f"Step{(Depth*2)+2}"
                CodeList=WriterPythonCode(Equation[LastIndex+1:LastIndex2+1],CodeList,(Depth*2)+2)
            CodeList.append(f" Step{Depth} = {Term_1} * {Term_2}")
            return CodeList
        case "^":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            LastIndex2:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=LastIndex+1)
            if LastIndex==1:
                Term_1 = Equation[1].symbol
            else:
                Term_1 = f"Step{(Depth*2)+1}"
                CodeList=WriterPythonCode(Equation[1:LastIndex+1],CodeList,(Depth*2)+1)
            if LastIndex2==LastIndex+1:
                Term_2 = Equation[LastIndex+1].symbol
                Term_2 = HandleNegativeConstant(Term_2)
            else:
                Term_2 = f"Step{(Depth*2)+2}"
                CodeList=WriterPythonCode(Equation[LastIndex+1:LastIndex2+1],CodeList,(Depth*2)+2)
            CodeList.append(f" try: Step{Depth} = {Term_2} ** {Term_1}")
            CodeList.append(f" except OverflowError as err: Step{Depth} = 10000000")
            CodeList.append(f" except ZeroDivisionError as err: Step{Depth} = 0")
            CodeList.append(f" if isinstance(Step{Depth},complex): Step{Depth} = 0")
            return CodeList
        case "/":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            LastIndex2:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=LastIndex+1)
            if LastIndex==1:
                Term_1 = Equation[1].symbol
            else:
                Term_1 = f"Step{(Depth*2)+1}"
                CodeList=WriterPythonCode(Equation[1:LastIndex+1],CodeList,(Depth*2)+1)
            if LastIndex2==LastIndex+1:
                Term_2 = Equation[LastIndex+1].symbol
            else:
                Term_2 = f"Step{(Depth*2)+2}"
                CodeList=WriterPythonCode(Equation[LastIndex+1:LastIndex2+1],CodeList,(Depth*2)+2)
            CodeList.append(f" try: Step{Depth} = {Term_2} / {Term_1}")
            CodeList.append(f" except ZeroDivisionError as err: Step{Depth} = 0")
            return CodeList
        case "S":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            if LastIndex==1:
                Term_1 = Equation[1].symbol
                Term_1 = HandleNegativeConstant(Term_1)
            else:
                Term_1 = f"Step{(Depth*2)+1}"
                CodeList=WriterPythonCode(Equation[1:LastIndex+1],CodeList,(Depth*2)+1)
            CodeList.append(f" try: Step{Depth} = {Term_1} ** 2")
            CodeList.append(f" except OverflowError as err: Step{Depth} = 10000000")
            return CodeList
        case "C":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            if LastIndex==1:
                Term_1 = Equation[1].symbol
            else:
                Term_1 = f"Step{(Depth*2)+1}"
                CodeList=WriterPythonCode(Equation[1:LastIndex+1],CodeList,(Depth*2)+1)
            CodeList.append(f" try: Step{Depth} = {Term_1} ** 3")
            CodeList.append(f" except OverflowError as err: Step{Depth} = 10000000")
            return CodeList
        case "R":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            if LastIndex==1:
                Term_1 = Equation[1].symbol
            else:
                Term_1 = f"Step{(Depth*2)+1}"
                CodeList=WriterPythonCode(Equation[1:LastIndex+1],CodeList,(Depth*2)+1)
            CodeList.append(f" try: Step{Depth} = math.sqrt({Term_1})")
            CodeList.append(f" except ValueError as err: Step{Depth} = {Term_1}")
            return CodeList
        case "T":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            if LastIndex==1:
                Term_1 = Equation[1].symbol
            else:
                Term_1 = f"Step{(Depth*2)+1}"
                CodeList=WriterPythonCode(Equation[1:LastIndex+1],CodeList,(Depth*2)+1)
            CodeList.append(f" Step{Depth} = math.cbrt({Term_1})")
            return CodeList
        case "$":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            if LastIndex==1:
                Term_1 = Equation[1].symbol
            else:
                Term_1 = f"Step{(Depth*2)+1}"
                CodeList=WriterPythonCode(Equation[1:LastIndex+1],CodeList,(Depth*2)+1)
            CodeList.append(f" try: Step{Depth} = math.sin({Term_1})")
            CodeList.append(f" except ValueError as err: Step{Depth} = 0")
            return CodeList
        case "&":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            if LastIndex==1:
                Term_1 = Equation[1].symbol
            else:
                Term_1 = f"Step{(Depth*2)+1}"
                CodeList=WriterPythonCode(Equation[1:LastIndex+1],CodeList,(Depth*2)+1)
            if Depth==0: CodeList.append(f' return Step_{Depth}')
            CodeList.append(f" try: Step{Depth} = math.cos({Term_1})")
            CodeList.append(f" except ValueError as err: Step{Depth} = 1")
            return CodeList
        case "@":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            if LastIndex==1:
                Term_1 = Equation[1].symbol
            else:
                Term_1 = f"Step{(Depth*2)+1}"
                CodeList=WriterPythonCode(Equation[1:LastIndex+1],CodeList,(Depth*2)+1)
            CodeList.append(f" try: Step{Depth} = math.tan({Term_1})")
            CodeList.append(f" except ValueError as err: Step{Depth} = 0")
            return CodeList
        case "E":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            if LastIndex==1:
                Term_1 = Equation[1].symbol
            else:
                Term_1 = f"Step{(Depth*2)+1}"
                CodeList=WriterPythonCode(Equation[1:LastIndex+1],CodeList,(Depth*2)+1)
            CodeList.append(f" try: Step{Depth} = math.exp({Term_1})")
            CodeList.append(f" except OverflowError as err: Step{Depth} = 1")
            return CodeList
        case "L":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            if LastIndex==1:
                Term_1 = Equation[1].symbol
            else:
                Term_1 = f"Step{(Depth*2)+1}"
                CodeList=WriterPythonCode(Equation[1:LastIndex+1],CodeList,(Depth*2)+1)
            CodeList.append(f" try: Step{Depth} = math.log({Term_1})")
            CodeList.append(f" except ValueError as err: Step{Depth} = 0")
            return CodeList
        case _:
            return [f" Step{Depth} = {Equation[0].symbol}"]

def WriterC_Code(Equation:list[Any],CodeList:list[str],Depth:int=1) -> list[str]:
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
                Term_1 = f"Step{(Depth*2)+1}"
                CodeList=WriterC_Code(Equation[1:LastIndex+1],CodeList,(Depth*2)+1)
            if LastIndex2==LastIndex+1:
                Term_2 = Equation[LastIndex+1].symbol
            else:
                Term_2 = f"Step{(Depth*2)+2}"
                CodeList=WriterC_Code(Equation[LastIndex+1:LastIndex2+1],CodeList,(Depth*2)+2)
            CodeList.append(f" double Step{Depth} = {Term_1} + {Term_2};")
            return CodeList
        case "-":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            LastIndex2:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=LastIndex+1)
            if LastIndex==1:
                Term_1 = Equation[1].symbol
            else:
                Term_1 = f"Step{(Depth*2)+1}"
                CodeList=WriterC_Code(Equation[1:LastIndex+1],CodeList,(Depth*2)+1)
            if LastIndex2==LastIndex+1:
                Term_2 = Equation[LastIndex+1].symbol
            else:
                Term_2 = f"Step{(Depth*2)+2}"
                CodeList=WriterC_Code(Equation[LastIndex+1:LastIndex2+1],CodeList,(Depth*2)+2)
            CodeList.append(f" double Step{Depth} = {Term_2} - {Term_1};")
            return CodeList
        case "*":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            LastIndex2:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=LastIndex+1)
            if LastIndex==1:
                Term_1 = Equation[1].symbol
            else:
                Term_1 = f"Step{(Depth*2)+1}"
                CodeList=WriterC_Code(Equation[1:LastIndex+1],CodeList,(Depth*2)+1)
            if LastIndex2==LastIndex+1:
                Term_2 = Equation[LastIndex+1].symbol
            else:
                Term_2 = f"Step{(Depth*2)+2}"
                CodeList=WriterC_Code(Equation[LastIndex+1:LastIndex2+1],CodeList,(Depth*2)+2)
            CodeList.append(f" double Step{Depth} = {Term_1} * {Term_2};")
            return CodeList
        case "^":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            LastIndex2:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=LastIndex+1)
            if LastIndex==1:
                Term_1 = Equation[1].symbol
            else:
                Term_1 = f"Step{(Depth*2)+1}"
                CodeList=WriterC_Code(Equation[1:LastIndex+1],CodeList,(Depth*2)+1)
            if LastIndex2==LastIndex+1:
                Term_2 = Equation[LastIndex+1].symbol
            else:
                Term_2 = f"Step{(Depth*2)+2}"
                CodeList=WriterC_Code(Equation[LastIndex+1:LastIndex2+1],CodeList,(Depth*2)+2)
            CodeList.append(f" double Step{Depth} = pow({Term_2}, {Term_1});")
            CodeList.append(f" if (isinf(Step{Depth}))  Step{Depth} = 10000000;")
            CodeList.append(f" if (isnan(Step{Depth})) Step{Depth} = 0;")
            return CodeList
        case "/":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            LastIndex2:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=LastIndex+1)
            if LastIndex==1:
                Term_1 = Equation[1].symbol
            else:
                Term_1 = f"Step{(Depth*2)+1}"
                CodeList=WriterC_Code(Equation[1:LastIndex+1],CodeList,(Depth*2)+1)
            if LastIndex2==LastIndex+1:
                Term_2 = Equation[LastIndex+1].symbol
            else:
                Term_2 = f"Step{(Depth*2)+2}"
                CodeList=WriterC_Code(Equation[LastIndex+1:LastIndex2+1],CodeList,(Depth*2)+2)
            CodeList.append(f" double Step{Depth};")
            CodeList.append(f" if ({Term_1}==0) Step{Depth} = 0;")
            CodeList.append(f" else Step{Depth} = (double) {Term_2} / {Term_1};")
            return CodeList
        case "S":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            if LastIndex==1:
                Term_1 = Equation[1].symbol
            else:
                Term_1 = f"Step{(Depth*2)+1}"
                CodeList=WriterC_Code(Equation[1:LastIndex+1],CodeList,(Depth*2)+1)
            CodeList.append(f" double Step{Depth} = {Term_1} * {Term_1};")
            CodeList.append(f" if (isinf(Step{Depth}))  Step{Depth} = 10000000;")
            return CodeList
        case "C":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            if LastIndex==1:
                Term_1 = Equation[1].symbol
            else:
                Term_1 = f"Step{(Depth*2)+1}"
                CodeList=WriterC_Code(Equation[1:LastIndex+1],CodeList,(Depth*2)+1)
            CodeList.append(f" double Step{Depth} = {Term_1} * {Term_1} * {Term_1};")
            CodeList.append(f" if (isinf(Step{Depth}))  Step{Depth} = 10000000;")
            return CodeList
        case "R":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            if LastIndex==1:
                Term_1 = Equation[1].symbol
            else:
                Term_1 = f"Step{(Depth*2)+1}"
                CodeList=WriterC_Code(Equation[1:LastIndex+1],CodeList,(Depth*2)+1)
            CodeList.append(f" double Step{Depth} = sqrt({Term_1});")
            CodeList.append(f" if (isnan(Step{Depth})) Step{Depth} = {Term_1};")
            return CodeList
        case "T":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            if LastIndex==1:
                Term_1 = Equation[1].symbol
            else:
                Term_1 = f"Step{(Depth*2)+1}"
                CodeList=WriterC_Code(Equation[1:LastIndex+1],CodeList,(Depth*2)+1)
            CodeList.append(f" double Step{Depth} = cbrt({Term_1});")
            return CodeList
        case "$":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            if LastIndex==1:
                Term_1 = Equation[1].symbol
            else:
                Term_1 = f"Step{(Depth*2)+1}"
                CodeList=WriterC_Code(Equation[1:LastIndex+1],CodeList,(Depth*2)+1)
            CodeList.append(f" double Step{Depth} = sin({Term_1});")
            CodeList.append(f" if (isnan(Step{Depth}))  Step{Depth} = 0;")
            return CodeList
        case "&":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            if LastIndex==1:
                Term_1 = Equation[1].symbol
            else:
                Term_1 = f"Step{(Depth*2)+1}"
                CodeList=WriterC_Code(Equation[1:LastIndex+1],CodeList,(Depth*2)+1)
            if Depth==0: CodeList.append(f' return Step_{Depth}')
            CodeList.append(f" double Step{Depth} = cos({Term_1});")
            CodeList.append(f" if (isnan(Step{Depth}))  Step{Depth} = 1;")
            return CodeList
        case "@":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            if LastIndex==1:
                Term_1 = Equation[1].symbol
            else:
                Term_1 = f"Step{(Depth*2)+1}"
                CodeList=WriterC_Code(Equation[1:LastIndex+1],CodeList,(Depth*2)+1)
            CodeList.append(f" double Step{Depth} = tan({Term_1});")
            CodeList.append(f" if (isnan(Step{Depth}))  Step{Depth} = 0;")
            return CodeList
        case "E":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            if LastIndex==1:
                Term_1 = Equation[1].symbol
            else:
                Term_1 = f"Step{(Depth*2)+1}"
                CodeList=WriterC_Code(Equation[1:LastIndex+1],CodeList,(Depth*2)+1)
            CodeList.append(f" double Step{Depth} = exp({Term_1});")
            CodeList.append(f" if (isinf(Step{Depth}))  Step{Depth} = 1;")
            return CodeList
        case "L":
            LastIndex:int = PickSubTree(Code=GP.Program(Code=Equation),FirstIndex=1)
            if LastIndex==1:
                Term_1 = Equation[1].symbol
            else:
                Term_1 = f"Step{(Depth*2)+1}"
                CodeList=WriterC_Code(Equation[1:LastIndex+1],CodeList,(Depth*2)+1)
            CodeList.append(f" double Step{Depth} = log({Term_1});")
            CodeList.append(f" if (isnan(Step{Depth}))  Step{Depth} = 0;")
            CodeList.append(f" if (isinf(Step{Depth}))  Step{Depth} = 0;")
            return CodeList
        case _:
            return [f" double Step{Depth} = {Equation[0].symbol}"]

def CreateErrorGraph(TotalError:list[float],MinError:list[float],ErrorList:list[int|float],EqLen:list[int],TargetFile:str) -> bool:
    """
    Creates and Saves a Graph of Error Statistics.
    """
    generation = [i for i in range(1,len(TotalError)+1)]
    plt.xlabel("Generation") # pyright: ignore[reportUnknownMemberType]
    plt.ylabel("Total Error") # pyright: ignore[reportUnknownMemberType]
    plt.plot(generation,TotalError,scalex=True) # pyright: ignore[reportUnknownMemberType]
    plt.savefig(f"{TargetFile}_TotalError.png",dpi=300) # pyright: ignore[reportUnknownMemberType]
    plt.close()
    
    plt.xlabel("Generation") # pyright: ignore[reportUnknownMemberType]
    plt.ylabel("Minimum Error") # pyright: ignore[reportUnknownMemberType]
    plt.plot(generation,MinError,c='r') # pyright: ignore[reportUnknownMemberType]
    plt.plot(generation,[0 for _ in range(len(TotalError))],c='y',ls=":") # pyright: ignore[reportUnknownMemberType]
    plt.savefig(f"{TargetFile}_MinError.png",dpi=300) # pyright: ignore[reportUnknownMemberType]
    plt.close()

    ErrorList_clean:list[int|float] = []
    for x in ErrorList:
        try:
            np.isfinite(x)
            if (x==math.inf): raise TypeError("Infinite error Encountered")
            ErrorList_clean.append(x)
        except TypeError as err:
            ErrorList.append(100000)
    plt.xlabel('Error Range')
    plt.ylabel('Number of Equations')
    plt.hist(ErrorList_clean,color="g")
    plt.savefig(f"{TargetFile}_hist_Err.png",dpi=300)
    plt.close()

    plt.xlabel('Equation Length(Complexity)')
    plt.ylabel('Number of Equations')
    plt.hist(EqLen,color='black')
    plt.savefig(f"{TargetFile}_hist_len.png",dpi=300)
    plt.close()

    Very_Accurate:int = len([i for i in ErrorList if i<1])
    Accurate:int = len([i for i in ErrorList if 1<i<5])
    Not_Accurate:int = len([i for i in ErrorList if i>5])
    plt.pie([Very_Accurate,Accurate,Not_Accurate],labels=['Very Accurate (<1)','Accurate (1-5)','Less Accurate (>5)'],colors=['g','y','r'],autopct='%.2f %%')
    plt.savefig(f"{TargetFile}_pie_Err.png",dpi=300)
    plt.close()

    Simple:int = len([i for i in EqLen if i<5])
    Sofic:int = len([i for i in EqLen if 5<i<10])
    Complex:int = len([i for i in EqLen if i>10])
    plt.pie([Simple,Sofic,Complex],labels=['Simple (<5)','Sofisticated (5-10)','Complex (>10)'],colors=['g','y','r'],autopct='%.2f %%')
    plt.savefig(f"{TargetFile}_pie_len.png",dpi=300)
    plt.close()
    return True

def CreatePredictionGraph(Input:list[list[int|float]],ReqOutput:list[int|float],PreOutput:list[int|float],Performer:int,TargetFile:str) -> bool:
    """
    Creates and Saves Graph of Given and Prediction Data
    with Respect to Each Input Variable.
    """
    for VarNum in range(len(Input[0])):
        CurrentInput = [Inputs[VarNum] for Inputs in Input]
        plt.xlabel(f"Input var{VarNum+1}") # pyright: ignore[reportUnknownMemberType]
        plt.ylabel("Output") # pyright: ignore[reportUnknownMemberType]
        plt.plot(CurrentInput,PreOutput,marker='o',label="Predicted") # pyright: ignore[reportUnknownMemberType]
        plt.plot(CurrentInput,ReqOutput,c='y',marker='o',ls=":",label="Given") # pyright: ignore[reportUnknownMemberType]
        plt.legend() # pyright: ignore[reportUnknownMemberType]
        plt.savefig(f"{TargetFile}_Prediction_{Performer}_{VarNum+1}.png",dpi=300) # pyright: ignore[reportUnknownMemberType]
        plt.close()
    return True

def DescribeEq(filename:str,TargetFile:TextIOWrapper,Equation: list[Any],InputData:list[list[int|float]],Req_Output:list[int|float],Pre_Output:list[int|float],Performer:int,ProgramError:int|float) -> None:
    """
    Writes Predicted Result Table and Equation to Tex File
    """
    
    TexEquation:str = WriteTexEquation(Equation=Equation)
    TargetFile.write(f'''\\section{{Result For Best Performance No. {Performer}}}''')
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
            \\label{{tab:data{Performer}}}       
        \\end{{longtable}}
        \\end{{center}}
''')               
#\\end{{table}}''')
    CreatePredictionGraph(Input=InputData,ReqOutput=Req_Output,PreOutput=Pre_Output,Performer=Performer,TargetFile=filename)
    TargetFile.write('''
\\subsection{Prediction Graph}''')
    for VarNum in range(len(InputData[0])):
        TargetFile.write(f'''
\\begin{{figure}}[H]
    \\centering
    \\includegraphics[height=200pt,width=300pt]{{{filename}_Prediction_{Performer}_{VarNum+1}.png}}
    \\caption{{ Prediction Graph with Respect to $X_{{{VarNum+1}}}$.}}
    \\label{{fig:Prediction_{Performer}_{VarNum+1}}}
\\end{{figure}}
''')
    TargetFile.write('''
\\subsection{Equation}
The Equation with minimum error was''')
    if len(Equation) >10 : TargetFile.write(f"\\begin{{equation}}\n\\resizebox{{0.95\\linewidth}}{{!}}{{$\nY={TexEquation}\n$}}\n\\end{{equation}}\n\nWith a Minimum Error of {ProgramError}\n")
    else: TargetFile.write(f"\\[\nY={TexEquation}\\]\n\nWith a Minimum Error of {ProgramError}\n")

def Create(filepath:str,equation: list[list[Any]],NumberOfCode:int,TotalError:list[float],ErrorList:list[int|float],MinError:list[float],Input:list[list[int|float]],Output:list[int|float],Predict:list[list[int|float]],HParams:dict[str,int|float|bool|str]) -> None:
    """
    Creates a Tex File for the execution of 
    Genetic Program and Compile into PDF File.
    """
    
    with open(f"{filepath}.tex","w") as TexFile:
        if not HParams["Anime"]: TexFile.write('''\\documentclass[a4paper]{article}
\\usepackage{amsmath}
\\usepackage{longtable}
\\usepackage{graphicx}
\\usepackage{minted}
\\usepackage{float}
\\usepackage{tikz}
\\usepackage{geometry}
\\geometry{margin=1in}

\\title{Report On Genetic Programs Execution}
\\author{Mustufa Ghadiyali}
\\date{\\today}
\\begin{document}
\\definecolor{cbg}{rgb}{0.1,0.1,0.3}
\\definecolor{pygb}{rgb}{0.02,0.02,0.05}
\\setminted[python3]{style=rrt,bgcolor=pygb}
\\setminted[c]{style=fruity,bgcolor=cbg}
\\begin{titlepage}
    \\centering
    \\vspace*{-2cm}
    \\begin{tikzpicture}[remember picture,overlay]
        \\node[anchor=north west, xshift=0.5cm, yshift=-0.5cm] at (current page.north west)
        {\\includegraphics[width=3cm]{Logo.png}}; % Optional anime-style logo
    \\end{tikzpicture}
    {\\Huge\\bfseries Report On Genetic Program's Execution \\par}
    \\vspace{1cm}
    {\\Large\\itshape Generated by Genetic Programming Engine \\par}
    \\vspace{2cm}
    {\\Large\\bfseries Mustufa Ghadiyali \\par}
    \\vspace{1cm}
    {\\large \\today \\par}
    \\vfill
    {\\small\\textcolor{gray}{An Auto Generated Report for the Execution and Operation of Genetic Program.} \\par}
\\end{titlepage}
\\tableofcontents
\\newpage''')
        else: TexFile.write('''\\documentclass[a4paper]{article}
\\usepackage{amsmath}
\\usepackage{longtable}
\\usepackage{graphicx}
\\usepackage{minted}
\\usepackage{float}
\\usepackage{tikz}
\\usepackage{geometry}
\\usepackage{xcolor}
\\usepackage{fontawesome}
\\usepackage{titlesec}
\\usepackage{geometry}
\\usepackage{fontspec}
\\geometry{margin=1in}

\\title{Report On Genetic Programs Execution}
\\author{Mustufa Ghadiyali}
\\date{\\today}
\\newcommand{\\animefont}{\\fontspec{Anime Ace}}
\\begin{document}
\\definecolor{cbg}{rgb}{0.1,0.1,0.3}
\\definecolor{pygb}{rgb}{0.02,0.02,0.05}
\\setminted[python3]{style=rrt,bgcolor=pygb}
\\setminted[c]{style=fruity,bgcolor=cbg}
\\begin{titlepage}
    \\centering
    % Decorative Header
    \\vspace*{-2cm}
    \\begin{tikzpicture}[remember picture,overlay]
        \\node[anchor=north west, xshift=0.5cm, yshift=-0.5cm] at (current page.north west)
        {\\includegraphics[width=3cm]{LogoSakura.png}}; % Optional anime-style logo
    \\end{tikzpicture}

    % Title
    {\\animefont\\Huge\\bfseries\\textcolor{pink} {Evolution Saga: Symbolic Regression} \\par}
    \\vspace{0.5cm}
    {\\Large\\itshape\\textcolor{gray}{Powered by Genetic Programming} \\par}
    \\vspace{1.5cm}

    % Author
    {\\Large\\textcolor{blue}{Mustufa Ghadiyali} \\par}
    {\\large Surat, India \\par}
    \\vspace{1cm}

    % Icons and Flair
    {\\Large\\textcolor{red}{\\faHeart} \\quad
     \\textcolor{orange}{\\faStar} \\quad
     \\textcolor{green}{\\faMagic} \\quad
     \\textcolor{cyan}{\\faRocket} \\par}
    \\vspace{1cm}

    % Date
    {\\large\\textcolor{gray}{\\today} \\par}

    % Footer
    \\vfill
    {\\small\\textcolor{gray}{This report was auto-generated using a custom symbolic regression engine.} \\par}
\\end{titlepage}
\\tableofcontents
\\newpage''')
        TexFile.write(f'''
\\section{{Values of Hyper Parameters}}
The Values of Hyper Parameters Were set as Follow for this run of\nGenetic Program.
\\begin{{itemize}}
    \\item Maximum Depth of Equation Tree = {HParams["MAXDEPTH"]}
    \\item Maximum Size of Generation = {HParams["GENSIZE"]}
    \\item Maximum Number of Generation = {HParams["MAXGEN"]}
    \\item Total Generation Evolved = {len(TotalError)}
    \\item Crossover Probability = {HParams["XOP"]}
    \\item Maximum Crossover per Generation = {HParams["MAXXO"]}
    \\item Mutation Probability = {HParams["MUTP"]}    
    \\item Maximum Mutation per Generation = {HParams["MAXMUT"]}
    \\item New Introduction Probability = {HParams["NEWP"]}
    \\item Maximum New Introduction Per Generation = {HParams["MAXNEW"]}
    \\item Verbose Output = {HParams["VERBOSE"]}
    \\item Function Set = {HParams["FSET"]} 
\\end{{itemize}}
''')
        

        for i in range(5): 
            DescribeEq(filename=filepath,TargetFile=TexFile,Equation=equation[i],Performer=(i+1),InputData=Input,Req_Output=Output,Pre_Output=Predict[i],ProgramError=ErrorList[i])
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


        CreateErrorGraph(TotalError,MinError,ErrorList,[len(i) for i in equation],filepath)
        TexFile.write(f'''\\section{{Performance Statistics}}
\\subsection{{Performance Graph}}
\\begin{{figure}}[H]
    \\centering
    \\includegraphics[height=200pt,width=300pt]{{{f"{filepath}_TotalError.png"}}}
    \\caption{{Graph of Total Error in Each Generation.}}
    \\label{{fig:TotalError}}
\\end{{figure}}
                      
\\begin{{figure}}[H]
    \\centering
    \\includegraphics[height=200pt,width=300pt]{{{f"{filepath}_MinError.png"}}}
    \\caption{{Graph of Minimum Error in Each Generation.}}
    \\label{{fig:MinError}}
\\end{{figure}}
                      
\\begin{{figure}}[H]
    \\centering
    \\includegraphics[height=200pt,width=300pt]{{{f"{filepath}_hist_Err.png"}}}
    \\caption{{Histogram of Equations By Errors.}}
    \\label{{fig:Hist_Err}}
\\end{{figure}}                      
                      
\\begin{{figure}}[H]
    \\centering
    \\includegraphics[height=200pt,width=300pt]{{{f"{filepath}_hist_len.png"}}}
    \\caption{{Histogram of Equations By Lenght.}}
    \\label{{fig:Hist_len}}
\\end{{figure}} 
                      
\\begin{{figure}}[H]
    \\centering
    \\includegraphics[height=200pt,width=300pt]{{{f"{filepath}_pie_Err.png"}}}
    \\caption{{Pie Chart of Equations By Errors.}}
    \\label{{fig:Pie_Err}}
\\end{{figure}}                      
                      
\\begin{{figure}}[H]
    \\centering
    \\includegraphics[height=200pt,width=300pt]{{{f"{filepath}_pie_len.png"}}}
    \\caption{{Pie Chart of Equations By Lenght.}}
    \\label{{fig:Pie_len}}
\\end{{figure}}                      
                      ''')
        TexFile.write('''\\subsection{Error Table}
    \\centering
    \\begin{longtable}{|c|c|c|c|}
        \\hline
        Gen No. & Total Error & Average Error & Min Error  \\\\
        \\hline\n''')
        for i,Value in enumerate(start=1,iterable=TotalError):
            TexFile.write(f"Gen {i} & {Value} & {(Value/NumberOfCode)} & {MinError[i-1]} \\\\\n\\hline\n")
        TexFile.write(
    '''
\\caption{Generation wise Total,Average and Minimum Error.}
\\label{tab:errors}
\\end{longtable}\n''')
        TexFile.write("\\end{document}")
    if HParams["Anime"]: os.system(f"lualatex {filepath}.tex")
    else: os.system(f"pdflatex {filepath}.tex")    
    if HParams["Anime"]: os.system(f"lualatex {filepath}.tex")
    else: os.system(f"pdflatex {filepath}.tex")
    os.remove(f"{filepath}_TotalError.png")
    os.remove(f"{filepath}_MinError.png")
    os.remove(f"{filepath}_hist_Err.png")
    os.remove(f"{filepath}_hist_len.png")
    os.remove(f"{filepath}_pie_Err.png")
    os.remove(f"{filepath}_pie_len.png")
    os.remove(f"{filepath}.aux")
    os.remove(f"{filepath}.log")
    os.remove(f"{filepath}.toc")
    #os.remove(f"{filepath}.tex")
    for i in range(5):
        for t in range(len(Input[0])):
            os.remove(f"{filepath}_Prediction_{i+1}_{t+1}.png")


if __name__ == "__main__":
    '''
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
    GP.Union_List= Function_Set + GP.Terminal_Set
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