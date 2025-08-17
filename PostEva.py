"""Compute the Value of Postfix Equation."""

import intopost
import Integer_Helper
from collections.abc import Generator
import math

def GetValue(Operands: set[str]) -> dict[str,int|float]:
    """
    Get Value of Unknown Variables form CLI as input
    """
    Results: dict[str,int|float] = {}
    for Operand in Operands:
        Value: int|float|str = Integer_Helper.CheckWhetherStringIsIntegerOrFloat(Operand)
        if Value != 'Null':
            Results[Operand] = Value
            continue
        Value: int|float|str = Integer_Helper.CheckWhetherStringIsIntegerOrFloat(input(f"Enter the Value of {Operand}: "))
        if Value == 'Null':
            print("Invalid, Input is Not a Number,Taking Value as 0")
            Value =0
        Results[Operand] = Value
    return Results

def EquationReader(Equation:str) -> Generator[tuple[int,str],None,str]:
    """
    An Generator for Reading the Equation.
    """
    for i,char in enumerate(Equation):
        yield (i,char)
    while True:
        yield (len(Equation),"Null")
    return "Null"

def Calculator(FirstOperand: int| float,SecondOperand: int| float, Operator:str) -> int|float:
    """
    Does Binary Calculation of Given Operator on The 
    Two Given Operands.
    Returns the Result
    """
    Result: int| float | str 
    match Operator:
        case "+":
            Result = Integer_Helper.CheckWhetherStringIsIntegerOrFloat(FirstOperand+SecondOperand)
        case "-":
            Result = Integer_Helper.CheckWhetherStringIsIntegerOrFloat(FirstOperand-SecondOperand)
        case "*":
            Result = Integer_Helper.CheckWhetherStringIsIntegerOrFloat(FirstOperand*SecondOperand)
        case "/":
            try:
                Result = Integer_Helper.CheckWhetherStringIsIntegerOrFloat(FirstOperand/SecondOperand)
            except ZeroDivisionError as err:
                #print("Division By Zero Encountered, Returning Zero",err)
                return 0
        case "^":
            try:
               if FirstOperand >= 1000 or SecondOperand >= 50: raise OverflowError
               Result = Integer_Helper.CheckWhetherStringIsIntegerOrFloat(FirstOperand**SecondOperand)
            except OverflowError as err:
               #print("Too Large Number, returning 10000000")
               return 10000000
            except ZeroDivisionError as err:
                #print("Division By Zero Encountered, Returning Zero",err)
                return 0
        case _:
            print("Invalid Operator, Returning Zero")
            Result=0
    if Result == "Null":
        Final_Result: int|float = 0
    else: Final_Result = Result
    return Final_Result

def Unary_Calculator(FirstOperand: int| float, Operator:str) -> int|float:
    """
    Does Unary Calculation of Given Operator on The 
    Given Operand.
    Returns the Result
    """
    Result: int| float | str 
    match Operator:
        case "R":
            try:
                Result = Integer_Helper.CheckWhetherStringIsIntegerOrFloat(math.sqrt(FirstOperand))
            except ValueError as err:
                return FirstOperand
        case "C":
            Result = Integer_Helper.CheckWhetherStringIsIntegerOrFloat(FirstOperand**3)
        case "S":
            Result = Integer_Helper.CheckWhetherStringIsIntegerOrFloat(FirstOperand**2)
        case "T":
            Result = Integer_Helper.CheckWhetherStringIsIntegerOrFloat(math.cbrt(FirstOperand))
        case "$":
            Result = Integer_Helper.CheckWhetherStringIsIntegerOrFloat(math.sin(FirstOperand))
        case "&":
            Result = Integer_Helper.CheckWhetherStringIsIntegerOrFloat(math.cos(FirstOperand))
        case "@":
            Result = Integer_Helper.CheckWhetherStringIsIntegerOrFloat(math.tan(FirstOperand))
        case _:
            print("Invalid Operator, Returning Zero")
            Result=0
    if Result == "Null":
        Final_Result: int|float = 0
    else: Final_Result = Result
    return Final_Result

def ComputeEq(PostEq: str,Values: dict[str,int|float]) -> float | int:
    """
    Calculate The Values of Postfix Equation PostEq for Values of Variables in Values
    Returns the Result.
    """
    Result: float = 0.0
    NumStack : list[int|float] = []
    ReadVar: list[str] = []
    PostEqReader: Generator[tuple[int,str],None,str] = EquationReader(Equation=PostEq)
    char:str
    Index,char = next(PostEqReader)
    while char!="Null":
        Precedence: int =intopost.Oper_Pre(Char=char)
        try:
            while char!=" " and (Precedence==-1 or (char=="-" and PostEq[Index+1]!=" ")) and char!="Null":
                ReadVar.append(char)
                Index,char=next(PostEqReader)
                Precedence = intopost.Oper_Pre(Char=char)
        except IndexError as err:
            ...
        if (char==" " or char=="Null"):
            if not ReadVar: Index,char=next(PostEqReader);continue
            NewVar: str = ''.join(ReadVar)
            try:
                NumStack.append(Values[NewVar])
            except KeyError as err:
                print("Value of Variable Not Found")
            NewVar:str = ''
            ReadVar.clear() 
            Index,char=next(PostEqReader)
        elif Precedence==0:
            try:
                Operand:int |float = NumStack.pop()
                NumStack.append(Unary_Calculator(FirstOperand=Operand,Operator=char))
            except IndexError as err:
                print("Not Enough Numbers to continue",err)
            finally:
                Index,char = next(PostEqReader)
        else:
            try:
                Operand_2: int | float = NumStack.pop()
                Operand_1: int | float = NumStack.pop()
                NumStack.append(Calculator(FirstOperand=Operand_1,SecondOperand=Operand_2,Operator=char))
            except IndexError as err:
                if char=="-":
                    '''ReadVar.append(char)
                    Index,char = next(PostEqReader)'''
                    continue
                print("Not Enough Numbers to continue",err)
            finally:
                Index,char = next(PostEqReader)
    try: Result = NumStack[0]
    except IndexError as err:
        print("No Elements to Assign the following error has occurred",err)
        Result = 0
    return Result


if __name__ == "__main__":
    InfixEquation: str = input("Enter the Infix Equation: ")
    PostfixEquation , Operands = intopost.intopost(InfixEquation)

    Values: dict[str,int|float] = GetValue(Operands=Operands)
#    InfixEquation:str ="-67"
#    PostfixEquation:str = "-67"
#   Values:dict[str,int|float] = {'-67':-67}
    Answer: int | float = ComputeEq(PostEq=PostfixEquation,Values=Values)
    print(f"The Value of {InfixEquation} is {Answer}\nFor Values: ",end="")
    for Name,Value in Values.items():
        print(f"{Name} = {Value}",end=" ")