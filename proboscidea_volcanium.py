import math
import random

class SimulatedAnnealing:
    def __init__(self, initial_move_list, solutionEvaluator, initialTemp, finalTemp, tempReduction, neighborOperator, iterationPerTemp=100, alpha=0.99, beta=5):
        self.move_list = initial_move_list
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
        return self.currTemp <= self.finalTemp

    def run(self):
        while not self.isTerminationCriteriaMet():
            # iterate that number of times
            for i in range(self.iterationPerTemp):
                # get all of the neighbors
                neighbors = self.neighborOperator(self.move_list)
                # pick a random neighbor, and retain copies of the original move_list
                new_move_list = random.choice(neighbors)
                original_move_list = self.move_list.copy()
                original_new_move_list = new_move_list.copy()
                # get the score between the two solutions
                original_score = self.evaluate(self.move_list)
                new_score = self.evaluate(new_move_list)
                score = new_score - original_score
                # if the new solution is better, accept it
                checker = math.exp(score / self.currTemp)
                if score >= 0:
                    self.move_list = original_new_move_list
                    print(new_score)
                # if the new solution is not better, accept it with a probability of e^(-cost/temp)
    
                elif random.uniform(0, 1) < checker:
                    self.move_list = original_new_move_list
                    print(new_score)
                # if it is not accepted, reset the move_list considered to the original move_list
                else:
                    self.move_list = original_move_list
                    print(original_score)
            # decrement the temperature
            self.decrementRule()

        return original_score

class Solution:
    def __init__(self, possible_moves, remaining, openers, valve_values, action_cost, pressure_per = None, total_pressure = None, move_list = None):

        #contains a set of the possible moves for the problem
        self.possible_moves = possible_moves
        #contains the remaining time
        self.remaining = remaining
        #contains a list of the openers
        self.openers = openers
        #contains a dictionary which correlates valves as strings to their values as integers
        self.valve_values = valve_values
        #Contains a dictionary of dictionaries used to lookup the cost of actions as action_cost[source][destination]
        self.action_cost = action_cost

        #Contains the initial list of moves to be considered
        if move_list is None:
            self.move_list = list(possible_moves)
        #conatins the pressure relieved per time step
        if pressure_per is None:
            self.pressure_per = 0
        #contains the total pressure relieved
        if total_pressure is None:
            self.total_pressure = 0

    def anneal(self):

        #First argument is the initial solution (The initial list of moves to try)
        #Second argument is the solution evaluator (the function to provide a score for the solution in question)
        #neighbor_states is a function to provide the neighboring permutations of the move set.
        
        annealer = SimulatedAnnealing(self.move_list, self.solve, 1500, 0.15, "geometric", self.neighbor_states)
        return annealer.run()

    def neighbor_states(self, move_list):
        #Gives a list of neighboring permutations of the current move_list
        permutations = []

        for move in move_list:
            current = move_list.index(move)
            for swap_move in move_list:
                swapped = move_list.copy()
                swapped_index = move_list.index(swap_move)
                if swapped_index > current:
                    swapped[current], swapped[swapped_index] = swapped[swapped_index], swapped[current]
                    permutations.append(swapped)

        return permutations


    def solve(self, move_list):

        #Loads the first two moves prior to beginning iteration based on the time remaining
        self.move_list = move_list
        for opener in self.openers:
            opener.load_move(self, move_list)

        self.remaining = 30
        self.pressure_per = 0
        self.total_pressure = 0
        starting_time = self.remaining

        while self.remaining > 0:
            if len(self.openers) > 1:
                soonest_opener, latest_opener = self.soonest()
            else:
                soonest_opener = self.openers[0]
                latest_opener = None
            soonest_opener.execute_move(self, latest_opener)
            if self.move_list != []:
                soonest_opener.load_move(self, move_list)
            else:
                soonest_opener.time_in_move = starting_time
                soonest_opener.room = "AA"
    
        
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

    def __init__(self, room, identity, time_in_move = None, destination = None):
        
        #the room the opener in question is in
        self.room = room
        self.identity = identity
        if time_in_move is None:
            self.time_in_move = 0
        if destination is None:
            self.destination = ""
    
    def __repr__(self):

        return f"{self.identity}"

    def execute_move(self, solution, other_opener):

        #When executing the shortest move, if the time to complete the move is less than the remaining time
        if solution.remaining >= self.time_in_move:
            
            #First, increase the total pressure relieved by the current pressure per, multiplied by the time to perform the move
            solution.total_pressure += (solution.pressure_per * self.time_in_move)
            #Then, increase pressure per by the value of the vale for the move performed.
            solution.pressure_per += solution.valve_values[self.destination]
            #And reduce the remaining time for both the overall problem, and for the other opener, if it exists
            solution.remaining -= self.time_in_move
            if other_opener:
                other_opener.time_in_move -= self.time_in_move

            #And finally, set the opener's room to the destination room
            self.room = self.destination
        #If the time to complete the soonest move is more than the remaining time
        else:
            #Increase the total pressure by the pressure per, multiplied by the remaining time
            solution.total_pressure += (solution.pressure_per * solution.remaining)
            #And set the remaining time to 0
            solution.remaining = 0

    def load_move(self, solution, move_list):

        self.destination = move_list.pop(0)
        self.time_in_move = solution.action_cost[self.room][self.destination]


class Node:

    def __init__(self, room, room_map, path):

        self.room = room
        self.room_map = room_map
        self.path = path  

    def __repr__(self):

        return f"Node {self.room}"


class RoomMap:

    def __init__(self, neighbor_map, valid_rooms):

        self.neighbor_map = neighbor_map
        self.valid_rooms = valid_rooms


def breadth_first_search(source, room_map):
   
    path_costs = {}
    explored = set()

    frontier = [Node(source, room_map, [source])]

    while len(frontier) != 0:

        #Takes the oldest node in the frontier as the current node, proceeding if the node has not already been explored.
        while True:
            current = frontier.pop(0)
            if current.room not in explored:
                break
        
        if current.room in room_map.valid_rooms and current.room is not source:
            cost = len(current.path)
            path_costs.update({current.room: cost})
        
        #Then add the neighbors to the popped node to the frontier
        #And add the room we were in to the explored set
        for room in room_map.neighbor_map[current.room]:
            if room not in explored:
                frontier.append(Node(room, room_map, current.path + [room]))
        explored.add(current.room)

    return path_costs
    #Returns a dict containing the destination rooms and costs for all valid rooms given the source room provided

def part1():
    with open("test_input.txt") as file:

        lines = file.readlines()

        valve_values = {}
        neighbor_map = {}

        for line in lines:
            tunnels = set()
            valve = line.split(" ", 2)[1]
            flow_rate = int(line.split("=")[1].split(";")[0])
            neighbors = line.split("valve")[1].split()
            if neighbors[0] == "s":
                neighbors.remove("s")
            [tunnels.add(tunnel.rstrip(",")) for tunnel in neighbors]
            if flow_rate != 0:
                valve_values.update({valve: flow_rate})
            neighbor_map.update({valve: tunnels})

        time = 30
        start_room = "AA"
        openers = [Opener(start_room, "Me")]

        #neighbor_map is going to be a dict containing each room as a key, and its neighboring rooms as values
        valid_rooms = set(valve_values.keys())
        valid_rooms.add(start_room)    

        room_map = RoomMap(neighbor_map, valid_rooms)
        
        #iterates over every valid source room, using bfs to generate a dict of the destination rooms and their costs for the given source room
        #Final result is a dict of dicts, action_cost, which can be used to lookup the action cost of going from one room to another by action_cost[source][destination]
        action_cost = {}
        for room in room_map.valid_rooms:
            action_cost.update({room: breadth_first_search(room, room_map)})

        possible_moves = valid_rooms
        possible_moves.remove(start_room)

        solution = Solution(possible_moves, time, openers, valve_values, action_cost)

        print(solution.anneal())



def main():
    part1()


main()

#Credit for the annealing framework
# https://towardsdatascience.com/optimization-techniques-simulated-annealing-d6a4785a1de7
