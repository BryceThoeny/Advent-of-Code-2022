def part1():

    file = open("input.txt")

    lines = file.readlines()

    cycle = 0
    stop_cycle = [x for x in range(20, 260, 40)]
    reg_list = []
    register = 1
    answer = 0

    for line in lines:
        cycle += 1
        if cycle in stop_cycle:
            reg_list.append((cycle, (register * cycle)))
        if line[0] == "a":
            cycle += 1
            if cycle in stop_cycle:
                reg_list.append((cycle, (register * cycle)))
            register += int(line.split()[1])

    for signal_strength in reg_list:
        answer += signal_strength[1]

    print(answer)

    file.close()


def part2():

    file = open("input.txt")

    lines = file.readlines()

    cycle = 0
    edge_check = [x for x in range(40, 280, 40)]
    register = 1
    sprite = [register, register + 1, register + 2]
    pixel = []

    for line in lines:
        cycle += 1
        if (cycle % 40) in sprite:
            if (cycle in edge_check and 0 not in sprite or
                cycle not in edge_check):
                    pixel.append("#")
            elif cycle in edge_check and 0 in sprite:
                pixel.append(".")
        else:
            pixel.append(".")

        if line[0] == "a":
            cycle += 1
            if (cycle % 40) in sprite:
                if (cycle in edge_check and 0 not in sprite or 
                    cycle not in edge_check):
                        pixel.append("#")
                elif cycle in edge_check and 0 in sprite:
                    pixel.append(".")
            else:
                pixel.append(".")
            register += int(line.split()[1])
            sprite = [register, register + 1, register + 2]

    for i in range(6):
        for j in range(40):
            print(pixel[j + (i * 40)], end = "")
        print("\n", end = "")

    file.close()


def main():
    part1()
    part2()


main()
