import re

def part1():
    file = open("input.txt")

    crate_raws = []

    line = file.readline()

    while line.rstrip():
        crate_raws.append(line)
        line = file.readline().rstrip()

    crate_raws.pop()

    stacks = [[] for _ in range(9)]

    for crate_raw in crate_raws:
        matches = re.findall(r"(\[(?:[\w])\]\s|\s{4})|(\[(?:[\w])\]|\s{3})", crate_raw)
        for column in range(9):
            if matches[column][0]:
                stacks[column].insert(0, matches[column][0].rstrip())
            else:
                stacks[column].insert(0, matches[column][1].rstrip())
    
    instructions = file.readlines()

    #cleans up the blanks
    for stack in stacks:
        count = stack.count("")
        for _ in range(count):
            stack.pop()

    #Just to show that this can all get compressed into one big ugly nested list comprehension/anonymous function pile
    instruction_list = [[(lambda components: int(components.group(1)))(components),
                         (lambda components: (int(components.group(2)) - 1))(components),
                         (lambda components: (int(components.group(3)) - 1))(components)] 
                         for components in [(lambda job: re.search(r"move (\w*) from (\w*) to (\w*)", job))(job) for job in instructions]]

    for instruction in instruction_list:
        moved_crates = []

        for _ in range(instruction[0]):
            moved_crates.append(stacks[instruction[1]].pop())

        for crate in moved_crates:
            stacks[instruction[2]].append(crate)
        
    response_string = ""

    for stack in stacks:
        response_string += stack.pop()

    response_string = re.sub(r"[^a-zA-Z]", "", response_string)

    print(response_string)

    file.close()


def part2():
    file = open("input.txt")

    crate_raws = []

    line = file.readline()

    while line.rstrip():
        crate_raws.append(line)
        line = file.readline().rstrip()

    crate_raws.pop()

    stacks = [[] for _ in range(9)]

    for crate_raw in crate_raws:
        matches = re.findall(r"(\[(?:[\w])\]\s|\s{4})|(\[(?:[\w])\]|\s{3})", crate_raw)
        for column in range(9):
            if matches[column][0]:
                stacks[column].insert(0, matches[column][0].rstrip())
            else:
                stacks[column].insert(0, matches[column][1].rstrip())
    
    instructions = file.readlines()

    #cleans up the blanks
    for stack in stacks:
        count = stack.count("")
        for _ in range(count):
            stack.pop()

    instruction_list = []

    for job in instructions:
        tasks = re.search(r"move (\w*) from (\w*) to (\w*)", job)
        num_moved = int(tasks.group(1))
        origin = int(tasks.group(2)) - 1
        destination = int(tasks.group(3)) - 1
        instruction_list.append([num_moved, origin, destination])

    for instruction in instruction_list:
        moved_crates = []

        for _ in range(instruction[0]):
            moved_crates.append(stacks[instruction[1]].pop())

        moved_crates.reverse()

        for crate in moved_crates:
            stacks[instruction[2]].append(crate)

    response_string = ""

    for stack in stacks:
        response_string += stack.pop()

    response_string = re.sub(r"[^a-zA-Z]", "", response_string)

    print(response_string)

    file.close()



def main():
    part1()
    part2()


main()
