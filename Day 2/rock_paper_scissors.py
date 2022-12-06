def part1():
    file = open("input.txt", "r")

    lines = file.readlines()

    my_score = 0

    score_guide = {"X": 1, "Y": 2, "Z": 3}
    their_moves = ["A", "B", "C"]
    my_moves = ["X", "Y", "Z"]

    for line in lines:
        their_move = line.split()[0]
        my_move = line.split()[1]
        
        if my_moves.index(my_move) == their_moves.index(their_move):
            my_score += 3
        elif my_moves.index(my_move) != 0:
            if (my_moves.index(my_move) - 1) == their_moves.index(their_move):
                my_score += 6
        else:
            if their_moves.index(their_move) == 2:
                my_score += 6
        my_score += score_guide[my_move]

    print(my_score)

    file.close()

def part2():
    file = open("input.txt", "r")

    lines = file.readlines()

    my_score = 0

    score_guide = {"A": 1, "B": 2, "C": 3}
    moves = ["A", "B", "C"]

    for line in lines:
        their_move = line.split()[0]
        goal = line.split()[1]

        if goal == "X":
            if their_move == "A":
                my_move = "C"
            else:
                my_move = moves[(moves.index(their_move) - 1)]
        elif goal == "Z":
            if their_move == "C":
                my_move = "A"
            else:
                my_move = moves[(moves.index(their_move) + 1)]
        else:
            my_move = their_move
        
        if moves.index(my_move) == moves.index(their_move):
            my_score += 3
        elif moves.index(my_move) != 0:
            if (moves.index(my_move) - 1) == moves.index(their_move):
                my_score += 6
        else:
            if moves.index(their_move) == 2:
                my_score += 6

        my_score += score_guide[my_move]

    print(my_score)

    file.close()


def main():
    part1()
    part2()


main()
