from random import shuffle
import timeit
import queue

class Node:

    def __init__(self, grid, parent, last_move, p1 ,p2):
        self.grid = grid

        if parent is None:
            self.depth = 0
            self.last_move = None
            self.parent = None
            self.p1 = p1
            self.p2 = p2
        else:
            self.depth = parent.depth + 1
            self.last_move = last_move
            self.parent = parent

    def getHeuristicEstimate(self, node):
        heuristic = 0

        for i in range(0, self.state.gridLength - 1):
            heuristic += abs(self.grid[i] - node.grid[i]) + abs(self.grids[i] - node.grid[i])
            if(parent.grid.dir_changed(self)):
                heuristic +=1
        
        if not self.parent is None:
            heuristic = heuristic + self.parent.getHeuristicEstimate(node)
            
        return heuristic

    def aStar(self):
        
        grid = []
        pq = queue.PriorityQueue()
        pq.put(0, self.startNode)
        
        visited = {self.startNode: True}

        while not pq.isEmpty():
            currentNode = pq.pop()

            #visit new node in tree
            currentNode.state.printGrid()
        
            if(currentNode.state.isEqual(self.finishState)):
                return(grid)
            
            #expand new node
            else:
                possibleMoves = currentNode.checkPossibleMoves()
                for nextNode in possibleMoves:
                    if not possibleMoves is None:

                        pq.put(nextNode.getHeuristicEstimate(Node(self.finishState, None, None)), nextNode)
                        visited[nextNode] = True

                        nextNode.state.printGrid()