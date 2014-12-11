# button.py
from graphics import *

class Button:
    """ This Button class was written by John Zelle and requires his graphics.py
    class to instantiate.
    A button is a labeled rectangle in a window.
    It is activated or deactivated with the activate()
    and deactivate() methods. The clicked(p) method
    returns true if the button is active and p is inside it."""

    def __init__(self, center, width, label):
        """ Creates a rectangular button, eg:
        qb = Button(centerPoint, width, 'Quit') """

        w,h = width/2.0, (20)/2.0
        x,y = center.getX(), center.getY()
        self.xmax, self.xmin = x+w, x-w
        self.ymax, self.ymin = y+h, y-h
        p1 = Point(self.xmin, self.ymin)
        p2 = Point(self.xmax, self.ymax)
        self.rect = Rectangle(p1,p2)
        self.rect.setFill('lightgray')
        self.label = Text(center, label)

    def clicked(self, p):
        "Returns true if button active and p is inside"
        return (self.active and
                self.xmin <= p.getX() <= self.xmax and
                self.ymin <= p.getY() <= self.ymax)

    def getLabel(self):
        "Returns the label string of this button."
        return self.label.getText()

    def activate(self):
        "Sets this button to 'active'."
        self.label.setFill('black')
        self.rect.setWidth(2)
        self.active = True

    def deactivate(self):
        "Sets this button to 'inactive'."
        self.label.setFill('darkgray')
        self.rect.setWidth(1)
        self.active = False

    def draw(self, win):
        "Draws the button in win"
        self.rect.draw(win)
        self.label.draw(win)
        self.activate()

    def undraw(self):
        "Draws the button in win"
        self.rect.undraw()
        self.label.undraw()
        self.activate()
