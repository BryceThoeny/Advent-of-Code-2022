import timeit

class Node:

    def __init__(self, location, height, distance):
        self.location = location
        self.height = height
        self.distance = distance


    def __repr__(self):
        return f"Node {self.location}"


    def neighbors(self, explored, lines, frontier):

        neighbor_locs = []

        if self.location[0] > 0:
            neighbor_locs.append(((self.location[0] - 1), self.location[1]))
        if self.location[0] < 40:
            neighbor_locs.append(((self.location[0] + 1), self.location[1]))
        if self.location[1] > 0:
            neighbor_locs.append((self.location[0], (self.location[1] - 1)))
        if self.location[1] < 65:
            neighbor_locs.append((self.location[0], (self.location[1] + 1)))
        #This gives a list of all neighbors that are on the map

        #Then need to check that these arent in explored, and remove them if they are  
        for neighbor in neighbor_locs.copy():
            if neighbor in explored or neighbor in frontier.frontier_locs:
                neighbor_locs.remove(neighbor)

        #Then need to compare their height values to the current node, 
        #and reject them if their height is more than 1 greater
        for neighbor in neighbor_locs.copy():
            if lines[neighbor[0]][neighbor[1]] == "E":
                neighbor_height = 26
            else:
                neighbor_height = ord(lines[neighbor[0]][neighbor[1]]) - 96
            if neighbor_height - 1 > self.height:
                neighbor_locs.remove(neighbor)
    
        return neighbor_locs


class NodeFrontier:

    def __init__(self, frontier_list, frontier_locs):
        self.frontier_list = frontier_list
        self.frontier_locs = frontier_locs
    
    def add_node(self, node):
        self.frontier_list.append(node)
        self.frontier_locs.append(node.location)

    def remove_node(self):
        self.frontier_locs.pop(0)
        return self.frontier_list.pop(0)


def find_path(locations, end_row, end_column, lines):

    explored = []
    start_nodes = []
    
    [start_nodes.append(Node((location[0], location[1]), 1, 0)) for location in locations]

    frontier = NodeFrontier(start_nodes, locations)

    while True:
        try:
            node = frontier.remove_node()
        except:
            return 10000000

        if node.location == ((end_row, end_column)):
            return node.distance
        else:
            #Add valid neighbor nodes to frontier
            neighbor_locs = node.neighbors(explored, lines, frontier)

            [frontier.add_node(Node(neighbor, 26, (node.distance + 1))) if lines[neighbor[0]][neighbor[1]] == "E" else
             frontier.add_node(Node(neighbor, (ord(lines[neighbor[0]][neighbor[1]]) - 96), (node.distance + 1)))
             for neighbor in neighbor_locs]

            explored.append(node.location)


def part1(lines):

    begin = timeit.default_timer()

    locations = []

    for row, line in enumerate(lines):
        for column, character in enumerate(line):
            if character == "E":
                end_row, end_column = row, column
            if character == "S":
                locations.append((row, column))

    print(find_path(locations, end_row, end_column, lines))

    end = timeit.default_timer()

    print(f"Execution time: {end - begin}")
        

def part2(lines):

    begin = timeit.default_timer()

    starts = []

    for row, line in enumerate(lines):
        for column, character in enumerate(line):
            if character == "E":
                end_row, end_column = row, column
            if character == "a":
                starts.append((row, column))

    print(find_path(starts, end_row, end_column, lines))

    end = timeit.default_timer()

    print(f"Execution time: {end - begin}")   
        

def main():

    with open("input.txt") as file:

        lines = file.readlines()

        part1(lines)
        part2(lines)


main()
