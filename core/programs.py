from core.nodes import *
import math
import random
from core.Integer_Helper import CheckWhetherStringIsIntegerOrFloat as CIF
import core.PostEva as PostEva

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
    def RandomCode(S:Node,Depth:int,MAX_DEPTH:int,Terminal_Set:list[Node],Union_List:list[Node]) -> list[Node]:
        """
        Generate Random Code.
        """
        
        Random:list[Node] = [S]
        if not Random[-1].Terminal:
            return Random
        if Depth>=MAX_DEPTH:
            for _ in range(0,Random[-1].Terminal):
                NewNode:Node = random.choice(Terminal_Set)
                Random.extend(Program.RandomCode(NewNode,Depth+1,MAX_DEPTH,Terminal_Set,Union_List))
            return Random
        
        for _ in range(0,Random[-1].Terminal):
            NewNode:Node = random.choice(Union_List)
            Random.extend(Program.RandomCode(NewNode,Depth+1,MAX_DEPTH,Terminal_Set,Union_List))
        return Random

            
    
    @staticmethod
    def CreateRandom(MAX_DEPTH:int,Terminal_Set:list[Node],Union_List:list[Node],SomeList:list[Node]|None = None) -> 'Program':
        """
        Return A Random Program
        """
        
        CodeList:list[Node] = []
        if not SomeList: Random_Node:Node = random.choice(Union_List)
        else: Random_Node:Node = random.choice(SomeList)
        CodeList.extend(Program.RandomCode(Random_Node,1,MAX_DEPTH,Terminal_Set,Union_List))
        return Program(Code=CodeList)
    
    @staticmethod
    def ParseCode(Terminal_Set:list[Node],Generation:list[str]) -> list['Program']:
        Current_Gen:list['Program'] = []
        for Code in Generation:
            separableCode = Code[1:-1]
            CodeList:list[Node] = []
            for Index,SomeNode in enumerate(separableCode.split(",")):
                if Index: SomeNode = SomeNode[1:]
                match SomeNode:
                    case '^':
                        CodeList.append(Power)
                    case '*':
                        CodeList.append(Mul)
                    case '/':
                        CodeList.append(Divide)
                    case '+':
                        CodeList.append(Plus)
                    case '-':
                        CodeList.append(Minus)
                    case "R":
                        CodeList.append(Square_Root)
                    case "C":
                        CodeList.append(Cube)
                    case "S":
                        CodeList.append(Square)
                    case "T":
                        CodeList.append(Cube_Root)
                    case "$":
                        CodeList.append(Sin)
                    case "&":
                        CodeList.append(Cos)
                    case "@":
                        CodeList.append(Tan)
                    case "E":
                        CodeList.append(Exp)
                    case "L":
                        CodeList.append(Log)
                    case _:
                        if SomeNode.startswith("var"): CodeList.append(Terminal_Set[int(SomeNode[3:])])
                        elif CIF(SomeNode)!="Null": CodeList.append(Node(SomeNode))
                        else: raise ValueError(f"Unknown Operator '{SomeNode}' Detected.")
            Current_Gen.append(Program(CodeList))
        
        return Current_Gen
