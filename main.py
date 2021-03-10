# Import Pygame, sqrt, and my classes
import pygame

from node import Node
from edge import Edge
from math import sqrt

# Defining colours
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GREY = (210, 210, 210)
WHITE = (255, 255, 255)

# Define and create window
SCREENWIDTH = 400
SCREENHEIGHT = 500

size = (SCREENWIDTH, SCREENHEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("COMP361")

# Groups to hold edges and nodes, separately
all_nodes = pygame.sprite.Group()
all_edges = pygame.sprite.Group()

# Loop flag and setting up pygame clock
carryOn = True
clock = pygame.time.Clock()

# Counter for when to change node colour
i = 1

while carryOn:
    
    for event in pygame.event.get(): # Check all user events
        
        if event.type == pygame.QUIT: # If user hit close, quit
            carryOn = False

        elif event.type == pygame.MOUSEBUTTONDOWN: # If user clicks mouse, store position
            
            pos = pygame.mouse.get_pos()

        elif event.type == pygame.MOUSEBUTTONUP: # If user lifts mouse button...

            new_pos = pygame.mouse.get_pos() # Get new position
            dx = new_pos[0] - pos[0]
            dy = new_pos[1] - pos[1]

            if sqrt(dx**2 + dy**2) >= 50: # If new position is more than 50 pixels away
                all_edges.add(Edge(pos[0], pos[1], new_pos[0], new_pos[1], BLACK)) # Add an edge
            else: # If not, create a new node
                pos = pygame.mouse.get_pos()
                all_nodes.add(Node(pos[0], pos[1], 50, GREY))
        
        elif event.type == pygame.KEYDOWN: # If a keypress is detected...
            
            if event.key == pygame.K_SPACE: # ... and it was the spacebar
            
                for node in all_nodes: # Cycle the colour of the nodes. BLUE -> GREEN -> GREY -> BLUE
                    if node.c == GREY:
                        node.setColour(BLUE)
                    elif node.c == BLUE:
                        node.setColour(GREEN)
                    elif node.c == GREEN:
                        node.setColour(GREY)
    
    if i % 60 == 0: # Every 60 frames, automatically cycle node colour
        for node in all_nodes:
            if node.c == GREY:
                node.setColour(BLUE)
            elif node.c == BLUE:
                node.setColour(GREEN)
            elif node.c == GREEN:
                node.setColour(GREY)
    

    i += 1 # Update frame counter

    screen.fill(WHITE) # Create blank screen

    all_edges.draw(screen) # Draw edges
    all_nodes.draw(screen) # Draw nodes on top of edges

    pygame.display.flip() # Updates entire window

    clock.tick(60) # Cap framerate to 60

pygame.quit()
