# ticker.py
from graphics import GraphWin, Point, Entry, Text
from button import Button

class Ticker():
    """ A Ticker which allows the user to increase or decrease
        the value of the button with one click."""
    def __init__(self,center,label):
        """ __init__(Point()) """
        self.center = center
        self.elements = []
        self.labelText = label
        self.minimum = None
        self.maximum = None
        self.increment = 1
        self.entry = Entry(Point(self.center.getX(),self.center.getY()-11),4)
        self.entry.setText(0)
        self.elements.append(self.entry)

        self.label = Text(Point(self.center.getX(),self.center.getY()-31),self.labelText)
        self.elements.append(self.label)
        self.bDown = Button(Point(self.center.getX()+10,self.center.getY()+11),20,"-")
        self.elements.append(self.bDown)
    
        self.bUp = Button(Point(self.center.getX()-10,self.center.getY()+11),20,"+")
        self.elements.append(self.bUp)

    def setMin(self,m):
        """ The minimum value the """
        self.minimum = m
    
    def setMax(self,m):
        self.maximum = m

    def _validateEntry(self):
        item = self.entry.getText()
        try:
            i = int(item)
            return i
        except ValueError:
            self.entry.setText(item)
        return 0
        
    def setEntry(self,s):
        self.entry.setText(s)

    def getEntry(self):
        return self._validateEntry()

    def setLabel(self,s):
        self.label.setText(s)

    def getLabel(self):
        return self.labelText

    def clicked(self,click):
        if(self.bUp.clicked(click)):
            number = self._validateEntry()
            if(self.maximum==None or number+1<=self.maximum):
                number+=self.increment
            self.entry.setText(number)
            return True
        elif(self.bDown.clicked(click)):
            number = self._validateEntry()
            if(self.minimum==None or number-1>=self.minimum):
                number-=self.increment
            self.entry.setText(number)
            return True
        return False

    def draw(self, win):
        for e in self.elements:
            e.draw(win)

    def undraw(self):
        for e in self.elements:
            e.undraw()

if __name__=="__main__":
    winW = 800
    winH = 600
    win = GraphWin("TickerTester", winW, winH)
    win.setBackground('white')

    ticker = Ticker(Point(winW/2,winH/2),"Ticker")
    ticker.setMax(6)
    ticker.setMin(0)
    ticker.draw(win)
    while True:
        click = win.getMouse()
        ticker.clicked(click)
        if(ticker.getEntry()>=100):
            break
    ticker.undraw()
    win.close()

