def diningDollarBudget(dollarsLeft, week):
    return dollarsLeft/(11-week)

def laundryLeft (schillersLeft):
    return int(schillersLeft/2.25)
    
def LDCSwipes(lst):
    LDCCount=0
    for i in lst:
        if (i=="CC LDC Aero 1") or (i=="CC LDC Aero 2"):
            LDCCount=LDCCount+1
    return LDCCount

def burtonSwipes(lst):
    BurtonCount=0
    for i in lst:
        if (i=="CC Burton/Davis Aero 1") or (i=="CC Burton/Sevy Aero 2"):
            BurtonCount=BurtonCount+1
    return BurtonCount

