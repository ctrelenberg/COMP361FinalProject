import pygame
from math import sqrt
from tools import get_font
from constants import WHITE, BLACK

class Node(pygame.sprite.Sprite):
    RADIUS = 30

    def __init__(self, x, y, r, c):

        super().__init__()

        # Create transparent sprite surface to draw sprite on
        self.image = pygame.Surface([2*r, 2*r])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)

        # Setting attributes
        self.x = x
        self.y = y
        self.c = c
        self.r = r

        # Drawing the circle
        self.draw()

        # Setting bounding rectangle of the drawn line
        self.rect = self.image.get_rect()
        self.rect.x = x-r
        self.rect.y = y-r

        # Set the parent to None, will set in algorithms
        self.parent = None

        self.costToReach = 0

        self.edges = []

        self.label = None
        self.label_rect = None
        self.label_text = None

    def set_label(self, text=None):
        if text is None:
            self.label = None
            self.label_text = None
            self.label_rect = None
            return
        self.label_text = text
        self.label = get_font().render(self.label_text, True, BLACK)
        textx = self.rect.x + Node.RADIUS
        texty = self.rect.y + Node.RADIUS
        tsrect = self.label.get_rect()
        tsrect.center = (textx, texty)
        self.label_rect = tsrect

    def get_label(self):
        return (self.label, self.label_rect)

    def has_label(self):
        return self.label is not None

    def addEdge(self, e):
        self.edges.append(e)

    def draw(self):

        # Draws circle relative to the sprite surface
        
        c = self.c
        r = self.r
        pygame.draw.circle(self.image, c, [r, r], r)
    

    def getPosition(self):

        return (self.x, self.y)


    def getX(self):
        
        return self.x


    def getY(self):

        return self.y
    

    def inBounds(self, x, y):

        return sqrt((self.x - x)**2 + (self.y - y)**2) <= self.r


    def removeEdge(self, e):
        self.edges.remove(e)
    

    def setColour(self, c):
        self.c = c
        self.draw()

    def getNeighbors(self):
        neighbors = []

        for edge in self.edges:
            if edge.n1 == self:
                neighbors.append(edge.n2)
            else:
                neighbors.append(edge.n1)
        
        return neighbors

