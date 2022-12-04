import string

class Rucksack():

    def __init__(self, compartment1, compartment2):
        self.compartment1 = compartment1
        self.compartment2 = compartment2


def part1():
    
    file = open("input.txt")
    lines = file.readlines()
    
    rucksacks = set()
    prioritysum = 0
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase

    for line in lines:
        linelen = len(line)
        compartment1 = line[:linelen // 2]
        compartment2 = line[linelen // 2:]
        rucksacks.add(Rucksack(compartment1, compartment2))

    for sack in rucksacks:
        for item in sack.compartment1:
            if item in sack.compartment2 and item in lowercase:
                prioritysum += (ord(item) - 96)
                break
            elif item in sack.compartment2 and item in uppercase:
                prioritysum += (ord(item) - 38)
                break

    print(prioritysum)

    file.close()


def part2():

    file = open("input.txt")
    lines = file.readlines()
    
    group = list()
    groups = list()

    prioritysum = 0
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase

    for line in lines:
        linenum = lines.index(line) + 1
        group.append(line)

        if linenum % 3 == 0:
            groups.append(group)
            group = list()

    for group in groups:
        for character in group[0]:
            if character in group[1] and character in group[2] and character in lowercase:
                prioritysum += (ord(character) - 96)
                break
            elif character in group[1] and character in group[2] and character in uppercase:
                prioritysum += (ord(character) - 38)
                break

    print(prioritysum)

    file.close()


def main():
    part1()
    part2()


main()