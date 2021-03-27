# Import Pygame, sqrt, and my classes
import pygame

from node import Node
from edge import Edge
from button import Button
from math import sqrt
import tools

# Superfluous import -------------------
# Used for random colours
import random
random.seed()
#---------------------------------------


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

pygame.init()

# Define and create window
infoObject = pygame.display.Info()
SCREENWIDTH = infoObject.current_w // 2
SCREENHEIGHT = infoObject.current_h // 2

size = (SCREENWIDTH, SCREENHEIGHT)
pygame.display.set_caption("COMP361 Final Project")

# Add buttons
WIDTH = 80
HEIGHT = 30
buttons = pygame.sprite.Group()
buttons.add(Button(10, SCREENHEIGHT-HEIGHT-10, WIDTH, HEIGHT, GREEN, "START"))
buttons.add(Button(20+WIDTH, SCREENHEIGHT-HEIGHT-10, WIDTH, HEIGHT, RED, "STOP"))
buttons.add(Button(10*3+WIDTH*2, SCREENHEIGHT-HEIGHT-10, WIDTH
                   , HEIGHT, YELLOW, "STEP"))

class Application:
    def __init__(self):
        # Groups to hold edges and nodes, separately
        self.all_nodes = pygame.sprite.Group()
        self.all_edges = pygame.sprite.Group()
        # Counter for when to change node colour
        self.i = 1
        # Loop flag  
        self.stepAlg = False
        self.runAlg = False

        # end node and if the end node is set of end node
        self.endNodeSet = False
        self.endNode = None

        # start node and current state of start node
        self.startNode = None
        self.startNodeSet = False

        # Render text on top of buttons
        self.text = pygame.font.SysFont('arial', 20)

        # Save pygame
        self.pg = pygame

        # Save screen
        self.screen = pygame.display.set_mode(size)

        # Clock
        self.clock = None

    def run(self):
        # setting up pygame clock
        self.clock = pygame.time.Clock()
        while self.do_tick(self.clock):
            pass
        pygame.quit()


    def generate_edge(self, x1, y1, x2, y2, n1, n2):
        weight = tools.get_user_input(app=self, loc=n1.rect, restraints=['num'], default=1, prompt='Enter Weight:')
        new_edge = Edge(x1, y1, x2, y2, BLACK, n1, n2, weight, app=self)
        # Adds edge to lists of the connected nodes
        n1.addEdge(new_edge)
        n2.addEdge(new_edge)
        self.all_edges.add(new_edge) # Add an edge


    def on_mouse_up(self, event):
        
        pos_up = pygame.mouse.get_pos() # Get new position
        
        dx = pos_up[0] - self.pos_down[0]
        dy = pos_up[1] - self.pos_down[1]

        buttonClicked = False

        for but in buttons:
            if but.inBounds(pos_up[0], pos_up[1]):
                if but.name == "START":
                    self.runAlg = True
                    self.setAlg = False
                elif but.name == "STOP":
                    self.runAlg = False
                    self.stepAlg = False
                elif but.name == "STEP":
                    self.runAlg = False
                    self.stepAlg = True
                buttonClicked = True

        # This restricts modifying graph to when the loop is not running
        if self.runAlg or self.stepAlg and not buttonClicked:
            return

        if sqrt(dx**2 + dy**2) > RADIUS and not buttonClicked: # If new pos is more than 50 pxls away

            # Flags for points that occur within nodes
            valid1 = False
            valid2 = False
            # Flag for duplicate edge
            isDup = False

            # Sorting the two points for ease of comparison
            sorted_pos = sorted([self.pos_down, pos_up])
            self.pos_down = sorted_pos[0]
            pos_up = sorted_pos[1]

            # Check that the endpoints occur within nodes
            for node in self.all_nodes:
                # Fix the endpoints to the centers of nodes if valid
                if node.inBounds(self.pos_down[0], self.pos_down[1]):
                    valid1 = True
                    x1 = node.getX()
                    y1 = node.getY()
                    n1 = node
                    
                if node.inBounds(pos_up[0], pos_up[1]):
                    valid2 = True
                    x2 = node.getX()
                    y2 = node.getY()
                    n2 = node

            # Check to see if edge is a duplicate, delete edge if it is
            for edge in self.all_edges:
                point1, point2 = edge.getEndpoints()
                if point1 == (x1, y1) and point2 == (x2, y2):
                    isDup = True
                    # Removes edge from the lists of it's connected nodes
                    edge.getNode1.removeEdge(edge)
                    edge.getNode2.removeEdge(edge)
                    edge.kill()
                    del edge
                

            if valid1 and valid2 and (not isDup):
                self.generate_edge(x1, y1, x2, y2, n1, n2)
                
            x1, y1, n1, x2, y2, n2 = None, None, None, None, None, None
            
        elif not buttonClicked: # If not, create/delete node

            valid = True
            
            pos = pygame.mouse.get_pos()

            for node in self.all_nodes:
                if node.inBounds(pos[0], pos[1]):
                    
                    if event.button == 3: # Right-click
                                                # sets start and end nodes

                        # if we don't have a start node set, set the node we clicked on to green and make it the start node
                        if not self.startNodeSet:
                            self.startNode = node
                            self.startNodeSet = True
                            node.setColour(GREEN)

                        # only set an end node after we have set a start node and make sure they aren't the same node
                        elif self.startNodeSet and not self.endNodeSet and (self.startNode != node):
                            self.endNodeSet = True
                            self.endNode = node
                            node.setColour(RED)
                        # return a start node to a regular node
                        elif node == self.startNode and self.startNodeSet:
                            self.startNode = None
                            self.startNodeSet = False
                            node.setColour(GREY)
                        # return an end to a regular node
                        elif node == self.endNode and self.endNodeSet:
                            self.endNodeSet = False
                            self.endNode = None
                            node.setColour(GREY)
                        
                    else:
                        # Delete edges attached to node
                        for edge in self.all_edges:
                            if edge.n1 == node or edge.n2 == node:
                                edge.kill()
                                del edge

                        # check if we are deleting a start or end node and update
                        if node == self.startNode:
                            self.startNodeSet = False
                            self.startNode = None
                        elif node == self.endState:
                            self.endNodeSet = False
                            self.endNode = None
                        # Delete node
                        node.kill()
                        del node
                        
                    valid = False

            if valid:
                self.all_nodes.add(Node(pos[0], pos[1], RADIUS, GREY))
            

    def do_tick(self, clock):
        #---------------------------------------------------------------------------
        # User input handling
        
        for event in pygame.event.get(): # Check all user events
            
            if event.type == pygame.QUIT: # If user hit close, quit
                return False

            elif event.type == pygame.MOUSEBUTTONDOWN: # If mouse down, store pos
                self.pos_down = pygame.mouse.get_pos()

            elif event.type == pygame.MOUSEBUTTONUP: # If user lifts mouse button...
                self.on_mouse_up(event)

            elif event.type == pygame.KEYDOWN: # If a keypress is detected...
                if event.key == pygame.K_SPACE: # ... and it was the spacebar
                    for node in self.all_nodes:
                        # Cycle the colour of the nodes. BLUE -> GREEN -> GREY -> BLUE
                        if node.c == GREY:
                            node.setColour(BLUE)
                        elif node.c == BLUE:
                            node.setColour(YELLOW)
                        elif node.c == YELLOW:
                            node.setColour(GREY)


        #---------------------------------------------------------------------------
        # Runtime "loop"
        if self.runAlg or self.stepAlg:
            if self.i % 60 == 0: # Every 60 frames, automatically cycle node colour
                for node in self.all_nodes:
                    if node.c == GREY:
                        node.setColour(BLUE)
                    elif node.c == BLUE:
                        node.setColour(YELLOW)
                    elif node.c == YELLOW:
                        node.setColour(GREY)

                if self.stepAlg:
                    self.stepAlg = False

            self.i += 1 # Update frame counter

        #---------------------------------------------------------------------------
        # Draw screen

        self.screen.fill(WHITE) # Create blank screen

        self.all_edges.draw(self.screen) # Draw edges
        self.all_nodes.draw(self.screen) # Draw nodes on top of edges
        buttons.draw(self.screen) # Draw buttons
        
        
        textSurf = self.text.render("Start", True, BLACK)
        textRect = textSurf.get_rect()
        textRect.center = ( 10 + WIDTH // 2, SCREENHEIGHT-HEIGHT-10 + HEIGHT // 2 )
        self.screen.blit(textSurf, textRect)

        textSurf = self.text.render("Stop", True, BLACK)
        textRect = textSurf.get_rect()
        textRect.center = ( 20+WIDTH + WIDTH // 2, SCREENHEIGHT-HEIGHT-10 + HEIGHT // 2 )
        self.screen.blit(textSurf, textRect)

        textSurf = self.text.render("Step", True, BLACK)
        textRect = textSurf.get_rect()
        textRect.center = ( 10*3+WIDTH*2 + WIDTH // 2, SCREENHEIGHT-HEIGHT-10 + HEIGHT // 2 )
        self.screen.blit(textSurf, textRect)

        pygame.display.update() # Updates entire window

        clock.tick(60) # Cap framerate to 60
        return True


if __name__ == "__main__":
    app = Application()
    app.run()
