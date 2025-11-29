'''A program to Convert Infix Equation to Postfix Equations'''

def Oper_Pre(Char: str) -> int:
    """
    Returns Precedence of Operator
    Operators With Higher Precedence are given a Lower Value
    """
    match Char:
        case '(':
            return 1
        case ')':
            return 1
        case '^':
            return 2
        case '*':
            return 3
        case '/':
            return 3
        case '%':
            return 3
        case '+':
            return 4
        case '-':
            return 4
        case "R"|"C"|"S"|"T"|"$"|"&"|"@"|"E"|"L":     #Unary Operation R = Square Root, C = Cube, S = Square , T = Cube Root, $ = Sin , & = Cos , @ = tan 
            return 0
        case _:
            return -1

def AddVar(NewVar: list[str],Operands: set[str],PostEqList: list[str]) -> None:
    """
    Add New Variable For the Equation
    """
    if NewVar:  # type: ignore
        VarName = ''.join(NewVar) # type: ignore
        Operands.add(VarName)
        PostEqList.append(VarName)
        PostEqList.append(" ")
        NewVar.clear()

def HandleClosing(OperatorStack: list[str],PostEqList: list[str]) -> str:
    """
    Handles the Closing of Parenthesis in Equation 
    """
    try:
        lastchar: str = OperatorStack.pop()
        while (lastchar !="("):
            PostEqList.append(lastchar)
            lastchar = OperatorStack.pop()
    except IndexError as e:
        print(f"No Opening Bracket Found, The Following Error was Encountered\n{e}")
        return '-1'
    else:
        return "0"


def intopost(InEq: str) -> tuple[str,set[str]]:
    """
    Converts a Given Infix Equation as String to Postfix Equation.
    Returns Postfix Equation and Set of Variables or Constants Found in Equation
    """
    PostEq: str = ''
    PostEqList: list[str] = []
    Operands: set[str] = set()
    ReadingVar: bool = False
    OperatorStack: list[str] = []
    NewVar: list[str] = []
    for char in InEq:
        if char==' ':
            continue
        elif Oper_Pre(Char=char)!=-1:
            ReadingVar=False
            AddVar(NewVar,Operands,PostEqList)
            if char==')':
                if HandleClosing(OperatorStack,PostEqList)=='-1':
                    return ('-1',{'-1'})
                

            elif (not OperatorStack) or (Oper_Pre(Char=char) < Oper_Pre(Char=OperatorStack[-1])) or OperatorStack[-1]=='(' or char==OperatorStack[-1]=='^':
                OperatorStack.append(char)
            else:
                while(OperatorStack and Oper_Pre(Char=char)>=Oper_Pre(Char=OperatorStack[-1])):
                    PostEqList.append(OperatorStack.pop())
                OperatorStack.append(char)
        elif ReadingVar==False:
            NewVar: list[str] = [char]
            ReadingVar = True
        else:
            NewVar.append(char) # type: ignore
    if NewVar: AddVar(NewVar=NewVar,Operands=Operands,PostEqList=PostEqList)

    while len(OperatorStack)>0:
        Oper: str = OperatorStack.pop()
        if Oper=='(':
            continue
        PostEqList.append(Oper)
    #print(Operands)
    return (PostEq.join(PostEqList),Operands)


if __name__ == "__main__":
    Eq:str=input("Enter the Equation: ")
    print(f"the Postfix Equation is\n{intopost(Eq)[0]}")