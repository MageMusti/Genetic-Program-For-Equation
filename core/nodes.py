from core.Integer_Helper import CheckWhetherStringIsIntegerOrFloat as CIF

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
Exp:Node = Node("E",1)
Log:Node = Node("L",1)
