import pygame

WHITE = (255, 255, 255)

class Node(pygame.sprite.Sprite):

    def __init__(self, x, y, r, c):

        super().__init__()

        # Create transparent sprite surface to draw sprite on
        self.image = pygame.Surface([2*r, 2*r])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)

        # Setting colour and radius
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

    def draw(self):

        # Draws circle relative to the sprite surface
        
        c = self.c
        r = self.r
        pygame.draw.circle(self.image, c, [r, r], r)

    def setColour(self, c):
        self.c = c
        self.draw()

    
