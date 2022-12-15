import re

def part1():
    
    row = 2000000

    with open("input.txt") as file:

        lines = file.readlines()

        sensor_beacon_dict = {}
        sensor_dist_dict = {}
        excluded = set()

        for line in lines:
            coordinates = re.findall("(-?\d+)", line)
            sensor_beacon_dict.update({(int(coordinates[0]), int(coordinates[1])): (int(coordinates[2]), int(coordinates[3]))})

        for sensor in sensor_beacon_dict:
            dist = abs(sensor[0] - sensor_beacon_dict.get(sensor)[0]) + abs(sensor[1] - sensor_beacon_dict.get(sensor)[1])
            sensor_dist_dict.update({sensor: dist})

        for sensor in sensor_dist_dict.copy():
            max_reach = (sensor[1] + sensor_dist_dict.get(sensor))
            min_reach = (sensor[1] - sensor_dist_dict.get(sensor))
            if row < min_reach or row > max_reach:
                sensor_dist_dict.pop(sensor)

        for sensor in sensor_dist_dict:
            reach_from = sensor[0]
            reach_dist = sensor_dist_dict.get(sensor) - abs(sensor[1] - row)
            for cell_column in range((reach_from - reach_dist),(reach_from + reach_dist + 1)):
                if (cell_column, row) not in sensor_beacon_dict.values():
                    excluded.add((cell_column, row))

        print(len(excluded))
             

def main():
    part1()
