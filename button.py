import pygame

WHITE = (255, 255, 255)

class Button(pygame.sprite.Sprite):

    def __init__(self, x, y, w, h, c, name):

        super().__init__()

        # Create transparent sprite surface to draw sprite on
        self.image = pygame.Surface([w, h])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)

        # Setting attributes
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.name = name

        # Setting colour
        self.c = c

        # Drawing box
        self.draw()

        # Setting bounding rectangle of the drawn line
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


    def draw(self):

        # Draws line relative to the sprite surface
        
        c = self.c
        x = self.x
        y = self.y
        w = self.w
        h = self.h
        pygame.draw.rect(self.image, c, [0, 0, w, h])


    def inBounds(self, x, y):

        inX = x > self.x and x < self.x+self.w
        inY = y > self.y and x < self.y+self.h

        return inX and inY
