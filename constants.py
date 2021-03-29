import pygame

BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 126, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
GREY = (210, 210, 210)
D_GREY = (105, 105, 105)
WHITE = (255, 255, 255)

infoObject = pygame.display.Info()
SCREENWIDTH = infoObject.current_w // 2
SCREENHEIGHT = infoObject.current_h // 2
SCREEN_SIZE = (SCREENWIDTH, SCREENHEIGHT)

BUTTON_WIDTH = 80
BUTTON_HEIGHT = 30

class Colours:
    CURRENT_NODE = (255,140,0)
    VISITED = D_GREY
    PATH_NODE = (0, 255, 100)