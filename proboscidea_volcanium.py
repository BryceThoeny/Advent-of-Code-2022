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

    def __init__(self, move_list, remaining, openers, valve_values, action_cost, pressure_per = 0, total_pressure = 0):

        #contains a list of the rooms moved to, for the current permutation under consideration
        move_list = self.move_list
        #contains the remaining time
        remaining = self.remaining
        #contains a list of the openers
        openers = self.openers
        #contains a dictionary which correlates valves as strings to their values as integers
        valve_values = self.valve_values
        #Contains a dictionary of dictionaries used to lookup the cost of actions as action_cost[source][destination]

        #conatins the pressure relieved per time step
        pressure_per = self.pressure_per
        #contains the total pressure relieved
        total_pressure = self.pressure


    def solve(self):

        #Loads the first two moves prior to beginning iteration based on the time remaining
        for opener in self.openers:
            opener.load_move(self)

        while not move_list == [] and self.remaining > 0:
            soonest_opener, latest_opener = soonest()
            soonest_opener.execute_move(self, latest_opener)
            soonest_opener.load_move(self)

        if self.remaining > 0:
            self.total_pressure += (self.remaining * self.pressure_per)

        return total_pressure

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
        room = self.room
        time_in_move = self.time_in_move
        destination = self.destination

    def execute_move(self, solution, other_opener):

        if solution.remaining >= self.time_in_move:
            value = self.room.valve_values(self.destination)

            solution.pressure_per += value
            solution.remaining -= self.time_in_move
            solution.total_pressure += (solution.pressure_per * self.time_in_move)

            other_opener.time_in_move -= self.time_in_move

            self.room = destination
        else:
            solution.total_pressure += (solution.pressure_per * solution.remaining)
            solution.remaining = 0

    def load_move(self, solution):

        self.destination = solution.move_list.pop(-1)
        self.time_in_move = solution.action_costs[self.room][self.destination]


def breadth_first_search(source, destination):
    foo = bar

    #Returns the cost to get to the destination from the source

def part1():
    with open("test_input.txt") as file:

        lines = file.readlines()

        time = 30
        start_room = "AA"
        openers = []
        move_list = ["DD", "BB", "JJ", "HH", "EE", "CC"]
        valve_values = {"BB": 13, "CC": 2, "DD": 20, "EE": 3, "HH": 22, "JJ": 21}
        
        #Still need to figure out how to get input from the file, and determine valid_rooms
     
        #Iterates over all combinations of valid source and destination rooms
        #Calls the BFS function for each one, and updates the path costs with a dict entry showing the cost to get to the keyed destination
        #Final result is a dict of dicts, action_cost, which can be used to lookup the action cost of going from one room to another by action_cost[source][destination]
        action_cost = {}
        valid_rooms = start_room + valve_values.keys
        for source_room in valid_rooms:
            path_costs = {}
            for destination_room in valid_rooms:
                path_costs.update({destination_rooom: breadth_first_search(source_room, destination_room)})

            action_cost.update({source_room: path_costs})

        solution = Solution(move_list, remaining, openers, valve_values, action_cost)

        print.solution.solve()



def main():
    part1()


main()


#Credit for the annealing framework
# https://towardsdatascience.com/optimization-techniques-simulated-annealing-d6a4785a1de7