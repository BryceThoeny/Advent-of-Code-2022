import re

class Monkey():
    def __init__(self, number, items, true_monkey, false_monkey, op_char, op_val, test_val):
        self.number = number
        self.items = items
        self.true_monkey = true_monkey
        self.false_monkey = false_monkey
        self.op_char = op_char
        self.op_val = op_val
        self.test_val = test_val


    def __str__(self):
        return f"Monkey {self.number}"


    def __repr__(self):
        return self.__str__()


    def inspect(self, item):
        if self.op_char == "*":
            if self.op_val == "old":
                return (int(item) ** 2)
            else:
                return (int(item) * int(self.op_val))
        elif self.op_char == "+":
            if self.op_val == "old":
                return (int(item) * 2)
            else:
                return (int(item) + int(self.op_val))


    def test(self, item, monkeys):
        if item % int(self.test_val) == 0:
            monkeys[int(self.true_monkey)][0].items.append(item)
        else:
            monkeys[int(self.false_monkey)][0].items.append(item)

def part1():

    file = open("input.txt")
    lines = file.readlines()

    monkeys = []

    for i in range(8):
        #Returns a string with the number of the monkey
        monkey_num = re.findall(r"Monkey (.)", lines[0])[0]

        #Returns a list of strings of the starting items for the monkey
        start_items = [x.strip() for x in ((re.findall(r"  Starting items: ?(.*)\n", lines[1])[0]).split(","))]

        #Returns the character for the operation the monkey performs, and the value
        op_info = re.findall(r"  Operation: new = old (.) (.+)\n", lines[2])
        op_char, op_val = op_info[0][0], op_info[0][1]

        #Returns the test value
        test_val = re.findall(r"  Test: divisible by (\d+)\n", lines[3])[0]

        #Returns the monkey thrown to if true/false
        true_monkey = re.findall(r"    If true: throw to monkey (\d+)\n", lines[4])[0]
        false_monkey = re.findall(r"    If false: throw to monkey (\d+)\n", lines[5])[0]

        monkeys.append([Monkey(monkey_num, start_items, true_monkey, false_monkey, op_char, op_val, test_val), 0])
        if i < 7:
            for _ in range(7):
                lines.pop(0)
    
    for round_num in range(1, 21):
        for monkey in monkeys:
            for item in monkey[0].items:
                monkey[1] += 1
                new_val = (monkey[0].inspect(item)) // 3
                monkey[0].test(new_val, monkeys)
            #After going through items, clear the list
            monkey[0].items = []

    first = 0
    second = 0
    for monkey in monkeys:
        if monkey[1] > second and monkey[1] > first:
            second = first
            first = monkey[1]
        elif monkey[1] > second:
            second = monkey[1]
    monkey_business = first * second

    print(monkey_business)

    file.close()


def part2():

    file = open("input.txt")
    lines = file.readlines()

    monkeys = []
    lcm = 1

    for i in range(8):
        #Returns a string with the number of the monkey
        monkey_num = re.findall(r"Monkey (.)", lines[0])[0]

        #Returns a list of strings of the starting items for the monkey
        start_items = [x.strip() for x in ((re.findall(r"  Starting items: ?(.*)\n", lines[1])[0]).split(","))]

        #Returns the character for the operation the monkey performs, and the value
        op_info = re.findall(r"  Operation: new = old (.) (.+)\n", lines[2])
        op_char, op_val = op_info[0][0], op_info[0][1]

        #Returns the test value
        test_val = re.findall(r"  Test: divisible by (\d+)\n", lines[3])[0]
        lcm *= int(test_val)

        #Returns the monkey thrown to if true/false
        true_monkey = re.findall(r"    If true: throw to monkey (\d+)\n", lines[4])[0]
        false_monkey = re.findall(r"    If false: throw to monkey (\d+)\n", lines[5])[0]

        monkeys.append([Monkey(monkey_num, start_items, true_monkey, false_monkey, op_char, op_val, test_val), 0])
        if i < 7:
            for _ in range(7):
                lines.pop(0)
    
    for round_num in range(1, 10001):
        for monkey in monkeys:
            for item in monkey[0].items:
                monkey[1] += 1
                new_val = (monkey[0].inspect(item))
                #The remaining amount beyond the least common multiple of the divisors is the exact same as the value itself for the rules we consider
                new_val = new_val % lcm
                monkey[0].test(new_val, monkeys)
            #After going through items, clear the list
            monkey[0].items = []

    first = 0
    second = 0
    for monkey in monkeys:
        if monkey[1] > second and monkey[1] > first:
            second = first
            first = monkey[1]
        elif monkey[1] > second:
            second = monkey[1]
    monkey_business = first * second

    print(monkey_business)

    file.close()


def main():
    part1()
    part2()

main()