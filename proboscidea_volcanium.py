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

    def __init__(self, room, map, path = None, cost = None):

        self.room = room
        self.map = map
        
        if path is None:
            self.path = [self.room]
        if cost is None:
            self.cost = 0
     

    def __repr__(self):

        return f"Node {self.room}"



def breadth_first_search(source, map, valid_rooms):

    current = Node(source, map, [source])
    frontier = [current]
    path_costs = {}

    while True:
        #Pop the oldest item off of the frontier
        current = frontier.pop(0)
        
        if current.room in valid_rooms:
            cost = len(current.path)
            path_costs.update({current.room: cost})
            
        else:
            #If the node popped from the frontier isn't the destination, then add the neighbors to the popped node to the frontier
            update_frontier(current.room)
            #And add the popped node to explored
            explored.add(current.room)
            
            
            
            
    

    #Returns a dict containing the destination rooms and costs for all valid rooms given the source room provided

def part1():
    with open("test_input.txt") as file:

        lines = file.readlines()

        time = 30
        start_room = "AA"
        openers = []
        move_list = ["DD", "BB", "JJ", "HH", "EE", "CC"]
        valve_values = {"BB": 13, "CC": 2, "DD": 20, "EE": 3, "HH": 22, "JJ": 21}

        #map is going to be a dict of dicts
        map = {}
        
        #Still need to figure out how to get input from the file, and determine valid_rooms
     
        #Iterates over all combinations of valid source and destination rooms
        #Calls the BFS function for each one, and updates the path costs with a dict entry showing the cost to get to the keyed destination
        #Final result is a dict of dicts, action_cost, which can be used to lookup the action cost of going from one room to another by action_cost[source][destination]
        
        valid_rooms = start_room + valve_values.keys

        #iterates over every valid source room, using bfs to generate a dict of the destination rooms and their costs for the given source room
        action_cost = {}
        for room in valid_rooms:
            action_cost.update({room: breadth_first_search(room, map, valid_rooms)})


        solution = Solution(move_list, time, openers, valve_values, action_cost)

        print.solution.solve()



def main():
    part1()


main()


#Credit for the annealing framework
# https://towardsdatascience.com/optimization-techniques-simulated-annealing-d6a4785a1de7
