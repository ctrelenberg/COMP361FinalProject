#!/usr/bin/env python3
import pygame
pygame.init()

from node import Node
from edge import Edge
from button import Button
from math import sqrt
import tools
from algorithm import *
from constants import *
from config import Config

tools.get_font('clippy', font_name='arial', font_size=13)

# Superfluous import -------------------
# Used for random colours
import random
random.seed()
#---------------------------------------

# Define and create window
pygame.display.set_caption("COMP361 Final Project")

# Add buttons
buttons = pygame.sprite.Group()
bottom_pos = lambda ordinal: ordinal * 10 + (ordinal - 1) * BUTTON_WIDTH
buttons.add(Button(bottom_pos(1), SCREENHEIGHT - BUTTON_HEIGHT - 10, BUTTON_WIDTH, BUTTON_HEIGHT, GREEN, "Start"))
buttons.add(Button(bottom_pos(2), SCREENHEIGHT - BUTTON_HEIGHT - 10, BUTTON_WIDTH, BUTTON_HEIGHT, RED, "Stop"))
buttons.add(Button(bottom_pos(3), SCREENHEIGHT - BUTTON_HEIGHT - 10, BUTTON_WIDTH , BUTTON_HEIGHT, YELLOW, "Step"))
buttons.add(Button(bottom_pos(4), SCREENHEIGHT - BUTTON_HEIGHT - 10, BUTTON_WIDTH , BUTTON_HEIGHT, GREY, "Clear"))
buttons.add(Button(bottom_pos(5), SCREENHEIGHT - BUTTON_HEIGHT - 10, BUTTON_WIDTH , BUTTON_HEIGHT, BLUE, "Reset"))
# A*, DFS, BFS, Greedy, D*, Theta*
left_pos = lambda ordinal: ordinal * 10 + (ordinal - 1) * BUTTON_HEIGHT
algorithm_ids = [(GREEN, "A*"), (RED, "DFS"), (BLUE, "BFS"), (CYAN, "Greedy"), (YELLOW, "Greedy*")]
[buttons.add(Button(10, left_pos(o+1), BUTTON_WIDTH, BUTTON_HEIGHT, c, n, tags=['algorithm'])) for o, (c, n) in enumerate(algorithm_ids)]

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

        # Save pygame
        self.pg = pygame

        # Save screen
        self.screen = pygame.display.set_mode(SCREEN_SIZE)

        # Clock
        self.clock = None

        # Algorithms
        self.algor = None
        self.algname = None
        self.alg_text = None

        self.config = Config()

    def clear(self):
        self.stepAlg = False
        self.runAlg = False
        self.endNode = None
        self.endNodeSet = False
        self.startNode = None
        self.startNodeSet = False
        self.all_nodes.empty()
        self.all_edges.empty()

    def run(self):
        # setting up pygame clock
        self.clock = pygame.time.Clock()
        while self.do_tick(self.clock):
            pass
        pygame.quit()

    def stop_running(self):
        self.runAlg = False
        self.stepAlg = False

    def generate_edge(self, x1, y1, x2, y2, n1, n2):
        #weight = tools.get_user_input(app=self, loc=n1.rect, restraints=['num'], default=1, prompt='Enter Weight:')
        new_edge = Edge(x1, y1, x2, y2, BLACK, n1, n2, 0, app=self)
        # Adds edge to lists of the connected nodes
        n1.addEdge(new_edge)
        n2.addEdge(new_edge)
        self.all_edges.add(new_edge) # Add an edge

    def reset_map(self):
        for n in self.all_nodes.sprites():
            if n not in [self.startNode, self.endNode]:
                n.c = GREY
            elif n == self.startNode:
                n.c = GREEN
            elif n == self.endNode:
                n.c = RED
            n.draw()
            self.stop_running()

    def set_algorithm(self, algname):
        if algname == self.algname:
            return
        self.reset_map()
        self.algname = algname
        if self.algname == "A*":
            self.algor = AStar(self.startNode, self.endNode)
            print('Set algorithm to A*.')
        elif self.algname == "DFS":
            self.algor = DepthFirstSearch(self.startNode, self.endNode)
            print('Set algorithm to DFS.')
        elif self.algname == "BFS":
            self.algor = BreadthFirstSearch(self.startNode, self.endNode)
            print('Set algorithm to BFS.')
        elif self.algname == "Greedy":
            self.algor = Greedy(self.startNode, self.endNode)
            print('Set algorithm to Greedy.')
        elif self.algname == "Greedy*":
            self.algor = GreedyHeuristic(self.startNode, self.endNode)
            print('Set algorithm to Greedy*.')
        for b in buttons:
            if b.tags is not None and 'algorithm' in b.tags:
                if b.name != self.algname:
                    b.set_deselected()
                else:
                    b.set_selected()

    def on_mouse_up(self, event):

        pos_up = pygame.mouse.get_pos() # Get new position

        dx = pos_up[0] - self.pos_down[0]
        dy = pos_up[1] - self.pos_down[1]

        buttonClicked = False

        for but in buttons:
            if but.inBounds(pos_up[0], pos_up[1]):
                if but.name == "Start":
                    if self.startNodeSet and self.endNodeSet:
                        print("Running with algorithm:", self.algor)
                        self.runAlg = True
                    else:
                        print('Start and/or end nodes are not defined.')
                elif but.name == "Stop":
                    self.stop_running()
                elif but.name == "Step":
                    if self.startNodeSet and self.endNodeSet:
                        self.stop_running()
                        self.stepAlg = True
                elif but.name == "Clear":
                    self.clear()
                elif but.name == "Reset":
                    self.reset_map()
                    self.set_algorithm(self.algname)
                else:
                    if self.startNodeSet and self.endNodeSet:
                        self.set_algorithm(but.name)
                    else:
                        print('Start and/or end nodes are not defined.')

                buttonClicked = True

        # This restricts modifying graph to when the loop is not running
        if self.runAlg or self.stepAlg and not buttonClicked:
            return

        if sqrt(dx**2 + dy**2) > Node.RADIUS and not buttonClicked: # If new pos is more than 50 pxls away

            # Flags for points that occur within nodes
            valid1 = False
            valid2 = False
            # Flag for duplicate edge
            isDup = False

            # Sorting the two points for ease of comparison
            sorted_pos = sorted([self.pos_down, pos_up])
            self.pos_down = sorted_pos[0]
            pos_up = sorted_pos[1]

            x1, y1, x2, y2 = None, None, None, None

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
                    edge.getNode1().removeEdge(edge)
                    edge.getNode2().removeEdge(edge)
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
                            node.set_label('Start')

                        # only set an end node after we have set a start node and make sure they aren't the same node
                        elif self.startNodeSet and not self.endNodeSet and (self.startNode != node):
                            self.endNodeSet = True
                            self.endNode = node
                            node.setColour(RED)
                            node.set_label('End')

                        # return a start node to a regular node
                        elif node == self.startNode and self.startNodeSet:
                            self.startNode = None
                            self.startNodeSet = False
                            node.setColour(GREY)
                            node.set_label()
                    # return an end to a regular node
                        elif node == self.endNode and self.endNodeSet:
                            self.endNodeSet = False
                            self.endNode = None
                            node.setColour(GREY)
                            node.set_label()


                        if self.startNodeSet and self.endNodeSet:
                            self.set_algorithm('A*')

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
                            self.set_algorithm(None)
                        elif node == self.endNode:
                            self.endNodeSet = False
                            self.endNode = None
                            self.set_algorithm(None)
                        # Delete node
                        node.kill()
                        del node
                        
                    valid = False

            if valid:
                self.all_nodes.add(Node(pos[0], pos[1], Node.RADIUS, GREY))
            

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
                    if self.startNodeSet and self.endNodeSet:
                        self.algor.stepAlgorithm()


        #---------------------------------------------------------------------------
        # Runtime "loop"
        if self.runAlg or self.stepAlg:
            if self.i % 60 == 0: # Every 60 frames, automatically cycle node colour
                
                if self.startNodeSet and self.endNodeSet:
                    self.algor.stepAlgorithm()


                if self.stepAlg:
                    self.stepAlg = False

            self.i += 1 # Update frame counter

        #---------------------------------------------------------------------------
        # Draw screen

        self.screen.fill(WHITE) # Create blank screen

        self.all_edges.draw(self.screen) # Draw edges
        if self.config.draw_edge_labels:
            for s in self.all_edges.sprites():
                s.draw_label()


        self.all_nodes.draw(self.screen) # Draw nodes on top of edges
        if self.config.draw_node_labels:
            for s in self.all_nodes.sprites():
                if s.has_label():
                    label_surf, label_rect = s.get_label()
                    self.screen.blit(label_surf, label_rect)

        buttons.draw(self.screen) # Draw buttons
        for s in buttons.sprites():
            button_surf, button_rect = s.get_text()
            self.screen.blit(button_surf, button_rect)

        if self.config.display_algorithm_indicator and self.algname is not None:
            if self.alg_text is None or self.alg_text[0] != self.algname:
                new_render = tools.get_font('clippy').render('Algorithm: ' + self.algname, True, BLACK)
                tsrect = new_render.get_rect()
                textx = SCREENWIDTH - 2 - tsrect.w
                texty = 10
                tsrect.center = (textx, texty)
                self.alg_text = (self.algname, new_render, tsrect)
            _name, surf, rct = self.alg_text
            self.screen.blit(surf, rct)

        pygame.display.update() # Updates entire window

        clock.tick(60) # Cap framerate to 60
        return True


if __name__ == "__main__":
    app = Application()
    app.run()
