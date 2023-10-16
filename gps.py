"""Create shortest routes between cities on a map.
"""

import sys
import argparse

class City:
    """ This class holds data representing a City.
    
    Attributes:
        name: the input string that contains the name of the city.
        neighbors (dict): Starts off as an empty string that we will populate with the add_neighbor() method later. The keys of this dictionary will be other City objects that are connected to this instance of City. The values of those keys are tuples where the first item is the distance between the cities(int), and the interstate(str) that connects them.
    """
    def __init__(self, name):
        self.name = name
        self.neighbors = {}
        
    def __repr__(self):
        return self.name
        
    def add_neighbor(self, neighbor,distance, interstate):
        """
        Parameters:
            self
            neighbor(City) - The City object that will be connected to this instance (and vice versa).
            distance(str) - The distance between the two cities.
            interstate(str) - The interstate number that connects the two cities
        """
        if neighbor not in self.neighbors:
            self.neighbors[neighbor] = (distance, interstate)
        if self not in neighbor.neighbors:
            neighbor.neighbors[self] = (distance, interstate)
                      
class Map:
    """This class stores the map data as a form of Graph where each node in the Graph is a city, and the edges are represented by the relationships that the cities have to each other.
    
    Attributes:
        cities: a list of all of the unique city objects that make up the Graph structure
    """
    def __init__(self, relationships):
        self.cities = []
        for city_name in relationships:
            if city_name not in {x.name for x in self.cities}:
                main_city = City(city_name)
                self.cities.append(main_city)
            
            main_city_index = [x.name for x in self.cities].index(city_name)
            
            for connection,distance, interstate in relationships[city_name]:
                if connection not in {x.name for x in self.cities}:
                    neighboring_city = City(connection)
                    self.cities.append(neighboring_city)
                
                connecting_city_index = [x.name for x in self.cities].index(connection)
                self.cities[main_city_index].add_neighbor(self.cities[connecting_city_index], distance, interstate)
              
    def __repr__(self):
        return str(self.cities)
    
def bfs(graph, start, goal):
    """An implementation for an undirected, unweighted graph
    
    Parameters:
        Graph(Map) - A map object representing the graph that we will be traversing.
        Start(str) - The start city in a roadtrip for example.
        Goal(str) - The destination city in a roadtrip for example.
    Returns:
        A list of strings (cities) that we will visit on the shortest path between the start and goal cities
    """
    explored = []
    queue = [[start]]
    while queue:
        path = queue.pop(0)
        lastNode = path[-1]
        if lastNode not in explored:
            city_names = [x.name for x in graph.cities]
            neighbours = graph.cities[city_names.index(str(lastNode))].neighbors
            for neighbour in neighbours:
                new_path = list(path)
                new_path.append(neighbour)
                queue.append(new_path)
                if str(neighbour) == goal:
                    return [str(x) for x in new_path]    
            explored.append(lastNode)
 
    print("No path has been found")
    return None

def main(start, destination, graph):
    """This function will create a Map object with the connections data being passed in. It will then use bfs() to find the path between a start City and a destination City. It will parse the returned value and instruct the user on where they should drive given a start node and an end node.
    
    Parameters:
        start(str) - The start city in a roadtrip for example.
        destination(str) - The destination city in a roadtrip for example.
        Graph(dict) - A dictionary representing an adjecency list of cities and the cities to which they connect.
    Returns:
        A string that contains all of the same contents that we have printed out to the console/terminal.
    """
    map = Map(graph)
    instructions = bfs(map, start, destination)
    
    try:
        content = ""
        for i, city in enumerate(instructions):
            if i == 0:
                print(f"Starting at {city}")
                content += f"Starting at {city}"
                
            if i < len(instructions) - 1:
                next_city = str(instructions[i+1])
                
                currCity = [x for x in map.cities if x.name == city][0]
                currCity_neighbor = {str(key): value for key,value in currCity.neighbors.items()}
                distance_to_drive, interstate = currCity_neighbor[next_city]
                
                print(f"Drive {distance_to_drive} miles on {interstate} towards {next_city}, then")
                content += f"Drive {distance_to_drive} miles on {interstate} towards {next_city}, then"

            if i == len(instructions) - 1:
                print("You will arrive at your destination")
                content += "You will arrive at your destination" 
        return content
    except:
        exit()
        
def parse_args(args_list):
    """Takes a list of strings from the command prompt and passes them through as arguments
    
    Args:
        args_list (list) : the list of strings from the command prompt
    Returns:
        args (ArgumentParser)
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--starting_city', type = str, help = 'The starting city in a route.')
    parser.add_argument('--destination_city', type = str, help = 'The destination city in a route.')
    args = parser.parse_args(args_list)
    return args

if __name__ == "__main__":  
    connections = {  
        "Baltimore": [("Washington", 39, "95"), ("Philadelphia", 106, "95")],
        "Washington": [("Baltimore", 39, "95"), ("Fredericksburg", 53, "95"), ("Bedford", 137, "70")], 
        "Fredericksburg": [("Washington", 53, "95"), ("Richmond", 60, "95")],
        "Richmond": [("Charlottesville", 71, "64"), ("Williamsburg", 51, "64"), ("Durham", 151, "85")],
        "Durham": [("Richmond", 151, "85"), ("Raleigh", 29, "40"), ("Greensboro", 54, "40")],
        "Raleigh": [("Durham", 29, "40"), ("Wilmington", 129, "40"), ("Richmond", 171, "95")],
        "Greensboro": [("Charlotte", 92, "85"), ("Durham", 54, "40"), ("Ashville", 173, "40")],
        "Ashville": [("Greensboro", 173, "40"), ("Charlotte", 130, "40"), ("Knoxville", 116, "40"), ("Atlanta", 208, "85")],
        "Charlotte": [("Atlanta", 245, "85"), ("Ashville", 130, "40"), ("Greensboro", 92, "85")],
        "Jacksonville": [("Atlanta", 346, "75"), ("Tallahassee", 164, "10"), ("Daytona Beach", 86, "95")],
        "Daytona Beach": [("Orlando", 56, "4"), ("Miami", 95, "268")],
        "Orlando": [("Tampa", 94, "4"), ("Daytona Beach", 56, "4")],
        "Tampa": [("Miami", 281, "75"), ("Orlando", 94, "4"), ("Atlanta", 456, "75"), ("Tallahassee", 243, "98")],
        "Atlanta": [("Charlotte", 245, "85"), ("Ashville", 208, "85"), ("Chattanooga", 118, "75"), ("Macon", 83, "75"), ("Tampa", 456, "75"), ("Jacksonville", 346, "75"), ("Tallahassee", 273, "27") ],
        "Chattanooga": [("Atlanta", 118, "75"), ("Knoxville", 112, "75"), ("Nashville", 134, "24"), ("Birmingham", 148, "59")],
        "Knoxville": [("Chattanooga", 112,"75"), ("Lexington", 172, "75"), ("Nashville", 180, "40"), ("Ashville", 116, "40")],
        "Nashville": [("Knoxville", 180, "40"), ("Chattanooga", 134, "24"), ("Birmingam", 191, "65"), ("Memphis", 212, "40"), ("Louisville", 176, "65")],
        "Louisville": [("Nashville", 176, "65"), ("Cincinnati", 100, "71"), ("Indianapolis", 114, "65"), ("St. Louis", 260, "64"), ("Lexington", 78, "64") ],
        "Cincinnati": [("Louisville", 100, "71"), ("Indianapolis,", 112, "74"), ("Columbus", 107, "71"), ("Lexington", 83, "75"), ("Detroit", 263, "75")],
        "Columbus": [("Cincinnati", 107, "71"), ("Indianapolis", 176, "70"), ("Cleveland", 143, "71"), ("Pittsburgh", 185, "70")],
        "Detroit": [("Cincinnati", 263, "75"), ("Chicago", 283, "94"), ("Mississauga", 218, "401")],
        "Cleveland":[("Chicago", 344, "80"), ("Columbus", 143, "71"), ("Youngstown", 75, "80"), ("Buffalo", 194, "90")],
        "Youngstown":[("Pittsburgh", 67, "76")],
        "Indianapolis": [("Columbus", 175, "70"), ("Cincinnati", 112, "74"), ("St. Louis", 242, "70"), ("Chicago", 183, "65"), ("Louisville", 114, "65"), ("Mississauga", 498, "401")],
        "Pittsburg": [("Columbus", 185, "70"), ("Youngstown", 67, "76"), ("Philadelphia", 304, "76"), ("New York", 391, "76"), ("Bedford", 107, "76")],
        "Bedford": [("Pittsburg", 107, "76")], #COMEBACK
        "Chicago": [("Indianapolis", 182, "65"), ("St. Louis", 297, "55"), ("Milwaukee", 92, "94"), ("Detroit", 282, "94"), ("Cleveland", 344, "90")],
        "New York": [("Philadelphia", 95, "95"), ("Albany", 156, "87"), ("Scranton", 121, "80"), ("Providence,", 95, "181"), ("Pittsburgh", 389, "76")],
        "Scranton": [("Syracuse", 130, "81")],
        "Philadelphia": [("Washington", 139, "95"), ("Pittsburgh", 305, "76"), ("Baltimore", 101, "95"), ("New York", 95, "95")]
    }
    args = parse_args(sys.argv[1:])
    main(args.starting_city, args.destination_city, connections)
