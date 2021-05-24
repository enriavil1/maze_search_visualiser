import pygame
from node import Node


class Maze:

    def __init__(self, screen, node_size):
        self.rows = screen.get_height()//node_size
        self.columns = screen.get_width()//node_size

        self.node_size = node_size
        self.starting_node = None
        self.ending_node = None
        self.screen = screen

        self.nodes = [[Node(i,j, self.node_size) for j in range(self.columns)] for i in range(self.rows)]
        self.node_graph = {}
        
        self.visited = []
        self.path = []
        self.default_connection()

        self.maze = []

    
    def default_connection(self):
        for node in self.node_iter():
            node.connections['UP'] = self.get_node(node.row-1, node.column)
            node.connections['DOWN'] = self.get_node(node.row+1, node.column)
            node.connections['RIGHT'] = self.get_node(node.row, node.column+1)
            node.connections['LEFT'] = self.get_node(node.row, node.column-1)

            self.node_graph[node] = set(node.get_connections())

    def node_iter(self):
        for i in range(self.columns):
            for j in range(self.rows):
                if self.nodes[i][j].get_state() != "WALL":
                    yield self.nodes[i][j]

    def draw_boundaries(self, width, height):
        topLeft = (0,0)
        topRight = (width-2, 0)
        bottomLeft = (0,height-2)
        bottomRight = (width-2,height-2)

        pygame.draw.line(self.screen,(255,255,255), topLeft, topRight, 3)
        pygame.draw.line(self.screen,(255,255,255), topRight, bottomRight, 3)
        pygame.draw.line(self.screen,(255,255,255), bottomRight, bottomLeft, 3)
        pygame.draw.line(self.screen,(255,255,255), bottomLeft, topLeft, 3)

    def draw_grid(self, width, height):
        for i in range(width):
            for j in range(height):

                rect =pygame.Rect(self.node_size*i, self.node_size*j, self.node_size, self.node_size) #square grid

                pygame.draw.rect(self.screen,(255,255,255), rect, 1)
        
    def draw_block(self, state, column, row):
        node = self.nodes[row][column]
        
        node.set_state(state)
        x = column * self.node_size
        y = row * self.node_size

        if node.get_state() == "WALL":
            
            self.node_switching(node)

            rect = pygame.Rect(x, y, self.node_size, self.node_size)
            pygame.draw.rect(self.screen, (0,0,255),rect, 0)
            pygame.draw.rect(self.screen,(255,255,255), rect, 1)
        
        if node.get_state() == "START":

            if self.starting_node is None:
                self.starting_node = node
            else:
                starting_node_row = self.starting_node.row
                starting_node_column = self.starting_node.column
                current_node_column = x//self.node_size
                current_node_row = y//self.node_size

                self.delete_block(starting_node_column, starting_node_row)
                self.delete_block(current_node_column, current_node_row)
                self.starting_node = node 

            rect = pygame.Rect(x, y, self.node_size, self.node_size)
            pygame.draw.rect(self.screen, (255,0,0),rect, 0)
            pygame.draw.rect(self.screen,(255,255,255), rect, 1)
        
        if node.get_state() == "END":

            if self.ending_node is None:
                self.ending_node = node
            
            else:
                ending_node_row = self.ending_node.row
                ending_node_column = self.ending_node.column
                current_node_column = x//self.node_size
                current_node_row = y//self.node_size

                self.delete_block(ending_node_column, ending_node_row)
                self.delete_block(current_node_column, current_node_row)
                self.ending_node = node

            rect = pygame.Rect(x, y, self.node_size, self.node_size)
            pygame.draw.rect(self.screen, (0,255,0),rect, 0)
            pygame.draw.rect(self.screen,(255,255,255), rect, 1)

        if node.get_state() == "SEARCH":
            rect = pygame.Rect(x, y, self.node_size, self.node_size)
            pygame.draw.rect(self.screen, (0,255,255),rect, 0)
            pygame.draw.rect(self.screen,(255,255,255), rect, 1)
        pygame.display.update()
            

    
        self.default_connection()
    
    def delete_block(self, column, row):

        node = self.nodes[row][column]

        self.node_switching(node)

        node.set_state("")

        x = column * self.node_size
        y = row * self.node_size

        rect = pygame.Rect(x, y, self.node_size, self.node_size)
        pygame.draw.rect(self.screen, (0,0,0),rect, 0)

        pygame.draw.rect(self.screen, (255,255,255),rect, 1)

        self.default_connection()
    
    def node_switching(self, node):

        if node is self.starting_node:
            self.starting_node = None

        if node is self.ending_node:
            self.ending_node = None
    
    def get_node(self, row, col):
        if row < self.rows and row >= 0 and col < self.columns and col >= 0 and self.nodes[row][col].get_state() != "WALL":
            return self.nodes[row][col]
        else:
            return None

    def print_node_connections(self):
        for node in self.node_iter():
            print((node.row, node.column),node.get_connections())
        

    def get_starting_node_location(self):
        if self.starting_node:
            return (self.starting_node.row, self.starting_node.column)
        else:
            return None
    
    def get_ending_node_location(self):
        if self.ending_node:
            return (self.ending_node.row, self.ending_node.column)
        else:
            return None
        
    def draw_path(self, path= None):

        if path == None:
            path = self.path

        for node in path:
            if node.get_state() == None or node.get_state() == "SEARCH":
                x = node.column * self.node_size
                y = node.row * self.node_size

                rect = pygame.Rect(x, y, self.node_size, self.node_size)
                pygame.draw.rect(self.screen, (255,0,255),rect, 0)
                pygame.draw.rect(self.screen,(255,255,255), rect, 1)
                pygame.display.update()
            
        self.draw_block("START", self.starting_node.column, self.starting_node.row)
        self.draw_block("END", self.ending_node.column, self.ending_node.row)


    def bfs(self):
        self.path = [self.starting_node]

        vertex_and_path = [self.starting_node, self.path]
        
        self.visited = set()

        bfs_queue = [vertex_and_path]

        while bfs_queue:
            current_vertex, self.path = bfs_queue.pop(0)

            self.visited.add(current_vertex)
            self.draw_block("SEARCH", current_vertex.column, current_vertex.row)

            for neighbors in self.node_graph[current_vertex]:
                if neighbors not in self.visited:
                    if neighbors is self.ending_node:
                        self.path += [neighbors]
                        return self.path
                    else:
                        bfs_queue.append([neighbors, self.path+[neighbors]])
                    

    def dfs(self, current):
            self.visited.append(current)
            self.distances = {}

            if current == self.ending_node:
                return self.visited
            
            for node in self.node_graph[current]:
                if node not in self.visited:
                    self.path = self.dfs(node)
                    if self.path:
                        return self.path

    def restart(self):

        self.screen.fill((0,0,0))
        self.draw_boundaries(self.screen.get_width(),self.screen.get_height())
        self.draw_grid(self.screen.get_width(), self.screen.get_height())

        self.visited = []
        self.path = []
        self.maze = []

        for node in self.node_iter():
            node.set_state("")

        if self.starting_node:
            self.draw_block("START", self.starting_node.column, self.starting_node.row)
        
        if self.ending_node:
            self.draw_block("END", self.ending_node.column, self.ending_node.row)
        

    def createMaze(self, file):
        opened = open(file, 'r')
        self.restart()
        for i in opened:
            self.maze.append([j.strip("\n") for j in i.split(",")])
        
        
        self.draw_maze()
        opened.close()
        
        
    def draw_maze(self):
        for row in range(len(self.maze)):
            for column in range(len(self.maze)):
                current = self.maze[row][column]
                if current == "#":
                    node = self.nodes[row][column]
                    self.draw_block("WALL", node.column, node.row)
                
    def save_maze(self):
        saving = [[None for j in range(self.columns)] for i in range(self.rows)]

        for row in range(len(self.nodes)):
            for column in range(len(self.nodes[row])):
                node = self.nodes[row][column]
                if node.get_state() == "WALL":
                    saving[node.row][node.column] = "#"
            
        
        file = open("maze.csv", "w")
        file.truncate(0)

        text = ""
        for i in range(len(saving)):
            for j in range(len(saving[i])):
                if j == len(saving[i]):
                    if saving[i][j] == None:
                        text += " "
                    
                    if saving[i][j] == "#":
                        text += "#"
                    
                else:
                    if saving[i][j] == None:
                        text += " ,"
                    
                    if saving[i][j] == "#":
                        text += "#,"
            file.write(text)
            file.write("\n")
            text = ""
        
        file.close()


    def get_path(self):
        path = []
        for node in self.path:
            path.append((node.row,node.column))
        
        return path
        
    def get_visited(self):
        visited = []

        for node in self.visited:
            visited.append((node.row,node.column))
        
        return visited
    
    def print_maze(self):
        for i in range(self.maze):
            print(self.maze[i])




    

            





        
    
    



    

