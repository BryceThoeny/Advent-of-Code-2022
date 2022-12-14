import sys
from functools import cmp_to_key

def compare(left, right):
    if isinstance(left, int) and isinstance(right, int):
        if left > right:
            return -1
        elif right > left:
            return 1
        else:
            return 0
    
    elif isinstance(left, int):
        left = [left]

    elif isinstance(right, int):
        right = [right]
        
    for value in (compare(l_subpacket, r_subpacket) for l_subpacket, r_subpacket in zip(left, right)):
            if value != 0:
                return value

    if len(left) < len(right):
        return 1
    elif len(left) > len(right):
        return -1
    else:
        return 0

def part1():

    with open("input.txt") as file:

        lines = file.readlines()

        packets = [eval(l) for l in lines if l.strip()]

        pairs = zip(packets[::2], packets[1::2])
        print(sum(idx + 1 for idx, (l, r) in enumerate(pairs) if compare(l, r) >= 0))


def part2():

    with open("input.txt") as file:

        lines = file.readlines()

        packets = [eval(l) for l in lines if l.strip()]

        markers = [[[6]], [[2]]]
        packets_markers = sorted(packets + markers, key=cmp_to_key(compare), reverse=True)
        idx1, idx2 = [packets_markers.index(m) for m in markers]

        print((idx1 + 1) * (idx2 + 1))

def main():
    part1()
    part2()

main()
