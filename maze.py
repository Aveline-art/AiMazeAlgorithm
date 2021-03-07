from node import Node
from queue import Queue
from stack import Stack

class Maze():

    def __init__(self, filename):

        # Important variables to keep track of; also here for ease lookup.
        self.start = None
        self.end = None
        self.paths = []
        self.walls = []
        self.height = None
        self.width = None
        self.solution = []
        self.explored = []

        # Opens maze in the form of a .txt file.
        with open(filename) as f:
            lines = f.read()
        
        # Validate lines.
        if lines.count('A') != 1:
            raise Exception('There can only be one start.')
        if lines.count('B') != 1:
            raise Exception('There can only be one end.')


        lines = lines.splitlines()
        self.height = len(lines)
        self.width = max([len(line) for line in lines])

        for row, line in enumerate(lines):
            for col, char in enumerate(line):
                if char == '#':
                    self.walls.append((row, col))
                elif char == 'B':
                    self.end = (row, col)
                elif char == 'A':
                    self.start = (row, col)
                elif char == ' ':
                    self.paths.append((row, col))
                else:
                    continue
        f.close()
    
    def __solve(self, frontier):
        if frontier.empty():
            return None
        node = frontier.retrieve()
        value = node.value
        if value == self.end:
            return node
        
        self.explored.append(value)
        
        next_cells = self.neighbors(value)
        if not next_cells:
            return None
        
        next_cells = [cell for cell in next_cells if cell not in self.explored]
        for cell in next_cells:
            child_node = Node(cell, node)
            frontier.add(child_node)

        solved_node = self.__solve(frontier)
        if solved_node:
            return solved_node
        return None
    
    def breath_first_search(self):
        self.explored = []
        frontier = Queue()
        frontier.add(Node(self.start))

        solved_node = self.__solve(frontier)
        solution = [solved_node.value]

        while solved_node.parent != None:
            solution.append(solved_node.parent.value)
            solved_node = solved_node.parent

        self.solution = solution

    def depth_first_search(self):
        self.explored = []
        frontier = Stack()
        frontier.add(Node(self.start))
        
        solved_node = self.__solve(frontier)
        solution = [solved_node.value]

        while solved_node.parent != None:
            solution.append(solved_node.parent.value)
            solved_node = solved_node.parent

        self.solution = solution

    def neighbors(self, cell):
        row = cell[0]
        col = cell[1]

        possible_neighbors = [
            # up
            (row + 1, col),
            # right
            (row, col + 1),
            # down
            (row - 1, col),
            # left
            (row, col -1)
        ]

        true_neighbors = [neighbor for neighbor in possible_neighbors if neighbor in self.paths or neighbor == self.end]
        return true_neighbors

    
    def print(self):
        for row in range(self.height):
            for col in range(self.width):
                if (row, col) == self.start:
                    print('A', end='')
                elif (row, col) == self.end:
                    print('B', end='')
                elif (row, col) in self.walls:
                    print('#', end='')
                elif self.solution and (row, col) in self.solution:
                    print('*', end='')
                else:
                    print(' ', end='')
            print('')
        if not self.solution:
            print('No solution.')
        print('Steps taken: ', len(self.explored))
            


maze = Maze('maze3.txt')
maze.depth_first_search()
maze.print()
maze.breath_first_search()
maze.print()
