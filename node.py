class Node:
    def __init__(self, y, x, size):
        self.column = x
        self.row = y
        self.size = size
        self.state = None

        self.connections = {}


    def get_connections(self):
        connections_list = []
        for val in self.connections.values():
            if val != None:
                connections_list.append(val)
            
        return connections_list
    
    def set_state(self, state):
        if state == "WALL":
            self.state = state
        
        elif state == "START":
            self.state = state
        
        elif state == "END":
            self.state = state

        elif state == "SEARCH":
            self.state = state

        else:
            self.state = None
        
        return self.state

    def get_state(self):
        return self.state
    
    def calculate_distance(self, node):
        row = node.row
        column = node.column

        y_distance = row - self.row
        x_distance = column - self.column

        distance = (y_distance**2 + x_distance**2)**(1/2)

        return distance