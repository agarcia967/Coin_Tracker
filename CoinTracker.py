# GUICoinTracker.py
__author__ = "Anthony R. Garcia <agarcia967@hotmail.com>"
__date__ = "11/11/2014"
__version__ = "4.0" #now with a GUI using graphics.py
__credits__ = None

from graphics import GraphWin, Point, Text, Rectangle, Line, Entry
from ticker import Ticker
from flicker import Flicker
from button import Button
import os

CENT_SYMBOL = u"\u00A2"
changesMade = False

def changesMadeTrue():
    global changesMade
    changesMade = True
    print("changesMade =",changesMade)

def changesMadeFalse():
    global changesMade
    changesMade = False
    print("changesMade =",changesMade)
    
def draw(elements,window):
    for e in elements:
        e.draw(window)

def undraw(elements):
    for e in elements:
        e.undraw()

def popup(win,prompt,positive_button_label,negative_button_label,neutral_button_label=None,is_input_type=False):
    print("[UI] PopUp")
    print("  '%s'" %prompt)
    print("  T: '%s'" %positive_button_label)
    if(neutral_button_label!=None):
        print("  N: '%s'" %neutral_button_label)
    print("  F: '%s'" %negative_button_label)
    if type(prompt)==type([]):
        list = prompt
        prompt = ""
        for i in list:
            prompt+=i
            if(list.index(i)<len(list)-1):
                prompt+="\n"
    winW, winH = win.getWidth(), win.getHeight()
    elements = []
    popT = winH*.30
    popL = winW*.30
    popB = winH*.70
    popR = winW*.70
    window = Rectangle(Point(popL,popT),Point(popR,popB))
    window.setWidth(2)
    window.setFill('lightblue')
    elements.append(window)
    
    prpt = Text(Point((popL+popR)/2,(popT+popB)*.45),prompt)
    elements.append(prpt)

    autowidth = 9
    bPositive = Button(Point((winW*.5+popR)*.5,(popT+popB)*.6), (len(positive_button_label)*autowidth), positive_button_label)
    elements.append(bPositive)

    if(is_input_type):
        entry = Entry(Point(winW/2,winH/2), 20)
        elements.append(entry)

    if(neutral_button_label):
        bNeutral = Button(Point((popL+popR)*.5,(popT+popB)*.6), (len(neutral_button_label)*autowidth), neutral_button_label)
        elements.append(bNeutral)
    
    bNegative = Button(Point((popL+winW*.5)*.5,(popT+popB)*.6), (len(negative_button_label)*autowidth), negative_button_label)
    elements.append(bNegative)
    
    draw(elements,win)
    while True:
        click = win.getMouse()
        if(bPositive.clicked(click)):
            undraw(elements)
            print("[UI] '%s'" %positive_button_label)
            if(is_input_type):
                return entry.getText()
            return True
        elif(bNegative.clicked(click)):
            undraw(elements)
            print("[UI] '%s'" %negative_button_label)
            return False
        elif(neutral_button_label!=None and bNeutral.clicked(click)):
            undraw(elements)
            print("[UI] '%s'" %neutral_button_label)
            return None

def dictToTotalValue(dict):
    mySum = 0
    mySum+=dict['hundred'] * 100
    mySum+=dict['fifty'] * 50
    mySum+=dict['twenty'] * 20
    mySum+=dict['ten'] * 10
    mySum+=dict['five'] * 5
    mySum+=dict['two'] * 2
    mySum+=dict['one'] * 1
    
    mySum+=dict['dollar'] * 1
    mySum+=dict['halfdollar'] * .50
    mySum+=dict['quarter'] * .25
    mySum+=dict['dime'] * .10
    mySum+=dict['nickel'] * .05
    mySum+=dict['penny'] * .01
    return mySum

def dictToBillValue(dict, inclMiscBills=False):
    mySum = 0
    mySum+=dict['hundred'] * 100
    mySum+=dict['fifty'] * 50
    mySum+=dict['twenty'] * 20
    mySum+=dict['ten'] * 10
    mySum+=dict['five'] * 5
    if(inclMiscBills):
        mySum+=dict['two'] * 2
    mySum+=dict['one'] * 1
    return mySum

def dictToCoinValue(dict, inclMiscCoins=False):
    mySum = 0
    if(inclMiscCoins):
        mySum+=dict['dollar'] * 1
        mySum+=dict['halfdollar'] * .50
    mySum+=dict['quarter'] * .25
    mySum+=dict['dime'] * .10
    mySum+=dict['nickel'] * .05
    mySum+=dict['penny'] * .01
    return mySum

def dictToRollers(dict):
    list = []
    list.append(dict['quarter']//40)
    list.append(dict['dime']//50)
    list.append(dict['nickel']//40)
    list.append(dict['penny']//50)
    return list

def deposit(dict,inclMiscBills,returnOnly=True):
    mySum = 0
    mySum+=dict['hundred'] * 100
    mySum+=dict['fifty'] * 50
    mySum+=dict['twenty'] * 20
    mySum+=dict['ten'] * 10
    mySum+=dict['five'] * 5
    if(inclMiscBills):
        mySum+=dict['two'] * 2
        if not returnOnly:
            dict['two'] = 0
    mySum+=dict['one'] * 1
    if not returnOnly:
        dict['hundred'] = 0
        dict['fifty'] = 0
        dict['twenty'] = 0
        dict['ten'] = 0
        dict['five'] = 0
        dict['one'] = 0
    billSum = mySum

    mySum+=(dict['quarter']//40) * 10
    mySum+=(dict['dime']//50) * 5
    mySum+=(dict['nickel']//40) * 2
    mySum+=(dict['penny']//50) * .5
    if not returnOnly:
        dict['quarter']%=40
        dict['dime']%=50
        dict['nickel']%=40
        dict['penny']%=50
        changesMadeTrue()
    return billSum, mySum

def getDict(keys,values):
    dictionary = {}
    if(len(keys)!=len(values)):
        return dictionary
    for i in range(len(values)):
        dictionary[keys[i]] = int(values[i].getEntry())
    return dictionary

def loadFile(FILENAME="cointracker.ini"):
    SECTIONS = ("bills","coins")
    BILLS = ("hundred","fifty","twenty","ten","five","two","one")
    COINS = ("dollar","halfdollar","quarter","dime","nickel","penny")
    
    loadedDict = {}
    print("Reading file '%s'. Please wait... " %FILENAME, end='')
    if(not(os.path.exists(FILENAME))):
        print("File does not exist.")
        return None
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
                return False
        elif(line):
            ll = line.split("=")
            for item in ll:
                ll[ll.index(item)] = item.strip()
            key = ll[0]
            value = int(ll[1])
            loadedDict[key] = value
        else:
            print("FILE READ ERROR\n::Unknown Error")
            return False
    inFile.close()
    print("Done.")
    return loadedDict

def saveFile(dict):
    SECTIONS = ("bills","coins")
    BILLS = ("hundred","fifty","twenty","ten","five","two","one")
    COINS = ("dollar","halfdollar","quarter","dime","nickel","penny")
    FILENAME = 'cointracker.ini'
    
    print("Writing dict to file '%s'. Please wait... " %FILENAME, end='')
    try:
        outFile = open(FILENAME,'w')
        outFile.write("#DO NOT move this file!\n")
        sectionCounter = 0
        for section in SECTIONS:
            outFile.write("[%s]\n" %section.upper())
            for key in dict:
                if(key in COINS and section=="coins"):
                    outFile.write("%s=%s\n" %(key,str(dict[key])))
                elif(key in BILLS and section=="bills"):
                    outFile.write("%s=%s\n" %(key,str(dict[key])))
            sectionCounter+=1
        outFile.close()
        print("Done.")
        return True
    except Exception:
        print("Error.\nUnknown Exception")
        return False

def updateBCValue(value,textDisplay):
    string = "$%7.2f" %value
    textDisplay.setText(string)

def updateDollarValue(dict,textDisplay):
    value = dictToTotalValue(dict)
    string = "$%8.2f" %value
    if(value>=1000):
        textDisplay.setFill('red')
        textDisplay.setStyle('bold')
    elif(value>=800):
        textDisplay.setFill('orange')
        textDisplay.setStyle('bold')
    elif(value>=500):
        textDisplay.setFill('blue')
        textDisplay.setStyle('bold')
    textDisplay.setText(string)

def updateRollers(intList,displaysList):
    displaysList[0].setText(intList[0])#quarters
    displaysList[1].setText(intList[1])#dimes
    displaysList[2].setText(intList[2])#nickels
    displaysList[3].setText(intList[3])#pennies

def updateRollersValue(intList,textDisplay):
    value = 0
    value += intList[0]*10.00 #quarters
    value += intList[1]* 5.00 #dimes
    value += intList[2]* 2.00 #nickels
    value += intList[3]* 0.50 #pennies
    string = "$%5.2f" %value
    textDisplay.setText(string)

def updateTickers(dict,tickers):
    for e in tickers:
        #print(e.getLabel())
        if(e.getLabel()=="$100"):
            e.setEntry(dict['hundred'])
        elif(e.getLabel()=="$50"):
            e.setEntry(dict['fifty'])
        elif(e.getLabel()=="$20"):
            e.setEntry(dict['twenty'])
        elif(e.getLabel()=="$10"):
            e.setEntry(dict['ten'])
        elif(e.getLabel()=="$5"):
            e.setEntry(dict['five'])
        elif(e.getLabel()=="$2"):
            e.setEntry(dict['two'])
        elif(e.getLabel()=="$1"):
            e.setEntry(dict['one'])
        elif(e.getLabel()=="$1.00"):
            e.setEntry(dict['dollar'])
        elif(e.getLabel()==("50%s"%CENT_SYMBOL)):
            e.setEntry(dict['halfdollar'])
        elif(e.getLabel()==("25%s"%CENT_SYMBOL)):
            e.setEntry(dict['quarter'])
        elif(e.getLabel()==("10%s"%CENT_SYMBOL)):
            e.setEntry(dict['dime'])
        elif(e.getLabel()==("5%s"%CENT_SYMBOL)):
            e.setEntry(dict['nickel'])
        elif(e.getLabel()==("1%s"%CENT_SYMBOL)):
            e.setEntry(dict['penny'])

def main():
    winW = 800
    winH = 600
    win = GraphWin("Coin Tracker", winW, winH)
    win.setBackground('white')

    BILLS = ("$100","$50","$20","$10","$5","$2","$1")
    COINS = ("$1.00",("50%s"%CENT_SYMBOL),("25%s"%CENT_SYMBOL),("10%s"%CENT_SYMBOL),("5%s"%CENT_SYMBOL),("1%s"%CENT_SYMBOL))
    TBILLS = ("hundred","fifty","twenty","ten","five","two","one")
    TCOINS = ("dollar","halfdollar","quarter","dime","nickel","penny")

    elements = []
    buttonY = winH*.05
    bSave = Button(Point(winW*.05,buttonY),50,"Save")
    elements.append(bSave)
    bLoad = Button(Point(winW*.15,buttonY),50,"Load")
    elements.append(bLoad)
    bDeposit = Button(Point(winW*.25,buttonY),60,"Deposit")
    elements.append(bDeposit)
    bQuit = Button(Point(winW*.95,buttonY),50,"Quit")
    elements.append(bQuit)
    SAVE_ANCHOR = Point(winW*.05,buttonY+30)
    LOAD_ANCHOR = Point(winW*.15,buttonY+30)
    DEPOSIT_ANCHOR = Point(winW*.25,buttonY+30)
    
    title = Text(Point(winW*.50,winH*.10),"Coin Tracker")
    title.setStyle('bold italic')
    title.setSize(20)
    elements.append(title)
    elements.append(Text(Point(winW*.44,winH*.15),"Value:"))
    totalValueDisp = Text(Point(winW*.53,winH*.15),"0")
    totalValueDisp.setFace('courier')
    elements.append(totalValueDisp)

    tickers = []
    billsRow = winH*.50
    coinsRow = winH*.66
    for i in range(len(BILLS)):
        t = Ticker(Point(100+55*i,billsRow),BILLS[i])
        t.setMin(0)
        tickers.append(t)
    for i in range(len(COINS)):
        t = Ticker(Point(100+55*i,coinsRow),COINS[i])
        t.setMin(0)
        tickers.append(t)
    elements += tickers

    flickers = []
    fMiscBills = Flicker(Point(winW*.62,billsRow),False,"Misc Bills")
    flickers.append(fMiscBills)

    fMiscCoins = Flicker(Point(winW*.62,coinsRow),False,"Misc Coins")
    flickers.append(fMiscCoins)
    elements+=flickers
    
    elements.append(Text(Point(winW*.75,billsRow*.93),"Bills Total:"))
    billsValueDisp = Text(Point(winW*.75,billsRow*1.01),"0")
    billsValueDisp.setFace('courier')
    elements.append(billsValueDisp)

    elements.append(Text(Point(winW*.75,coinsRow*.95),"Coins Total:"))
    coinsValueDisp = Text(Point(winW*.75,coinsRow*1.01),"0")
    coinsValueDisp.setFace('courier')
    elements.append(coinsValueDisp)

    coinRollDisp = []
    tableXL = winW*.68
    tableXR = winW*.864
    tableYT = winH*.15
    tableYB = winH*.41
    crTable = Rectangle(Point(tableXL,tableYT),Point(tableXR,tableYB))
    coinRollDisp.append(crTable)
    crTitle = Text(Point(winW*.77,winH*.18),"Coin Rollers")
    crTitle.setStyle('bold')
    coinRollDisp.append(crTitle)
    for i in range(5):
        coinRollDisp.append(Line(Point(tableXL,winH*.20+(25*i)),Point(tableXR,winH*.20+(25*i))))
    coinRollDisp.append(Line(Point(winW*.79,tableYT+30),Point(winW*.79,tableYB)))

    nameCol = winW*.73
    numCol = winW*.83
    topRow = winH*.22
    rowSpcg = winH*.042
    coinRollDisp.append(Text(Point(nameCol,topRow),"Quarters"))
    qRolls = Text(Point(numCol,topRow),"0")
    coinRollDisp.append(qRolls)
    topRow+=rowSpcg
    coinRollDisp.append(Text(Point(nameCol,topRow),"Dimes"))
    dRolls = Text(Point(numCol,topRow),"0")
    coinRollDisp.append(dRolls)
    topRow+=rowSpcg
    coinRollDisp.append(Text(Point(nameCol,topRow),"Nickels"))
    nRolls = Text(Point(numCol,topRow),"0")
    coinRollDisp.append(nRolls)
    topRow+=rowSpcg
    coinRollDisp.append(Text(Point(nameCol,topRow),"Pennies"))
    pRolls = Text(Point(numCol,topRow),"0")
    coinRollDisp.append(pRolls)
    topRow+=rowSpcg
    coinRollDisp.append(Text(Point(nameCol,topRow),"Total"))
    rollersValueDisp = Text(Point(numCol,topRow),"0")
    coinRollDisp.append(rollersValueDisp)
    elements += coinRollDisp

    draw(elements,win)

    errorMsg = Text(LOAD_ANCHOR,"New Error Message")
    errorMsg.setFill('red')
    
    mydict = {"hundred":0,"fifty":0,"twenty":0,"ten":0,"five":0,"two":0,"one":0,
              "dollar":0,"halfdollar":0,"quarter":0,"dime":0,"nickel":0,"penny":0}
    print("Initial file read:")
    result = loadFile()
    if result==None:
        errorMsg.setText("File not found.")
        errorMsg.draw(win)
    elif(type(result)==type(mydict)):
        errorMsg.setText("File read successful.")
        errorMsg.setFill('green')
        errorMsg.draw(win)
        mydict = result
        changesMadeFalse()
    else:
        errorMsg.setText("File read error.")
        errorMsg.draw(win)
        
    while True:
        updateTickers(mydict,tickers)
        updateDollarValue(mydict,totalValueDisp)
        updateBCValue(dictToBillValue(mydict,fMiscBills.getState()),billsValueDisp)
        updateBCValue(dictToCoinValue(mydict,fMiscCoins.getState()),coinsValueDisp)
        updateRollers(dictToRollers(mydict),[qRolls,dRolls,nRolls,pRolls])
        updateRollersValue(dictToRollers(mydict),rollersValueDisp)
        p = win.getMouse()
        errorMsg.setFill('red')
        errorMsg.undraw()

        tickerFlag = False
        for e in tickers:
            tickerClickResult = e.clicked(p)
            if(tickerFlag==False and tickerClickResult):
                tickerFlag = True
        if(tickerFlag):
            mydict = getDict(TBILLS+TCOINS,tickers)
            print("[UI] Ticker")
            changesMadeTrue()
        flickerFlag = False
        for e in flickers:
            flickerClickResult = e.clicked(p)
            if(flickerFlag==False and flickerClickResult):
                flickerFlag = True
        if(flickerFlag):
            print("[UI] Flicker")
        
        if(bQuit.clicked(p)):
            print("[UI] Quit")
            result = True
            if(changesMade):
                undraw(tickers)
                result = popup(win,"Any unsaved changes will be lost.\nAre you sure you want to quit?","Quit","Cancel","Save & Quit")
                draw(tickers,win)
            if(result==None):
                result = saveFile(mydict)
                if not result:
                    errorMsg.setText("File could not be saved.")
                    errorMsg.anchor = SAVE_ANCHOR
                    errorMsg.draw(win)
                else:
                    win.close()
                    return
            elif(result):
                win.close()
                return
        elif(bSave.clicked(p)):
            print("[UI] Save")
            result = saveFile(mydict)
            if result:
                errorMsg.anchor = SAVE_ANCHOR
                errorMsg.setFill('green')
                errorMsg.setText("Saved!")
                errorMsg.draw(win)
                changesMadeFalse()
            else:
                errorMsg.anchor = SAVE_ANCHOR
                errorMsg.setText("File could not be saved.")
                errorMsg.draw(win)
        elif(bDeposit.clicked(p)):
            print("[UI] Deposit")
            undraw(tickers)
            bills,total = deposit(mydict,fMiscBills.getState(),True)
            result = popup(win,"Are you sure you want to make a deposit?\nBills: $%0.2f\nCoins: $%0.2f\nTotal: $%0.2f"%(bills,total-bills,total)," Yes "," No ")
            draw(tickers,win)
            if(result):
                bills,total = deposit(mydict,fMiscBills.getState())
                print(bills,total)
                errorMsg.anchor = DEPOSIT_ANCHOR
                errorMsg.setFill('green')
                errorMsg.setText("Deposit complete.")
                errorMsg.draw(win)
                changesMadeTrue()
        elif(bLoad.clicked(p)):
            print("[UI] Load")
            undraw(tickers)
            result = popup(win, "What file would you like to load?", " OK ", "Cancel", is_input_type=True)
            draw(tickers,win)
            if(type(result)==type("")):
                filename = result
                result = loadFile(filename)
                if result==None:
                    errorMsg.anchor = LOAD_ANCHOR
                    errorMsg.setText("File not found.")
                    errorMsg.draw(win)
                elif(type(result)==type(mydict)):
                    errorMsg.anchor = LOAD_ANCHOR
                    errorMsg.setText("File read successful.")
                    errorMsg.setFill('green')
                    errorMsg.draw(win)
                    mydict = result
                    changesMadeTrue()
                else:
                    errorMsg.anchor = LOAD_ANCHOR
                    errorMsg.setText("File read error.")
                    errorMsg.draw(win)
        else:
            mydict = getDict(TBILLS+TCOINS,tickers)

main()
