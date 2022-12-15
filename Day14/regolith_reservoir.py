#Would be smarter to do this with two dimensions, but I didnt want to redo everything when I saw part 2 was more intensive.

class Cave:
    def __init__(self, floor, nodes = None, maximum = 0, sands = 0, fallpath = None):
        self.floor = floor
        if nodes is None:
            self.nodes = set()
        self.maximum = maximum
        self.sands = sands
        if fallpath is None:
            self.fallpath =  [(0, 500)]
        

    def __repr__(self):
        return f"The map for the problem. Filled points are {self.nodes}"


    def add_nodes(self, pair, material = "#"):
        start_col = int(pair[0][0].rstrip())
        start_row = int(pair[0][1].rstrip())
        end_col = int(pair[1][0].rstrip())
        end_row = int(pair[1][1].rstrip())
        
        if start_row != end_row:
            for row in range(min([start_row, end_row]), max([start_row, end_row])):
                if self.empty_space((row, start_col)):
                    self.nodes.add(Node((row, start_col), material))
        else:
            for col in range(min([start_col, end_col]), max([start_col, end_col]) + 1):
                if self.empty_space((start_row, col)):
                    self.nodes.add(Node((start_row, col), material))

        if max([start_row, end_row]) > self.maximum:
            self.maximum = max([start_row, end_row])


    def generate_sand(self):
        location = self.fallpath.pop()
        sand = Node(location, "+")
        self.nodes.add(sand)
        return sand


    def empty_space(self, location):
        if not any(node.location == location for node in self.nodes):
            return True


class Node:
    def __init__(self, location, material = None):
        self.location = location
        self.material = material


    def __repr__(self):
        return f"Node {self.location}[{self.material}]"


    def fall(self, cave):
        while True:
            row, column = self.location

            if not any(node.location == (row + 1, column) for node in cave.nodes):
                if cave.floor and row == (cave.maximum + 1):
                    cave.nodes.add(Node((row + 1, column), "#"))
                else:
                    cave.fallpath.append(self.location)
                    self.location = (row + 1, column)
                    if self.check_max(cave):
                        break 

            elif not any(node.location == (row + 1, column - 1) for node in cave.nodes):
                if cave.floor and row == (cave.maximum + 1):
                    cave.nodes.add(Node((row + 1, column - 1), "#"))
                else:
                    cave.fallpath.append(self.location)
                    self.location = (row + 1, column - 1)
                    if self.check_max(cave):
                        break

            elif not any(node.location == (row + 1, column + 1) for node in cave.nodes):
                if cave.floor and row == (cave.maximum + 1):
                    cave.nodes.add(Node((row + 1, column + 1), "#"))
                else:
                    cave.fallpath.append(self.location)
                    self.location = (row + 1, column + 1)
                    if self.check_max(cave):
                        break

            else:
                cave.sands += 1
                if self.location == (0, 500):
                    cave.maximum = -1
                break
                

    def check_max(self, cave):
        if self.location[0] == cave.maximum and not cave.floor:
            cave.maximum = -1
            return True
        return False


def part1():
    with open("test_input.txt") as file:
        cave = Cave(floor = False)
        lines = file.readlines()
        structures = []
        structure_pairs = []

        for line in lines:
            structure_verts = []
            [structure_verts.append((vertex.split(","))) for vertex in line.split(" -> ")]
            structures.append(structure_verts)

        for structure in structures:
            pairs= []
            [pairs.append(pair) for pair in zip(structure, structure[1:])]
            structure_pairs.append(pairs)

        [([cave.add_nodes(pair) for pair in pairs]) for pairs in structure_pairs]        

        while True:
            cave.generate_sand().fall(cave)
            if cave.maximum == -1:
                break  

        print(cave.sands)


def part2():
    with open("test_input.txt") as file:       
            cave = Cave(floor = True)
            lines = file.readlines()
            structures = []
            structure_pairs = []

            for line in lines:
                structure_verts = []
                [structure_verts.append((vertex.split(","))) for vertex in line.split(" -> ")]
                structures.append(structure_verts)

            for structure in structures:
                pairs= []
                [pairs.append(pair) for pair in zip(structure, structure[1:])]
                structure_pairs.append(pairs)

            [([cave.add_nodes(pair) for pair in pairs]) for pairs in structure_pairs] 

            while True:
                cave.generate_sand().fall(cave)
                if cave.maximum == -1:
                    break  

            print(cave.sands)


def main():
    part1()
    part2()


main()
