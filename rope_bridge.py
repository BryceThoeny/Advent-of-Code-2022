def head_mover(direction, head):
    if direction == "U":
        head[1] += 1
    elif direction == "D":
        head[1] -=1
    elif direction == "R":
        head[0] += 1
    elif direction == "L":
        head[0] -= 1


def tail_mover(sep_x, sep_y, tail):
    if sep_y == 2:
        tail[1] += 1
        if sep_x > 0:
            tail[0] += 1
        elif sep_x < 0:
            tail[0] -= 1
    elif sep_y == -2:
        tail[1] -= 1
        if sep_x > 0:
            tail[0] += 1
        elif sep_x < 0:
            tail[0] -= 1
    elif sep_x == 2:
        tail[0] += 1
        if sep_y > 0:
            tail[1] += 1
        elif sep_y < 0:
            tail[1] -= 1
    elif sep_x == -2:
        tail[0] -= 1
        if sep_y > 0:
            tail[1] += 1
        elif sep_y < 0:
            tail[1] -= 1


def check_add(tail, touched):
    if (tail[0], tail[1]) not in touched:
        touched.append((tail[0], tail[1]))


def part1():

    file = open("input.txt")

    lines = file.readlines()
    head, tail = [0, 0], [0, 0]
    touched = [(0, 0)]

    for line in lines:
        instruction = line.split()
        for step in range(int(instruction[1])):
            head_mover(instruction[0], head)
            sep_x, sep_y = head[0] - tail[0], head[1] - tail[1]
            tail_mover(sep_x, sep_y, tail)
            check_add(tail, touched)

    print(len(touched))

    file.close()


def part2():

    file = open("input.txt")

    lines = file.readlines()
    rope = [[0, 0] for x in range(1, 11)]
    touched = [(0, 0)]

    for line in lines:
        instruction = line.split()
        for step in range(int(instruction[1])):
            prev_knot = []
            for knot in rope:
                if prev_knot == []:
                    head_mover(instruction[0], knot)
                else:
                    sep_x, sep_y = prev_knot[0] - knot[0], prev_knot[1] - knot[1]
                    tail_mover(sep_x, sep_y, knot)
                prev_knot = knot
            check_add(rope[9], touched)
        
    print(len(touched))

    file.close()


def main():
    part1()
    part2()


main()