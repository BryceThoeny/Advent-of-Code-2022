class Tree:
    def __init__(self, height, visible = False):
        self.height = int(height)
        self.visible = visible

    def __str__(self):
        return f"A tree of heigh {height} with a scenic score of {scenic_score}"

    def score(self, tree_grid, tree_row, tree_column, height, width):

        #Comparing horizontally
        trees_r = 0
        for column in range((tree_column + 1), width):
            trees_r += 1
            if tree_grid[tree_row][column].height >= self.height:
                break
        trees_l = 1
        for column in range((tree_column - 1), 0, -1):
            if tree_grid[tree_row][column].height >= self.height:
                break
            trees_l += 1
    
        #Comparing vertically
        trees_d = 0
        for row in range((tree_row + 1), height):
            trees_d += 1
            if tree_grid[row][tree_column].height >= self.height:
                break
        trees_u = 1
        for row in range((tree_row - 1), 0, -1):
            if tree_grid[row][tree_column].height >= self.height:
                break
            trees_u += 1
    
        score = trees_r * trees_l * trees_u * trees_d
        return score


def part1():

    file = open("input.txt")

    lines = file.readlines()

    tree_grid = []

    for line in lines:
        tree_grid.append([])
        for character in line:
            if character != "\n":
                tree_grid[lines.index(line)].append(Tree(character))

    #Comparing horizontally
    for row in tree_grid:
        
        #First left to right
        tree_max = -1
        for tree in row:
            if tree.height > tree_max:
                tree.visible = True
                tree_max = tree.height
                
        #Then right to left
        tree_max = -1
        for tree in reversed(row):
            if tree.height > tree_max:
                tree.visible = True
                tree_max = tree.height

    height = len(tree_grid)
    width = len(tree_grid[0])

    #Comparing vertically
    for column in range(width):

        #First top to bottom
        tree_max = -1
        for row in range(height):
            if tree_grid[row][column].height > tree_max:
                tree_grid[row][column].visible = True
                tree_max = tree_grid[row][column].height

        #Then bottom to top
        tree_max = -1
        for row in range((height - 1), 0, -1):
            if tree_grid[row][column].height > tree_max:
                tree_grid[row][column].visible = True
                tree_max = tree_grid[row][column].height

    sum = 0

    for row in tree_grid:
        for tree in row:
            if tree.visible == True:
                sum += 1

    print(sum)

    file.close()

def part2():

    file = open("input.txt")

    lines = file.readlines()

    tree_grid = []

    for line in lines:
        tree_grid.append([])
        for character in line: #Could do this with a lambda?
            if character != "\n":
                tree_grid[lines.index(line)].append(Tree(character))

    #Comparing horizontally
    for row in tree_grid:
        
        #First left to right
        tree_max = -1
        for tree in row:
            if tree.height > tree_max:
                tree.visible = True
                tree_max = tree.height
                
        #Then right to left
        tree_max = -1
        for tree in reversed(row):
            if tree.height > tree_max:
                tree.visible = True
                tree_max = tree.height

    height = len(tree_grid)
    width = len(tree_grid[0])

    #Comparing vertically
    for column in range(width):

        #First top to bottom
        tree_max = -1
        for row in range(height):
            if tree_grid[row][column].height > tree_max:
                tree_grid[row][column].visible = True
                tree_max = tree_grid[row][column].height

        #Then bottom to top
        tree_max = -1
        for row in range((height - 1), 0, -1):
            if tree_grid[row][column].height > tree_max:
                tree_grid[row][column].visible = True
                tree_max = tree_grid[row][column].height

    max_score = 0

    for column in range(width):
        for row in range(height):
            score = tree_grid[row][column].score(tree_grid, row, column, height, width)
            if score > max_score:
                max_score = score

    print(max_score)

    file.close()


def main():

    part1()
    part2()


main()
