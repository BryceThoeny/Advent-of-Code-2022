import re


def draw(from_point, to_point, limits, sensor_beacon_dict):

    point = list(from_point)
    points_drawn = set()

    if from_point[0] < to_point[0]:
        x_iteration = 1
    else:
        x_iteration = -1
    if from_point[1] < to_point[1]:
        y_iteration = 1
    else:
        y_iteration = -1

    while point != list(to_point):
        point[0] += x_iteration
        point[1] += y_iteration
        if point[0] in range(limits + 1) and point[1] in range(limits + 1):
            if ((point[0], point[1]) not in sensor_beacon_dict.keys() and 
                (point[0], point[1]) not in sensor_beacon_dict.values()):
                    points_drawn.add((point[0], point[1]))

    return points_drawn


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


def part2():
    
    limits = 4000000

    with open("input.txt") as file:

        lines = file.readlines()

        sensor_beacon_dict = {}
        sensor_dist_dict = {}

        for line in lines:
            coordinates = re.findall("(-?\d+)", line)
            sensor_beacon_dict.update({(int(coordinates[0]), int(coordinates[1])): (int(coordinates[2]), int(coordinates[3]))})

        for sensor in sensor_beacon_dict:
            dist = abs(sensor[0] - sensor_beacon_dict.get(sensor)[0]) + abs(sensor[1] - sensor_beacon_dict.get(sensor)[1])
            sensor_dist_dict.update({sensor: dist})

        for sensor in sensor_dist_dict.copy():
            #Calculate the maximum/minimum row and column
            max_row = (sensor[1] + sensor_dist_dict.get(sensor))
            min_row = (sensor[1] - sensor_dist_dict.get(sensor))
            max_col = (sensor[0] + sensor_dist_dict.get(sensor))
            min_col = (sensor[0] - sensor_dist_dict.get(sensor))

            #Check if there is no overlap with the (0, limits) interval given these maxima/minima
            if  (not (max_row >= limits >= min_row or max_row >= 0 >= min_row or (max_row <= limits and min_row >= 0)) or
                 not (max_col >= limits >= min_col or max_col >= 0 >= min_col or (max_col <= limits and min_col >= 0))):
                    #If there is no overlap, we do not need to consider further, and we pop the sensor from the list.
                    sensor_dist_dict.pop(sensor)

        to_check = set()

        for sensor in sensor_dist_dict:
            #First, draw from min_col to min_row
            #
            from_point = (((sensor[0] - sensor_dist_dict.get(sensor)) - 1), sensor[1])
            to_point = (sensor[0], ((sensor[1] - sensor_dist_dict.get(sensor)) -1 ))
            to_check = to_check.union(draw(from_point, to_point, limits, sensor_beacon_dict))
            #
            #Then, from min_row to max_col
            from_point = (sensor[0], ((sensor[1] - sensor_dist_dict.get(sensor)) - 1))
            to_point = (((sensor[0] + sensor_dist_dict.get(sensor)) + 1), sensor[1])
            to_check = to_check.union(draw(from_point, to_point, limits, sensor_beacon_dict))
            #
            #Then from max_col to max_row
            from_point = (((sensor[0] + sensor_dist_dict.get(sensor)) + 1), sensor[1])
            to_point = (sensor[0], ((sensor[1] + sensor_dist_dict.get(sensor)) +1 ))
            to_check = to_check.union(draw(from_point, to_point, limits, sensor_beacon_dict))
            #
            #And finally from max_row to min_col
            from_point = (sensor[0], ((sensor[1] + sensor_dist_dict.get(sensor)) +1 ))
            to_point = (((sensor[0] - sensor_dist_dict.get(sensor)) - 1), sensor[1])
            to_check = to_check.union(draw(from_point, to_point, limits, sensor_beacon_dict))

        count = 0
        total = len(to_check)
        for possibility in to_check:
            count += 1
            if count % 1000000 == 0:
                print((count / total))
            #Loop over every sensor in the set, and find the distance to the closest one
            found = True
            for sensor in sensor_dist_dict:
                #Calculate the distance between the point and the sensor
                #This distance is what is not calculating correctly
                distance = abs(possibility[0] - sensor[0]) + abs(possibility[1] - sensor[1])
                if distance <= sensor_dist_dict.get(sensor):
                    found = False
                    break

            if found:
                print(possibility)
                print(((possibility[0] * 4000000) + possibility[1]))
                #Do your calcs


def main():
    part1()
    part2()

main()
