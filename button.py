import pygame
from constants import BUTTON_WIDTH, BUTTON_HEIGHT, BLACK, WHITE, GREY
from tools import get_font


class Button(pygame.sprite.Sprite):

    def __init__(self, x, y, w, h, c, name, tags=None):
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
        self.deselect_col = None

        # Drawing box
        self.draw()

        # Setting bounding rectangle of the drawn line
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Tags
        self.tags = tags

        # Rendering button text
        self.textSurf = get_font().render(self.name, True, BLACK)
        textx = x + BUTTON_WIDTH // 2
        texty = y + BUTTON_HEIGHT // 2
        tsrect = self.textSurf.get_rect()
        tsrect.center = (textx, texty)
        self.textRect = tsrect

    def get_text(self):
        return (self.textSurf, self.textRect)

    def set_deselected(self, deselect_col = GREY):
        self.deselect_col = deselect_col
        self.draw()

    def set_selected(self, deselect_col = GREY):
        self.deselect_col = None
        self.draw()

    def draw(self):
        # Draws line relative to the sprite surface

        c = self.c
        x = self.x
        y = self.y
        w = self.w
        h = self.h
        pygame.draw.rect(self.image, c if self.deselect_col is None else self.deselect_col, [0, 0, w, h])

    def inBounds(self, x, y):
        inX = x > self.x and x < self.x + self.w
        inY = y > self.y and y < self.y + self.h

        return inX and inY
