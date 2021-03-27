import pygame
from queue import PriorityQueue
from math import sqrt

from itertools import count

unique = count()

# implementation of A* algorithm
class AStar:
    def __init__(self, startNode, endNode):
        self.startNode = startNode              # start node
        self.endNode = endNode                  # end node
        self.currentNode = None                 # the currently used node
        self.visitedNodes = []                  # list of visited nodes
        self.priorityQueue = PriorityQueue()    # priority queue to make for less sorting

        self.complete = False   # boolean if the algorithm has completed or not


        # put the start node into the priority queue
        self.priorityQueue.put((0,next(unique),startNode))

    # this function performs one step of A* until completeion
    def stepAlgorithm(self):
        # don't do anything if there is nothing in the priority queue or the algorithm is complete
        if self.complete or self.priorityQueue.empty():
            return
        # get the next best node from the priority queue
        self.currentNode = self.priorityQueue.get()[2]

        # add the current node to the list of visited nodes
        self.visitedNodes.append(self.currentNode)
        # change the colour of visited nodes to grey
        for node in self.visitedNodes:
            node.setColour((210,210,210))

        # set the colour of the curren node to orange
        self.currentNode.setColour((255,140,0))

        # check if we have found the goal node
        if self.currentNode == self.endNode:

            # set complete to true
            self.complete = True
            # change the path of nodes to green
            while self.currentNode != None:
                self.currentNode.setColour((0,255,100))
                self.currentNode = self.currentNode.parent
            return

        # find the neighbors of the current node
        neighbors = self.currentNode.getNeighbors()

        # add each neighbor to the priority queue if we haven't visited it yet
        for neighbor in neighbors:
            # skip a node if we have visited it
            if neighbor in self.visitedNodes:
                continue
            # make the parent of the neighboring node the current node
            neighbor.parent = self.currentNode
            # update the cost to reach of the neighboring node
            neighbor.costToReach = self.currentNode.costToReach + self.distanceBetweenNodes(neighbor, self.currentNode)
            # put the neighboring node in the priority queue
            self.priorityQueue.put((self.huristicFunction(neighbor,self.endNode) + neighbor.costToReach, next(unique), neighbor))
            # set the colour of a visited node to blue
            neighbor.setColour((0,0,255))

    
    # find the distance between nodes using euclidean distance
    def distanceBetweenNodes(self, node1, node2):
        x = node1.x - node2.x
        y = node1.y - node2.y
        return sqrt(x**2 + y**2)

    # find the huristics between nodes using euclidean distance
    def huristicFunction(self, node1, node2):
        return self.distanceBetweenNodes(node1, node2)