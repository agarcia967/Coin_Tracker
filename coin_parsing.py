# coin_parsing.py
__author__ = "Anthony R. Garcia <agarcia967@hotmail.com>"
__date__ = "10/30/2014"
__version__ = "3.6"
__credits__ = None

def _beginsWithNumber(str):
    """
    This function returns the index of a string up
    to the point where there are no more digits.

    String may then be called with string[:r],
    or it may be called with string[r:].
    """
    digits=["0","1","2","3","4","5","6","7","8","9"]
    r=0
    for i in range(len(str)):
        if str[i] in digits:
            r+=1#increments if there is a digit
        else:
            return r
    return r

def parseBillsLine():
    error = ["Item not in valid format!",
             "Integers only!",
             "Invalid bill type!"]
    acceptedBills = ["H","I","T","E","F","W","O"]
    abText = ["Hundreds",
              "Fifties",
              "Twenties",
              "Tens",
              "Fives",
              "Twos",
              "Ones"]
    returnable = [0 for i in acceptedBills]
    done = False
    while(not(done)):
        z = 0
        while z<len(acceptedBills):
            print(acceptedBills[z],"-",abText[z])
            z+=1
        print("Enter all bills on one line in format:\n6%s 3%s 1%s" %(acceptedBills[6],acceptedBills[4],acceptedBills[2]))
        line = input("Enter bills: ")
        if(line=="" or line==None):
            print("Please enter bills. Enter 'c' to cancel or 'h' for help")
            done = False
        elif(line.lower()=="cancel" or line[0].lower()=="c"):
            return None
        elif(line.lower()=="help" or line[0].lower()=="h"):
            z = 0
            while z<len(acceptedBills):
                print(acceptedBills[z],"-",abText[z])
                z+=1
            print("Enter all bills on one line in format:\n6%s 3%s 1%s" %(acceptedBills[6],acceptedBills[4],acceptedBills[2]))
            done = False
        else:
            done = True
    list = line.split()
    for i in list:
        a = 0
        n = ""
        index = _beginsWithNumber(i)
        if(index>0):
            a = int(i[:index])
        else:
            print(i,"does not begin with a number greater than 0!")
        try:
            rest = i[index:].upper()
            if(rest in acceptedBills):
                n = rest
                if(__name__=='__main__'):
                    print("Increment %s by %d\n" %(abText[acceptedBills.index(n)],a))
                returnable[acceptedBills.index(n)]+=a
            else:
                print(error[2],"'%s'" %rest)
                print("Item was not added.\n")
        except IndexError:
            print(error[0],"'%s'"%i)
            print("Item was not added.\n")
    return returnable

def parseCoinsLine():
    error = ["Item not in valid format!",
             "Integers only!",
             "Invalid coin type!"]
    acceptedCoins = ["W","H","Q","D","N","P"]
    acText = ["Whole Dollar Coins",
              "Half Dollar Coins",
              "Quarters",
              "Dimes",
              "Nickels",
              "Pennies"]
    returnable = [0 for i in acceptedCoins]
    done = False
    while(not(done)):
        z = 0
        while z<len(acceptedCoins):
            print(acceptedCoins[z],"-",acText[z])
            z+=1
        print("Enter all coins on one line in format:\n4%s 3%s 1%s" %(acceptedCoins[5],acceptedCoins[3],acceptedCoins[2]))
        line = input("Enter coins: ")
        if(line=="" or line==None):
            print("Please enter coins. Enter 'c' to cancel or 'h' for help")
            done = False
        elif(line.lower()=="cancel" or line[0].lower()=="c"):
            return None
        elif(line.lower()=="help" or line[0].lower()=="h"):
            z = 0
            while z<len(acceptedCoins):
                print(acceptedCoins[z],"-",acText[z])
                z+=1
            print("Enter all coins on one line in format:\n4%s 3%s 1%s" %(acceptedCoins[5],acceptedCoins[3],acceptedCoins[2]))
            done = False
        else:
            done = True
    list = line.split()
    for i in list:
        a = 0
        n = ""
        index = _beginsWithNumber(i)
        if(index>0):
            a = int(i[:index])
        else:
            print("'%s' does not begin with a number greater than 0!" %i)
            print("Item was not added.\n")
        try:
            rest = i[index:].upper()
            if(rest in acceptedCoins):
                n = rest
                if(__name__=='__main__'):
                    print("Increment %s by %d" %(acText[acceptedCoins.index(n)],a))
                returnable[acceptedCoins.index(n)]+=a
            else:
                print(error[2],"'%s'" %rest)
                print("Item was not added.\n")
        except IndexError:
            print(error[0],"'%s'"%i)
            print("Item was not added.\n")
    return returnable

if(__name__=='__main__'):
    billsList = parseBillsLine()
    coinsList = parseCoinsLine()
    print(billsList)
    print(coinsList)
