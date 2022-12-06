file = open("input.txt", "r")

lines = file.readlines()
elf_cals = 0
top3 = [0, 0, 0]

for line in lines:
    if line != '\n':
        elf_cals += int(line)
    else:
        if elf_cals > top3[2]:
            top3[2] = elf_cals
            top3.sort(reverse = True)
        elf_cals = 0

print(top3)
print(sum(top3))

file.close()
