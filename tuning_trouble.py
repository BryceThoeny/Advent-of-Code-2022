def part1():
    file = open("input.txt")
    
    data = file.readline()

    data_enum = list(enumerate(data, start = 1))

    recents = []

    for character_tuple in data_enum:
        if character_tuple[0] < 4:
            recents.append(character_tuple[1])
        else:
            if (character_tuple[1] not in recents 
                                   and recents[0] != recents[1] 
                                   and recents[0] != recents[2] 
                                   and recents[1] != recents[2]):
                return character_tuple[0]
            recents.pop(0)
            recents.append(character_tuple[1])

    file.close()


def part2():
    file = open("input.txt")
    
    data = file.readline()

    data_enum = list(enumerate(data, start = 1))

    recents = []

    for character_tuple in data_enum:

        repeat = False

        if character_tuple[0] < 14:
            recents.append(character_tuple[1])
            
        else:
            for i in range(13):
                if recents.count(recents[i]) > 1:
                    repeat = True

            if (character_tuple[1] not in recents 
                                   and not repeat):
                return character_tuple[0]
            recents.pop(0)
            recents.append(character_tuple[1])

    file.close()


def main():
    print(part1())
    print(part2())


main()