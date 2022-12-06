import re

def part1():

    file = open("input.txt")

    lines = file.readlines()

    pair_count = 0

    for line in lines:

        matches = re.search(r"^(.*?)-(.*?),(.*?)-(.*?)$", line)
        
        pair1_min = matches.group(1)
        pair1_max = matches.group(2)
        pair2_min = matches.group(3)
        pair2_max = matches.group(4)

        pair1_range = int(pair1_max) - int(pair1_min)
        pair2_range = int(pair2_max) - int(pair2_min)

        pair1 = set([int(pair1_min)])
        pair2 = set([int(pair2_min)])

        for i in range(pair1_range):
            pair1.add((int(pair1_min) + (i + 1)))
        for j in range(pair2_range):
            pair2.add((int(pair2_min) + (j + 1)))

        if pair1.issubset(pair2) or pair2.issubset(pair1):
            pair_count += 1

    print(pair_count)

    file.close()


def part2():
    
    file = open("input.txt")

    lines = file.readlines()

    pair_count = 0

    for line in lines:

        matches = re.search(r"^(.*?)-(.*?),(.*?)-(.*?)$", line)
        
        pair1_min = matches.group(1)
        pair1_max = matches.group(2)
        pair2_min = matches.group(3)
        pair2_max = matches.group(4)

        pair1_range = int(pair1_max) - int(pair1_min)
        pair2_range = int(pair2_max) - int(pair2_min)

        pair1 = set([int(pair1_min)])
        pair2 = set([int(pair2_min)])

        for i in range(pair1_range):
            pair1.add((int(pair1_min) + (i + 1)))
        for j in range(pair2_range):
            pair2.add((int(pair2_min) + (j + 1)))

        if len(pair1) > len(pair2):
            for number in pair2:
                if number in pair1:
                    pair_count += 1
                    break
        else:
            for number in pair1:
                if number in pair2:
                    pair_count += 1
                    break

    print(pair_count)

    file.close()


def main():

    part1()
    part2()


main()
