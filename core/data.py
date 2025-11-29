import csv
from core.Integer_Helper import CheckWhetherStringIsIntegerOrFloat as CIF


def FormatCsv(filepath:str) -> tuple[list[dict[str,int|float]],list[int|float]]:

    """
    This Function takes a Path to a csv file and returns
    a list of list of Integers and floats as Input for all elements except
    the last in each and the Output as list of all last elements of each row.
    """
    
    with open(file=filepath,mode="r") as csv_file:
        csv_reader = csv.reader(csv_file)
        Output:list[int|float] = []
        Input:list[dict[str,int|float]] = []
        for row in csv_reader:
            list_row: list[str] = row.copy()
            OutputNum:str = list_row.pop()
            if (x:=CIF(OutputNum))=="Null":
                raise TypeError(f"Last Element in row {row} is not a Number")    
            Output.append(x)
            Input.append({f"var{i}":CIF(Num) for i,Num in enumerate(start=1,iterable=list_row) if CIF(Num)!="Null"}) # type: ignore

    return (Input,Output)