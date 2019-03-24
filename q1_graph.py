# Team ID: G4T12
import utilities as util
import  itertools
from collections import defaultdict 
from collections import defaultdict

class Graph():
    def __init__(self):
        """
        self.edges is a dict of all possible next nodes
        e.g. {'X': ['A', 'B', 'C', 'E'], ...}
        self.weights has all the weights between two nodes,
        with the two nodes as a tuple as the key
        e.g. {('X', 'A'): 7, ('X', 'B'): 2, ...}
        """
        self.edges = defaultdict(list)
        self.weights = {}
    
    def add_edge(self, from_node, to_node, weight):
        # Note: assumes edges are bi-directional
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        self.weights[(from_node, to_node)] = weight
        self.weights[(to_node, from_node)] = weight

def dijsktra(graph, initial, end):
    # shortest paths is a dict of nodes
    # whose value is a tuple of (previous node, weight)
    shortest_paths = {initial: (None, 0)}
    current_node = initial
    visited = set()
    
    while current_node != end:
        visited.add(current_node)
        destinations = graph.edges[current_node]
        weight_to_current_node = shortest_paths[current_node][1]

        for next_node in destinations:
            weight = graph.weights[(current_node, next_node)] + weight_to_current_node
            if next_node not in shortest_paths:
                shortest_paths[next_node] = (current_node, weight)
            else:
                current_shortest_weight = shortest_paths[next_node][1]
                if current_shortest_weight > weight:
                    shortest_paths[next_node] = (current_node, weight)
        
        next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
        if not next_destinations:
            return "Route Not Possible"
        # next node is the destination with the lowest weight
        current_node = min(next_destinations, key=lambda k: next_destinations[k][1])
    
    # Work back through destinations in shortest path
    path = []
    while current_node is not None:
        path.append(current_node)
        next_node = shortest_paths[current_node][0]
        current_node = next_node
    # Reverse path
    path = path[::-1]
    return path

def store_in_dict(locations):
    dd = {}
    for loc in locations:
        lst = loc.split(",")
        if lst[0] not in dd :
            dd[lst[0]] = {lst[1]: lst[2]}
        else:
            start = lst[0]
            dest = lst[1]
            val = lst[2]
            dd[start][dest] = val
    return dd

def listElementToTuple(element):
    lst = element.split(",")
    return(lst[0],lst[1],int(lst[2]))


def schedule1(locations, start_location, number_of_trucks, orders):
    # TODO: replace the code in this function with your algorithm
    # orders: Order ID, Weight, Delivery location
    # This simple model solution does not make use of locations
    # However, to optimize your longest traveling time, you should use the information in locations.
    #OUTPUT: 
    # [[(1, 100, 'RUS'), (5, 200, 'CHN'), (9, 180, 'FRN')],
    # [(2, 150, 'CAN'), (6, 250, 'MEX'), (10, 230, 'SPN')],
    # [(3, 250, 'SIN'), (7, 350, 'AUS')],
    # [(4, 300, 'KOR'), (8, 270, 'GMY')]]

    #=========== INITIALISE GRAPH ==========
    graph = Graph()
    #contruct edges
    for element in locations:
        edge = listElementToTuple(element)
        graph.add_edge(*edge)
    print(dijsktra(graph, 'USA', 'BAR'))

    return []


