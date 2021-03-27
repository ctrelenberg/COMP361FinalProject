import pygame
from queue import PriorityQueue
from math import sqrt

from itertools import count

unique = count()

class AStar:
    def __init__(self, startNode, endNode):
        self.startNode = startNode
        self.endNode = endNode
        self.currentNode = None
        self.visitedNodes = []
        self.priorityQueue = PriorityQueue()

        self.complete = False

        self.priorityQueue.put((0,next(unique),startNode))

    def stepAlgorithm(self):
        # don't do anything if there is nothing in the priority queue or the algorithm is complete
        if self.complete or self.priorityQueue.empty():
            return
        
        self.currentNode = self.priorityQueue.get()[2]

        self.visitedNodes.append(self.currentNode)
        for node in self.visitedNodes:
            if node == self.startNode:
                node.setColour((0,0,255))
            node.setColour((210,210,210))

        
        self.currentNode.setColour((255,140,0))

        if self.currentNode == self.endNode:
            self.complete = True
            while self.currentNode != None:
                self.currentNode.setColour((0,255,100))
                self.currentNode = self.currentNode.parent
            return

        neighbors = self.currentNode.getNeighbors()

        for neighbor in neighbors:

            if neighbor in self.visitedNodes:
                continue

            neighbor.parent = self.currentNode
            neighbor.costToReach = self.currentNode.costToReach + self.distanceBetweenNodes(neighbor, self.currentNode)
            self.priorityQueue.put((self.huristicFunction(neighbor,self.endNode) + neighbor.costToReach, next(unique), neighbor))
            neighbor.setColour((0,0,255))

    

    def distanceBetweenNodes(self, node1, node2):
        x = node1.x - node2.x
        y = node1.y - node2.y
        return sqrt(x**2 + y**2)


    def huristicFunction(self, node1, node2):
        return self.distanceBetweenNodes(node1, node2)