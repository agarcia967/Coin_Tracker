# Coin Tracker.py
__author__ = "Anthony R. Garcia <agarcia967@hotmail.com>"
__date__ = "10/20/2014"
__version__ = "1.0"
__credits__ = None

import os

FILENAME = "cointracker.ini"
CENT_SYMBOL = u"\u00A2"
SECTIONS = ["bills","coins"]
KEYS = [["hundred","fifty","twenty","ten","five","two","one"],
        ["dollar","halfdollar","quarter","dime","nickel","penny"]]
values = [[0 for i in range(len(KEYS[i]))] for i in range(len(KEYS))]
changesMade = False

def saveFile():
    global changesMade
    print("Writing file '%s'. Please wait... " %FILENAME, end='')
    outFile = open(FILENAME,'w')
    outFile.write("#DO NOT move this file!\n")
    sectionCounter = 0
    for section in SECTIONS:
        keyCounter = 0
        outFile.write("[%s]\n" %section.upper())
        for key in KEYS[sectionCounter]:
            outFile.write("%s=%s\n" %(KEYS[sectionCounter][keyCounter],values[sectionCounter][keyCounter]))
            keyCounter+=1
        sectionCounter+=1
    outFile.close()
    print("Done.")
    changesMade = False

def readINIFile():
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
            if(key in KEYS[currentSection]):
                values[currentSection][KEYS[currentSection].index(key)] = value
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
    print(" $100.00 - %d" %values[0][0])
    print(" $ 50.00 - %d" %values[0][1])
    print(" $ 20.00 - %d" %values[0][2])
    print(" $ 10.00 - %d" %values[0][3])
    print(" $  5.00 - %d" %values[0][4])
    print(" $  2.00 - %d" %values[0][5])
    print(" $  1.00 - %d" %values[0][6])
    billsTotal = sum([values[0][0]*100,
                      values[0][1]*50,
                      values[0][2]*20,
                      values[0][3]*10,
                      values[0][4]*5,
                      values[0][5]*2,
                      values[0][6]*1])
    print("Bills Total: $%0.2f" %billsTotal)
    print("\n  COINS")
    print(" $1.00 - %3.0d" %values[1][0])
    print("   50%s - %3.0d" %(CENT_SYMBOL,values[1][1]))
    qR = values[1][2]//40
    dR = values[1][3]//50
    nR = values[1][4]//40
    pR = values[1][5]//50
    e=""
    if(qR):
        e="(%s)" %qR
    print("   25%s - %3.0d %s" %(CENT_SYMBOL,values[1][2],e))
    
    e=""
    if(dR):
        e="(%s)" %dR
    print("   10%s - %3.0d %s" %(CENT_SYMBOL,values[1][3],e))
    e=""
    if(nR):
        e="(%s)" %nR
    print("    5%s - %3.0d %s" %(CENT_SYMBOL,values[1][4],e))
    e=""
    if(pR):
        e="(%s)" %pR
    print("    1%s - %3.0d %s" %(CENT_SYMBOL,values[1][5],e))
    coinsTotal = sum([values[1][0]*1,
                      values[1][1]*.5,
                      values[1][2]*.25,
                      values[1][3]*.10,
                      values[1][4]*.05,
                      values[1][5]*.01,])
    print("Coins Total: $%0.2f\n" %coinsTotal)

def calcDeposit():
    print("\nCalculating...")
    depositAll = 0
    depositValue = 0
    depositValue+=values[0][0]*100
    depositValue+=values[0][1] *50
    depositValue+=values[0][2] *20
    depositValue+=values[0][3] *10
    depositValue+=values[0][4] * 5
    if(depositAll):
        depositValue+=values[0][5] * 2
    else:
        print("[$2 bills omitted]")
    depositValue+=values[0][6] * 1
    billsOnly = depositValue

    if(depositAll):
        depositValue+=values[1][0] *1.00
    else:
        print("[$1 coins omitted]")
    if(depositAll):
        depositValue+=values[1][1] * .50
    else:
        print("[50%s coins omitted]" %CENT_SYMBOL)
    depositValue+=((values[1][2]//40)*10)
    depositValue+=((values[1][3]//50)*5)
    depositValue+=((values[1][4]//40)*2)
    depositValue+=((values[1][5]//50)*.5)
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
    values[0][0] = 0 #hundreds
    values[0][1] = 0 #fifties
    values[0][2] = 0 #twenties
    values[0][3] = 0 #tens
    values[0][4] = 0 #fives
    if(depositAll):
        values[0][5] = 0 #twos
    else:
        print("[$2 bills omitted]")
    values[0][6] = 0 #ones

    if(depositAll):
        values[1][0] = 0 #dollar coins
    else:
        print("[$1 coins omitted]")
    if(depositAll):
        values[1][1] = 0 #fifty cent coins
    else:
        print("[50%s coins omitted]" %CENT_SYMBOL)
    values[1][2] = values[1][2] % 40 #quarters
    values[1][3] = values[1][3] % 50 #dimes
    values[1][4] = values[1][4] % 40 #nickels
    values[1][5] = values[1][5] % 50 #pennies
    print("Deposited amounts removed from current values.")
    changesMade = True

def currentValue():
    totalValue = 0
    totalValue+=values[0][0]*100
    totalValue+=values[0][1] *50
    totalValue+=values[0][2] *20
    totalValue+=values[0][3] *10
    totalValue+=values[0][4] * 5
    totalValue+=values[0][5] * 2
    totalValue+=values[0][6] * 1

    totalValue+=values[1][0] *1.00
    totalValue+=values[1][1] * .50
    totalValue+=values[1][2] * .25
    totalValue+=values[1][3] * .10
    totalValue+=values[1][4] * .05
    totalValue+=values[1][5] * .01
    return totalValue

def coinRollers(isPrinter):
    qRolls = values[1][2]//40
    dRolls = values[1][3]//50
    nRolls = values[1][4]//40
    pRolls = values[1][5]//50
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
                readINIFile()
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
