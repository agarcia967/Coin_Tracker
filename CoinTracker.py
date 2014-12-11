# Coin Tracker.py
__author__ = "Anthony R. Garcia <agarcia967@hotmail.com>"
__date__ = "11/07/2014"
__version__ = "3.0" #now with dictionaries and tuples!
__credits__ = None

import os

FILENAME = "cointracker.ini"
CENT_SYMBOL = u"\u00A2"
SECTIONS = ("bills","coins")
BILLS = ("hundred","fifty","twenty","ten","five","two","one")
COINS = ("dollar","halfdollar","quarter","dime","nickel","penny")
billsCoins= {"hundred":0,"fifty":0,"twenty":0,"ten":0,"five":0,"two":0,"one":0,
             "dollar":0,"halfdollar":0,"quarter":0,"dime":0,"nickel":0,"penny":0}
changesMade = False

def saveFile():
    global changesMade
    print("Writing file '%s'. Please wait... " %FILENAME, end='')
    outFile = open(FILENAME,'w')
    outFile.write("#DO NOT move this file!\n")
    sectionCounter = 0
    for section in SECTIONS:
        outFile.write("[%s]\n" %section.upper())
        for key in billsCoins:
            if(key in COINS and section=="coins"):
                outFile.write("%s=%s\n" %(key,str(billsCoins[key])))
            elif(key in BILLS and section=="bills"):
                outFile.write("%s=%s\n" %(key,str(billsCoins[key])))
        sectionCounter+=1
    outFile.close()
    print("Done.")
    changesMade = False

def readINIFile(FILENAME="cointracker.ini"):
    print("Reading file '%s'. Please wait... " %FILENAME, end='')
    if(not(os.path.exists(FILENAME))):
        print("File does not exist.")
        saveFile()
        return
    inFile = open(FILENAME, "r")
    counter = 0
    currentSection = 0
    for line in inFile:
        line = line.strip()
        counter+=1
        ll = []
        section = ""
        if(line=="" or line[0]=="#"):
            ""
        elif(line[0]=="["):
            section = line.replace("[","")
            section = section.replace("]","")
            if(section.lower() in SECTIONS):
                currentSection = (SECTIONS.index(section.lower()))
            else:
                print("FILE READ ERROR\n::Invalid Section name:",section)
                return
        elif(line):
            ll = line.split("=")
            for item in ll:
                ll[ll.index(item)] = item.strip()
            key = ll[0]
            value = int(ll[1])
            if(key in billsCoins):
                billsCoins[key] = value
            else:
                print("FILE READ ERROR\n::Invalid Key in Section %s: %s" %(SECTIONS[currentSection],key))
                return
        else:
            print("FILE READ ERROR\n::Unknown Error")
            return
    inFile.close()
    print("Done.")

def printValues():
    print("\n  BILLS")
    print(" $100.00 - %d" %billsCoins['hundred'])
    print(" $ 50.00 - %d" %billsCoins['fifty'])
    print(" $ 20.00 - %d" %billsCoins['twenty'])
    print(" $ 10.00 - %d" %billsCoins['ten'])
    print(" $  5.00 - %d" %billsCoins['five'])
    print(" $  2.00 - %d" %billsCoins['two'])
    print(" $  1.00 - %d" %billsCoins['one'])
    billsTotal = sum([billsCoins['hundred']*100,
                      billsCoins['twenty']*50,
                      billsCoins['one']*20,
                      billsCoins['ten']*10,
                      billsCoins['five']*5,
                      billsCoins['two']*2,
                      billsCoins['one']*1])
    print("Bills Total: $%0.2f" %billsTotal)
    print("\n  COINS")
    print(" $1.00 - %3.0d" %billsCoins['dollar'])
    print("   50%s - %3.0d" %(CENT_SYMBOL,billsCoins['halfdollar']))
    q = billsCoins['quarter']
    d = billsCoins['dime']
    n = billsCoins['nickel']
    p = billsCoins['penny']
    qR, dR, nR, pR = q//40, d//50, n//40, p//50
    e=""
    if(qR):
        e="(%s)" %qR
    print("   25%s - %3.0d %s" %(CENT_SYMBOL,q,e))
    
    e=""
    if(dR):
        e="(%s)" %dR
    print("   10%s - %3.0d %s" %(CENT_SYMBOL,d,e))
    e=""
    if(nR):
        e="(%s)" %nR
    print("    5%s - %3.0d %s" %(CENT_SYMBOL,n,e))
    e=""
    if(pR):
        e="(%s)" %pR
    print("    1%s - %3.0d %s" %(CENT_SYMBOL,p,e))
    coinsTotal = sum([billsCoins['dollar']*1,
                      billsCoins['halfdollar']*.5,
                      q*.25, d*.10, n*.05, p*.01,])
    print("Coins Total: $%0.2f\n" %coinsTotal)

def calcDeposit():
    print("\nCalculating...")
    depositAll = False
    depositValue = 0
    depositValue+=billsCoins['hundred']*100
    depositValue+=billsCoins['fifty'] *50
    depositValue+=billsCoins['twenty'] *20
    depositValue+=billsCoins['ten'] *10
    depositValue+=billsCoins['five'] * 5
    if(depositAll):
        depositValue+=billsCoins['two'] * 2
    else:
        print("[$2 bills omitted]")
    depositValue+=billsCoins['one'] * 1
    billsOnly = depositValue

    if(depositAll):
        depositValue+=billsCoins['dollar'] *1.00
    else:
        print("[$1 coins omitted]")
    if(depositAll):
        depositValue+=billsCoins['halfdollar'] * .50
    else:
        print("[50%s coins omitted]" %CENT_SYMBOL)
    depositValue+=((billsCoins['quarter']//40)*10)
    depositValue+=((billsCoins['dime']//50)*5)
    depositValue+=((billsCoins['nickel']//40)*2)
    depositValue+=((billsCoins['penny']//50)*.5)
    print("Done.")
    print("\nBills Only: $%0.2f" %billsOnly)
    print("Deposit value: $%0.2f\n" %depositValue)
    return depositValue

def makeDeposit():
    global changesMade
    calcDeposit()
    resp=input("Are you sure you have or want to deposit\nthis amount to the bank? (y/n) ")
    if(not(resp[0].lower()=="y")):
        return
    depositAll = 0
    billsCoins['hundred'] = 0 #hundreds
    billsCoins['fifty'] = 0 #fifties
    billsCoins['twenty'] = 0 #twenties
    billsCoins['ten'] = 0 #tens
    billsCoins['five'] = 0 #fives
    if(depositAll):
        billsCoins['two'] = 0 #twos
    else:
        print("[$2 bills omitted]")
    billsCoins['one'] = 0 #ones

    if(depositAll):
        billsCoins['dollar'] = 0 #dollar coins
    else:
        print("[$1 coins omitted]")
    if(depositAll):
        billsCoins['halfdollar'] = 0 #fifty cent coins
    else:
        print("[50%s coins omitted]" %CENT_SYMBOL)
    billsCoins['quarter'] = billsCoins['quarter'] % 40 #quarters
    billsCoins['dime'] = billsCoins['dime'] % 50 #dimes
    billsCoins['nickel'] = billsCoins['nickel'] % 40 #nickels
    billsCoins['penny'] = billsCoins['penny'] % 50 #pennies
    print("Deposited amounts removed from current values.")
    changesMade = True

def currentValue():
    totalValue = 0
    totalValue+=billsCoins['hundred']*100
    totalValue+=billsCoins['fifty'] *50
    totalValue+=billsCoins['twenty'] *20
    totalValue+=billsCoins['ten'] *10
    totalValue+=billsCoins['five'] * 5
    totalValue+=billsCoins['two'] * 2
    totalValue+=billsCoins['one'] * 1

    totalValue+=billsCoins['dollar'] *1.00
    totalValue+=billsCoins['halfdollar'] * .50
    totalValue+=billsCoins['quarter'] * .25
    totalValue+=billsCoins['dime'] * .10
    totalValue+=billsCoins['nickel'] * .05
    totalValue+=billsCoins['penny'] * .01
    return totalValue

def coinRollers(isPrinter):
    qRolls = billsCoins['quarter']//40
    dRolls = billsCoins['dime']//50
    nRolls = billsCoins['nickel']//40
    pRolls = billsCoins['penny']//50
    if(isPrinter):
        if(sum([qRolls,dRolls,nRolls,pRolls])<1):
            print("No coin rollers.")
            return 0
        if(qRolls>=1):
            print("%s Quarter Roller" %int(qRolls), end='')
            if(qRolls==1):
                print("")
            else:
                print("s")
        if(dRolls>=1):
            print("%s Dime Roller" %int(dRolls), end='')
            if(dRolls==1):
                print("")
            else:
                print("s")
        if(nRolls>=1):
            print("%s Nickel Roller" %int(nRolls), end='')
            if(nRolls==1):
                print("")
            else:
                print("s")
        if(pRolls>=1):
            print("%s Penny Roller" %int(pRolls), end='')
            if(pRolls==1):
                print("")
            else:
                print("s")
        print()
    else:
        return sum([qRolls,dRolls,nRolls,pRolls])

def addMoney():
    global changesMade
    print("\nAdd Bills & Coins\n-----------------\nType 'c' to cancel")
    counter = 0
    print("\nBILLS")
    for item in KEYS[0]:
        valid = 0
        while(not(valid)):
            try:
                i = input("%s: "%item)
                if(i==""):
                    ValueError
                elif(i[0].lower()=="c"):
                    return
                #i = int(i)
                values[0][counter] += int(i)
                changesMade = True
                valid = 1
            except ValueError:
                print("Integers only!")
                valid = 0
        counter+=1
    counter = 0
    print("\nCOINS")
    for item in KEYS[1]:
        valid = 0
        while(not(valid)):
            try:
                i = input("%s: "%item)
                if(i[0].lower()=="c"):
                    return
                #i = int(i)
                values[1][counter] += int(i)
                changesMade = True
                valid = 1
            except ValueError:
                print("Integers only!")
                valid = 0
        counter+=1
    billsList = parseBillsLine()
    if(billsList!=None):
        changesMade = True
        billsCoins['hundred']+=billsList[0]
        billsCoins['fifty']  +=billsList[1]
        billsCoins['twenty'] +=billsList[2]
        billsCoins['ten']    +=billsList[3]
        billsCoins['five']   +=billsList[4]
        billsCoins['two']    +=billsList[5]
        billsCoins['one']    +=billsList[6]
    else:
        return
    print("\nCOINS")
    coinsList = parseCoinsLine()
    if(coinsList!=None):
        changesMade = True
        billsCoins['dollar']    +=coinsList[0]
        billsCoins['halfdollar']+=coinsList[1]
        billsCoins['quarter']   +=coinsList[2]
        billsCoins['dime']      +=coinsList[3]
        billsCoins['nickel']    +=coinsList[4]
        billsCoins['penny']     +=coinsList[5]
    else:
        while(True):
            resp = input("Clear bills? (y/n) ")
            if(len(resp)>0 and resp[0].lower()=="y"):
                changesMade = False
                billsCoins['hundred']-=billsList[0]
                billsCoins['fifty']  -=billsList[1]
                billsCoins['twenty'] -=billsList[2]
                billsCoins['ten']    -=billsList[3]
                billsCoins['five']   -=billsList[4]
                billsCoins['two']    -=billsList[5]
                billsCoins['one']    -=billsList[6]
                print("Bills cleared.")
                return
            elif(len(resp)>0 and resp[0].lower()=="n"):
                print("Bills saved.")
                return
            else:
                print("Please enter 'y' or 'n'.")
        return
    return

menu = ["Add Bills & Coins",
        "Show Bills & Coins",
        "See Coin rollers",
        "Show Deposit",
        "Make Deposit",
        "Reload file",
        "Save & Quit"]
def menuMaker():
    counter = 1
    for item in menu:
        print("%d -%s" %(counter,item))
        counter+=1
    print("0 -Quit")

def main():
    global changesMade
    readINIFile()
    resp = 0
    while(1==1):
        total = currentValue()
        print("\nCurrent Total: $%0.2f" %total)
        if(coinRollers(0)):
            print("<< There are coins to roll. >>")
        try:
            menuMaker()
            resp = int(input("> "))
            if(resp==0): #menu[0] "Quit"
                if(not(changesMade)):
                    return
                while(1==1):
                    resp = input("Save changes? (y/n)")
                    if(("yes" in resp.lower()) or ("y" in resp.lower())):
                        saveFile()
                        return
                    elif(("no" in resp.lower()) or ("n" in resp.lower())):
                        return
                    elif(("cancel" in resp.lower()) or ("c" in resp.lower())):
                        break
                    else:
                        print("Please enter 'y' or 'n'.")
                        input("Press ENTER to continue.")
            elif(resp==1): #menu[1] "Add Bills & Coins"
                addMoney()
            elif(resp==2): #menu[2] "Show Bills & Coins"
                printValues()
            elif(resp==3): #menu[3] "See Coin rollers"
                coinRollers(1)
            elif(resp==4): #menu[4] "Show Deposit"
                calcDeposit()
            elif(resp==5): #menu[5] "Make Deposit"
                makeDeposit()
            elif(resp==6): #menu[6] "Reload file"
                readINIFile('myfile.txt')
            elif(resp==7): #menu[7] "Save & Quit"
                saveFile()
                return
            else:
                print("Please enter a number in range 0-%s" %len(menu))
            input("Press ENTER to continue.")
        except ValueError:
            print("Please enter numbers only.")
            input("Press ENTER to continue.")

main()
