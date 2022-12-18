import math
import random

class SimulatedAnnealing:
    def __init__(self, initialSolution, solutionEvaluator, initialTemp, finalTemp, tempReduction, neighborOperator, iterationPerTemp=100, alpha=10, beta=5):
        self.solution = initialSolution
        self.evaluate = solutionEvaluator
        self.currTemp = initialTemp
        self.finalTemp = finalTemp
        self.iterationPerTemp = iterationPerTemp
        self.alpha = alpha
        self.beta = beta
        self.neighborOperator = neighborOperator

        if tempReduction == "linear":
            self.decrementRule = self.linearTempReduction
        elif tempReduction == "geometric":
            self.decrementRule = self.geometricTempReduction
        elif tempReduction == "slowDecrease":
            self.decrementRule = self.slowDecreaseTempReduction
        else:
            self.decrementRule = tempReduction

    def linearTempReduction(self):
        self.currTemp -= self.alpha

    def geometricTempReduction(self):
        self.currTemp *= self.alpha

    def slowDecreaseTempReduction(self):
        self.currTemp = self.currTemp / (1 + self.beta * self.currTemp)

    def isTerminationCriteriaMet(self):
        # can add more termination criteria
        return self.currTemp <= self.finalTemp or self.neighborOperator(self.solution) == 0

    def run(self):
        while not self.isTerminationCriteriaMet():
            # iterate that number of times
            for i in range(self.iterationPerTemp):
                # get all of the neighbors
                neighbors = self.neighborOperator(self.solution)
                # pick a random neighbor
                newSolution = random.choice(neighbors)
                # get the cost between the two solutions
                cost = self.evaluate(self.solution) - self.evaluate(newSolution)
                # if the new solution is better, accept it
                if cost >= 0:
                    self.solution = newSolution
                # if the new solution is not better, accept it with a probability of e^(-cost/temp)
                else:
                    if random.uniform(0, 1) < math.exp(-cost / self.currTemp):
                        self.solution = newSolution
            # decrement the temperature
            self.decrementRule()

class Solution:
    """
Need to redo this to use the new action_cost thing for room/cost lookup, rather than using room objects.


Might be OK? Need to review some time
"""

    def __init__(self, move_list, remaining, openers, valve_values, action_cost, pressure_per = None, total_pressure = None):

        #contains a list of the rooms moved to, for the current permutation under consideration
        self.move_list = move_list
        #contains the remaining time
        self.remaining = remaining
        #contains a list of the openers
        self.openers = openers
        #contains a dictionary which correlates valves as strings to their values as integers
        self.valve_values = valve_values
        #Contains a dictionary of dictionaries used to lookup the cost of actions as action_cost[source][destination]
        self.action_cost = action_cost

        #conatins the pressure relieved per time step
        if pressure_per is None:
            self.pressure_per = 0
        #contains the total pressure relieved
        if total_pressure is None:
            self.total_pressure = 0


    def solve(self):

        #Loads the first two moves prior to beginning iteration based on the time remaining
        for opener in self.openers:
            opener.load_move(self)

        while not self.move_list == [] and self.remaining > 0:
            soonest_opener, latest_opener = self.soonest()
            soonest_opener.execute_move(self, latest_opener)
            soonest_opener.load_move(self)

        if self.remaining > 0:
            self.total_pressure += (self.remaining * self.pressure_per)

        return self.total_pressure

    def soonest(self):

        soonest = 10000000
        for opener in self.openers:
            if opener.time_in_move < soonest:
                soonest = opener.time_in_move
                if not latest_opener:
                    latest_opener = soonest_opener
                soonest_opener = opener
            else:
                latest_opener = opener
        return soonest_opener, latest_opener


class Opener:

    def __init__(self, room, time_in_move = 0, destination = ""):
        
        #the room the opener in question is in
        self.room = room
        if time_in_move is None:
            self.time_in_move = 0
        if destination is None:
            self.destination is ""
    

    def execute_move(self, solution, other_opener):

        if solution.remaining >= self.time_in_move:
            value = self.room.valve_values(self.destination)

            solution.pressure_per += value
            solution.remaining -= self.time_in_move
            solution.total_pressure += (solution.pressure_per * self.time_in_move)

            other_opener.time_in_move -= self.time_in_move

            self.room = self.destination
        else:
            solution.total_pressure += (solution.pressure_per * solution.remaining)
            solution.remaining = 0

    def load_move(self, solution):

        self.destination = solution.move_list.pop(-1)
        self.time_in_move = solution.action_costs[self.room][self.destination]



class Node:

    def __init__(self, room, map, path):

        self.room = room
        self.map = map
        self.path = path  

    def __repr__(self):

        return f"Node {self.room}"


class Map:

    def __init__(self, neighbor_map, valid_rooms):

        self.neighbor_map = neighbor_map
        self.valid_rooms = valid_rooms


def breadth_first_search(source, map):
   
    path_costs = {}

    frontier = [Node(source, map, [source])]
    explored = set(source)

    while frontier is not []:

        current = frontier.pop(0)
        #Clears out any duplicates in the frontier. Would be more efficient to avoid generating them, but this would be harder.
        for node in frontier:
            if node.room is current.room:
                frontier.remove(node)
        
        if current.room in map.valid_rooms and current.room is not source:
            cost = len(current.path)
            path_costs.update({current.room: cost})
        
        #Then add the neighbors to the popped node to the frontier
        #And add the room we were in to the explored set
        for room in map.neighbor_map[current.room]:
            if room not in explored:
                frontier.append(Node(room, map, current.path + [room]))
        explored.add(current.room)

    return path_costs
    #Returns a dict containing the destination rooms and costs for all valid rooms given the source room provided

def part1():
    with open("test_input.txt") as file:

        lines = file.readlines()

        #Dont need regex to find values. Can use string splits
        for line in lines:
            valve = line.split("Valve ")[1][0:1]


        time = 30
        start_room = "AA"
        openers = []
        move_list = ["DD", "BB", "JJ", "HH", "EE", "CC"]
        valve_values = {"BB": 13, "CC": 2, "DD": 20, "EE": 3, "HH": 22, "JJ": 21}

        #neighbor_map is going to be a dict of dicts
        neighbor_map = {}
        
        valid_rooms = start_room + valve_values.keys    

        map = Map(neighbor_map, valid_rooms)

        #Still need to figure out how to get input from the file, and determine valid_rooms
     
        
        

        #iterates over every valid source room, using bfs to generate a dict of the destination rooms and their costs for the given source room
        #Final result is a dict of dicts, action_cost, which can be used to lookup the action cost of going from one room to another by action_cost[source][destination]
        action_cost = {}
        for room in map.valid_rooms:
            action_cost.update({room: breadth_first_search(room, map)})


        solution = Solution(move_list, time, openers, valve_values, action_cost)

        print.solution.solve()



def main():
    part1()


main()


#Credit for the annealing framework
# https://towardsdatascience.com/optimization-techniques-simulated-annealing-d6a4785a1de7
