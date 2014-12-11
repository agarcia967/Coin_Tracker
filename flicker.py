# flicker.py
from graphics import GraphWin, Point, Text, Rectangle

red = 'red3'
green = 'green4'
backdrop = 'lightgray'
width = 30
height = width/2

class Flicker():
    """ A Flicker acts as a switch and can hold a boolean state."""
    def __init__(self,center,state=True,label=None):
        """ Flicker(point,state=True,label=None) """
        self.center = center
        self.state = state
        self.elements = []
        if(label):
            self.label = Text(Point(self.center.getX(),self.center.getY()-width+10),label)
            self.elements.append(self.label)

        self.upperLeft = Point(self.center.getX()-width/2,self.center.getY()-height/2)
        self.lowerRight= Point(self.center.getX()+width/2,self.center.getY()+height/2)
        self.back = Rectangle(self.upperLeft,self.lowerRight)
        self.back.setWidth(width*.1)
        self.back.setFill(backdrop)
        self.elements.append(self.back)

        self.greenRect = Rectangle(Point(self.center.getX()-width/2,self.center.getY()-height/2),
                                   Point(self.center.getX(),self.center.getY()+height/2))
        self.greenRect.setFill(green)

        self.redRect = Rectangle(Point(self.center.getX(),self.center.getY()-height/2),
                                 Point(self.center.getX()+width/2,self.center.getY()+height/2))
        self.redRect.setFill(red)
    
    def setState(self,s):
        """ Set the state of the Flicker to s (True/False). """
        if(type(s)==type(True)):
            self.state = s
    
    def swapState(self):
        """ Switch the state of the Flicker to what it isn't.
            If it is currently True, make it False. """
        if(self.state==True):
            self.state = False
            self.undraw()
            self.draw(self.win)
        else:
            self.state = True
            self.undraw()
            self.draw(self.win)
    
    def getState(self):
        """ Get the current state of the Flicker (bool). """
        return self.state

    def setLabel(self,t):
        """ Set the Flicker's label. """
        self.label.setText(t)

    def getLabel(self):
        """ Get the Flicker's label as a string. """
        return self.label.getText()

    def clicked(self,click):
        """ If Point click is inside the Flicker swaps the state of the Flicker
            and returns True. """
        if(self.upperLeft.getX()<=click.getX()<=self.lowerRight.getX() and
           self.upperLeft.getY()<=click.getY()<=self.lowerRight.getY()):
            self.swapState()
            return True
        return False

    def draw(self, win):
        for e in self.elements:
            e.draw(win)
        self.win = win
        if(self.state):
            self.greenRect.draw(win)
        else:
            self.redRect.draw(win)

    def undraw(self):
        self.greenRect.undraw()
        self.redRect.undraw()
        for e in self.elements:
            e.undraw()

if __name__=="__main__":
    winW = 800
    winH = 600
    win = GraphWin("FlickerTester", winW, winH)
    win.setBackground('white')

    flicker = Flicker(Point(winW/2,winH/2),False,"Flicker")
    flicker.draw(win)
    while True:
        click = win.getMouse()
        if(not(flicker.clicked(click))):
            break
        print(flicker.getState())
    flicker.undraw()
    win.close()

