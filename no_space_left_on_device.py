def part1():

    file = open("input.txt")
    lines = file.readlines()

    pointer = path_name = "/"
    directories = {"/": 0}
    parentage = []

    for line in lines:
        line = line.rstrip()

        #This moves the pointer around as required, and tracks directory parentage 
        if line[0] == "$" and line[2] != "l":
            if line[5] == "/":
                pointer = "/"
                parentage = []
            elif line[5] == ".":
                pointer = parentage.pop()

            #If directory is changed to something by name, read out the name, add pointer to parentage, set-up the path name, and update pointer to the new directory name
            else:
                directory_name = ""
                for character_num in range(5, len(line)):
                    directory_name += line[character_num]

                parentage.append(pointer)

                path_name = directory_name
                for dir in reversed(parentage):
                    path_name += f"-{dir}"
                
                directories.update({path_name: 0})    
                pointer = directory_name

        # if the line starts with a number, it is a file and we should add its size to the directories
        if line[0].isdigit():
            file_size = ""
            #Read the file size from the line
            for character in line:
                if character.isdigit():
                    file_size += character
                elif character == " ":
                    break
        
            #Convert the path name to a list of directories, iterate through, adding the file size to the path name where the file was found, and every parent directory
            pn_list = path_name.split("-")
            for dir in pn_list.copy():
                sub_pn = "-".join(pn_list)
                directories[sub_pn] += int(file_size)
                pn_list.pop(0)

    sum = 0

    #Loop through directories, adding to sum if 100000 or less
    for directory in directories:
        if directories[directory] <= 100000:
            sum += directories[directory]

    print(sum)

    file.close()


def part2():

    file = open("input.txt")
    lines = file.readlines()

    pointer = path_name = "/"
    directories = {"/": 0}
    parentage = []

    for line in lines:
        line = line.rstrip()

        #This moves the pointer around as required, and tracks directory parentage 
        if line[0] == "$" and line[2] != "l":
            if line[5] == "/":
                pointer = "/"
                parentage = []
            elif line[5] == ".":
                pointer = parentage.pop()

            #If directory is changed to something by name, read out the name, add pointer to parentage, set-up the path name, and update pointer to the new directory name
            else:
                directory_name = ""
                for character_num in range(5, len(line)):
                    directory_name += line[character_num]

                parentage.append(pointer)

                path_name = directory_name
                for dir in reversed(parentage):
                    path_name += f"-{dir}"
                
                directories.update({path_name: 0})    
                pointer = directory_name

        # if the line starts with a number, it is a file and we should add its size to the directories
        if line[0].isdigit():
            file_size = ""
            #Read the file size from the line
            for character in line:
                if character.isdigit():
                    file_size += character
                elif character == " ":
                    break
        
            #Convert the path name to a list of directories, iterate through, adding the file size to the path name where the file was found, and every parent directory
            pn_list = path_name.split("-")
            for dir in pn_list.copy():
                sub_pn = "-".join(pn_list)
                directories[sub_pn] += int(file_size)
                pn_list.pop(0)

    #Set smallest to its maximum possible value, and calculate the space we need to clear
    smallest = 40000000
    to_clear = directories["/"] - 40000000
    
    #Check every directory, if it is at least as big as the space to clear, but smaller than the previous smallest, update smallest
    for directory in directories:
        if directories[directory] > to_clear and directories[directory] < smallest:
            smallest = directories[directory]

    print(smallest)

    file.close()


def main():

    part1()
    part2()


main()