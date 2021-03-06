import pygame
from math import floor, sqrt
from tools import get_font
from constants import WHITE

class Edge(pygame.sprite.Sprite):

    def __init__(self, x1, y1, x2, y2, c, n1, n2, weight=0, app=None):

        super().__init__()

        # Create transparent sprite surface to draw sprite on
        self.image = pygame.Surface([abs(x1-x2), abs(y1-y2)])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)

        # Setting global endpoints
        self.x1 = x1
        self.y1 = y1

        self.x2 = x2
        self.y2 = y2

        # Adding nodes
        self.n1 = n1
        self.n2 = n2

        # Setting line colour
        self.c = c

        # Setting weight

        # Changing weight to the length of the line
        # self.weight = str(weight)
        self.weight = str(floor(sqrt(abs(x1-x2)**2 + abs(y1-y2)**2)))
        self.text = get_font().render(self.weight, True, (255,255,255), (40,40,40))
        self.scr = app.screen
        tr = self.text.get_size()

        midx = (x1 + x2) / 2
        midy = (y1 + y2) / 2
        ltpos = (midx - tr[0]/2, midy - tr[1]/2)

        self.text_rect = pygame.Rect(ltpos, tr)
        print(self.text_rect)

        # Drawing line
        self.draw()

        # Setting bounding rectangle of the drawn line
        self.rect = self.image.get_rect()
        self.rect.x = min(x1, x2)
        self.rect.y = min(y1, y2)


    def draw(self):

        # Draws line relative to the sprite surface
        
        c = self.c
        x1 = self.x1
        y1 = self.y1
        x2 = self.x2
        y2 = self.y2

        start, end = self.convertEndpoints()
        pygame.draw.line(self.image, c, start, end, 5)


    def draw_label(self):
        self.scr.blit(self.text, self.text_rect)


    def convertEndpoints(self):

        # Takes the global endpoint values and converts them
        # to relative values for the sprite surface
        
        x1 = self.x1
        y1 = self.y1
        x2 = self.x2
        y2 = self.y2

        if x1 <= x2 and y1 <= y2:
            return [0, 0], [x2-x1, y2-y1]
        elif x1 <= x2 and y1 > y2:
            return [0, y1-y2], [x2-x1, 0]
        elif x1 > x2 and y1 > y2:
            return [0, 0], [x1-x2, y1-y2]
        elif x1 > x2 and y1 <= y2:
            return [0, y2-y1], [x1-x2, 0]


    def getEndpoints(self):

        return (self.x1, self.y1), (self.x2, self.y2)


    def getEndpoint1(self):

        return (self.x1, self.y1)


    def getEndpoint2(self):

        return (self.x2, self.y2)


    def getNode1(self):

        return self.n1


    def getNode2(self):

        return self.n2


    def getPosition(self):
        
        return (self.x, self.y)
        

    def setColour(self, c):
        self.c = c
        self.draw()
