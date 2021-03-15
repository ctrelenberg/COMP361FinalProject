# Import Pygame, sqrt, and my classes
import pygame

from node import Node
from edge import Edge
from button import Button
from math import sqrt

pygame.init()

# Defining colours
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
GREY = (210, 210, 210)
D_GREY = (105, 105, 105)
WHITE = (255, 255, 255)

# Constants
RADIUS = 30

# Define and create window
infoObject = pygame.display.Info()
SCREENWIDTH = infoObject.current_w // 2
SCREENHEIGHT = infoObject.current_h // 2

size = (SCREENWIDTH, SCREENHEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("COMP361")

# Groups to hold edges and nodes, separately
all_nodes = pygame.sprite.Group()
all_edges = pygame.sprite.Group()

# Add buttons
WIDTH = 80
HEIGHT = 30
buttons = pygame.sprite.Group()
buttons.add(Button(10, SCREENHEIGHT-HEIGHT-10, WIDTH, HEIGHT, GREEN))
buttons.add(Button(20+WIDTH, SCREENHEIGHT-HEIGHT-10, WIDTH, HEIGHT, RED))
buttons.add(Button(10*3+WIDTH*2, SCREENHEIGHT-HEIGHT-10, WIDTH, HEIGHT, YELLOW))

# Loop flag and setting up pygame clock
appRunning = True
stepAlg = False
runAlg = False
clock = pygame.time.Clock()

# Counter for when to change node colour
i = 1

while appRunning:

    #---------------------------------------------------------------------------
    # User input handling
    
    for event in pygame.event.get(): # Check all user events
        
        if event.type == pygame.QUIT: # If user hit close, quit
            appRunning = False

        elif event.type == pygame.MOUSEBUTTONDOWN: # If mouse down, store pos
            
            pos_down = pygame.mouse.get_pos()

        elif event.type == pygame.MOUSEBUTTONUP: # If user lifts mouse button...

            pos_up = pygame.mouse.get_pos() # Get new position
            
            dx = pos_up[0] - pos_down[0]
            dy = pos_up[1] - pos_down[1]

            if sqrt(dx**2 + dy**2) > 50: # If new pos is more than 50 pxls away

                # Flags for points that occur within nodes
                valid1 = False
                valid2 = False
                # Flag for duplicate edge
                isDup = False

                # Sorting the two points for ease of comparison
                sorted_pos = sorted([pos_down, pos_up])
                pos_down = sorted_pos[0]
                pos_up = sorted_pos[1]

                # Check that the endpoints occur within nodes
                for node in all_nodes:
                    # Fix the endpoints to the centers of nodes if valid
                    if node.inBounds(pos_down[0], pos_down[1]):
                        valid1 = True
                        x1 = node.getX()
                        y1 = node.getY()
                    if node.inBounds(pos_up[0], pos_up[1]):
                        valid2 = True
                        x2 = node.getX()
                        y2 = node.getY()

                # Check to see if edge is a duplicate, delete edge if it is
                for edge in all_edges:
                    point1, point2 = edge.getEndpoints()
                    if point1 == (x1, y1) and point2 == (x2, y2):
                        isDup = True
                        edge.kill()
                    
                if valid1 and valid2 and (not isDup):
                    all_edges.add(Edge(x1, y1, x2, y2, BLACK)) # Add an edge
                x1, y1, x2, y2 = None, None, None, None
                
            else: # If not, create a new node

                valid = True
                
                pos = pygame.mouse.get_pos()

                for node in all_nodes:
                    if node.inBounds(pos[0], pos[1]):
                        node.kill()
                        valid = False
                        
                if valid:
                    all_nodes.add(Node(pos[0], pos[1], RADIUS, GREY))
        
        elif event.type == pygame.KEYDOWN: # If a keypress is detected...
            
            if event.key == pygame.K_SPACE: # ... and it was the spacebar
            
                for node in all_nodes:
                    # Cycle the colour of the nodes. BLUE -> GREEN -> GREY -> BLUE
                    if node.c == GREY:
                        node.setColour(BLUE)
                    elif node.c == BLUE:
                        node.setColour(GREEN)
                    elif node.c == GREEN:
                        node.setColour(GREY)


    #---------------------------------------------------------------------------
    # Runtime "loop"
    if runAlg:
        if i % 60 == 0: # Every 60 frames, automatically cycle node colour
            for node in all_nodes:
                if node.c == GREY:
                    node.setColour(BLUE)
                elif node.c == BLUE:
                    node.setColour(GREEN)
                elif node.c == GREEN:
                    node.setColour(GREY)
        

        i += 1 # Update frame counter


    #---------------------------------------------------------------------------
    # Draw screen

    screen.fill(WHITE) # Create blank screen

    all_edges.draw(screen) # Draw edges
    all_nodes.draw(screen) # Draw nodes on top of edges
    buttons.draw(screen) # Draw buttons
    
    # Render text on top of buttons
    text = pygame.font.SysFont('arial', 20)
    
    textSurf = text.render("Start", True, BLACK)
    textRect = textSurf.get_rect()
    textRect.center = ( 10 + WIDTH // 2, SCREENHEIGHT-HEIGHT-10 + HEIGHT // 2 )
    screen.blit(textSurf, textRect)

    textSurf = text.render("Stop", True, BLACK)
    textRect = textSurf.get_rect()
    textRect.center = ( 20+WIDTH + WIDTH // 2, SCREENHEIGHT-HEIGHT-10 + HEIGHT // 2 )
    screen.blit(textSurf, textRect)

    textSurf = text.render("Step", True, BLACK)
    textRect = textSurf.get_rect()
    textRect.center = ( 10*3+WIDTH*2 + WIDTH // 2, SCREENHEIGHT-HEIGHT-10 + HEIGHT // 2 )
    screen.blit(textSurf, textRect)

    pygame.display.update() # Updates entire window

    clock.tick(60) # Cap framerate to 60

pygame.quit()
