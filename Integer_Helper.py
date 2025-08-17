"""A Module To Assist with Numbers"""

def CheckWhetherStringIsIntegerOrFloat(Target_String):
    """
    Converts a Given Target_String To Integer Otherwise Float. If neither is Possible a String "Null" will be Returned
    """
    try: Target_String=str(Target_String)
    except ValueError as err:
        print("Probably Too Large Number\n",err )
        return 100000000
    try:
        x=float(Target_String)
    except:
        return "Null"
    if x%1==0:
        X=int(x)
        return X
    else:
        return x
    """
    try:
        x=int(Target_String)
        return x
    except:
        try:
            x=float(Target_String)
            return x
        except:
            return "Null"
        """
def sqrt(Target_Number):
    d=CheckWhetherStringIsIntegerOrFloat(Target_Number)
    if d=="Null":
        return "Null"
    else:
        c=d**(1/2)
        c=CheckWhetherStringIsIntegerOrFloat(c)
        return c
def cbrt(Target_Number):
    d=CheckWhetherStringIsIntegerOrFloat(Target_Number)
    if d=="Null":
        return "Null"
    else:
        c=d**(1/3)
        c=CheckWhetherStringIsIntegerOrFloat(c)
        return c