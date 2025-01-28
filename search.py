# Functions for searching algorithms
import copy

from game import Game, map2objects

# 1. Breadth First Search algorithm
def breadth_first_search(initial_game, blanks, max_time):
    """Breadth First Search algorithm
        Parameters:
            game (object): Game object
            max_time (int): Maximum time to run the algorithm (in minutes)
        Returns:
            output (dict): Dictionary with the ids, parent ids and states of the visited nodes
    """
    from time import time
    start = time()
    compute_time = 0
    current_state = copy.deepcopy(initial_game.get_current_state())
    fringe = [[0, -1, current_state]] # [state id, parent id, state]
    visited = []
    ids = []
    parent_ids = []
    next_id = 1
    while fringe and compute_time < max_time*60:
        state_id, parent_id, state = fringe.pop(0)
            
        if state not in visited:
            visited.append(state)
            ids.append(state_id)
            parent_ids.append(parent_id)
            iter_game = Game(state, blanks)
            
            if iter_game.check_win():
                total_time = (time() - start) / 60
                print(f"Solution found in {total_time} minutes")
                output = {"time": total_time, "ids" : ids, "parent_ids": parent_ids, "states" : visited}
                return output
            else:
                current_state = iter_game.get_current_state()
                next_states = iter_game.successor_function()
                for s in next_states:
                    fringe.append([next_id, state_id, s])
                    next_id = next_id + 1
                    
            compute_time = time() - start
            
    if not iter_game.check_win():
        if (compute_time < max_time*60):
            print("No solution found")
            return {"time": compute_time, "reason": "No solution found"}
        else:
            print("Time exceeded")
            return {"time": compute_time, "reason": "Time exceeded"}

#2. Depth First Search algorithm
def depth_first_search(initial_game, blanks, max_time):
    """Depth First Search algorithm
        Parameters:
            game (object): Game object
            max_time (int): Maximum time to run the algorithm (in minutes)
        Returns:
            output (dict): Dictionary with the ids, parent ids and states of the visited nodes
    """
    from time import time
    start = time()
    compute_time = 0
    current_state = copy.deepcopy(initial_game.get_current_state())
    fringe = [[0, -1, current_state]] # [state id, parent id, state]
    visited = []
    ids = []
    parent_ids = []
    next_id = 1
    
    while fringe and compute_time < max_time*60:
        state_id, parent_id, state = fringe.pop(0)
        
        if state not in visited:
            visited.append(state)
            ids.append(state_id)
            parent_ids.append(parent_id)
            iter_game = Game(state, blanks)
            
            if iter_game.check_win():
                total_time = (time() - start) / 60
                print(f"Solution found in {total_time} minutes")
                output = {"time": total_time, "ids" : ids, "parent_ids": parent_ids, "states" : visited}
                return output
            else:
                current_state = iter_game.get_current_state()
                next_states = iter_game.successor_function()
                for s in next_states:
                    # Add the next states to the beginning of the fringe
                    fringe.insert(0, [next_id, state_id, s])
                    next_id = next_id + 1
            compute_time = time() - start
            
    if not iter_game.check_win():
        if (compute_time < max_time*60):
            print("No solution found")
            return {"time": compute_time, "reason": "No solution found"}
        else:
            print("Time exceeded")
            return {"time": compute_time, "reason": "Time exceeded"}

#3. Greedy Best Search algorithm
def greedy_best_search(initial_game, blanks, max_time):
    """Greedy Best Search algorithm
        Parameters:
            game (object): Game object
            max_time (int): Maximum time to run the algorithm (in minutes)
        Returns:
            output (dict): Dictionary with the ids, parent ids and states of the visited nodes
    """
    from time import time
    start = time()
    compute_time = 0
    current_state = copy.deepcopy(initial_game.get_current_state())
    initial_distance = sum_distances_from_state(current_state)
    fringe = [[initial_distance, 0, -1, current_state]] # [sum of distances, state id, parent id, state]
    visited = []
    ids = []
    parent_ids = []
    next_id = 1
    
    while fringe and  compute_time < max_time*60:
        distance, state_id, parent_id, state = fringe.pop(0)
        
        if state not in visited:
            visited.append(state)
            ids.append(state_id)
            parent_ids.append(parent_id)
            iter_game = Game(state, blanks)
            
            if iter_game.check_win():
                total_time = (time() - start) / 60
                print(f"Solution found in {total_time} minutes")
                output = {"time": total_time, "ids" : ids, "parent_ids": parent_ids, "states" : visited}
                return output
            else:
                current_state = iter_game.get_current_state()
                next_states = iter_game.successor_function()
                for s in next_states:
                    # Add the next states to the fringe
                    distance = sum_distances_from_state(s)
                    fringe.append([distance, next_id, state_id, s])
                    next_id = next_id + 1
                    
                # sort the states by the sum of distances
                fringe.sort()
            compute_time = time() - start
            
    if not iter_game.check_win():
        if (compute_time < max_time*60):
            print("No solution found")
            return {"time": compute_time, "reason": "No solution found"}
        else:
            print("Time exceeded")
            return {"time": compute_time, "reason": "Time exceeded"}

# 4. A* Search algorithm
def a_star_search(initial_game, blanks, max_time):
    """A* Search algorithm
        Parameters:
            game (object): Game object
            max_time (int): Maximum time to run the algorithm (in minutes)
        Returns:
            output (dict): Dictionary with the ids, parent ids and states of the visited nodes
    """
    from time import time
    start = time()
    compute_time = 0
    current_state = copy.deepcopy(initial_game.get_current_state())
    initial_distance = sum_distances_from_state(current_state)
    
    # f(n): total cost
    # f(n)=g(n)+h(n)
    # • g(n): Gives the path cost from the start node to node n
    # • h(n): Heuristic function (Manhattan distance)

    # We store for each node [f(n)=g(n)+h(n), g(n), state id, parent id, state].
    # g(n) is stored since it is historical, but to save memory h(n) is just computed every time we need it.
    fringe = [[initial_distance, 0, 0, -1, current_state]]
    visited = []
    ids = []
    parent_ids = []
    next_id = 1
    

    while fringe and compute_time < max_time*60:
        cost, path_cost, state_id, parent_id, state = fringe.pop(0)
        
        if state not in visited:
            visited.append(state)
            ids.append(state_id)
            parent_ids.append(parent_id)
            iter_game = Game(state, blanks)
            
            if iter_game.check_win():
                total_time = (time() - start) / 60
                print(f"Solution found in {total_time} minutes")
                output = {"time": total_time, "ids" : ids, "parent_ids": parent_ids, "states" : visited}
                return output
            else:
                current_state = iter_game.get_current_state()
                next_states = iter_game.successor_function()
                
                path_cost = path_cost + 1 # We increase the path cost by 1 for the children nodes
                for s in next_states:
                    
                    # Add the next states to the fringe
                    distance = sum_distances_from_state(s)
                    cost = path_cost + distance # cost = f(n)
                    fringe.append([cost, path_cost, next_id, state_id, s])
                    
                    next_id = next_id + 1
                    
                # sort the states by the total cost
                fringe.sort()
            compute_time = time() - start
            
    if not iter_game.check_win():
        if (compute_time < max_time*60):
            print("No solution found")
            return {"time": compute_time, "reason": "No solution found"}
        else:
            print("Time exceeded")
            return {"time": compute_time, "reason": "Time exceeded"}    
    
# 5. Manhatan distance function
def manhattan_distance(point_a, point_b):
    """Manhattan Distance algorithm
        Parameters:
            point_a (tuple): Coordinates of the first point
            point_b (tuple): Coordinates of the second point
        Returns:
            distance (float): Manhattan distance between the two points
    """
    distance = abs(point_a[0] - point_b[0]) + abs(point_a[1] - point_b[1])
    return distance

# 6. Sum of distances from state function
def sum_distances_from_state(state):
    """Computes the sum of the manhattan distances between the boxes and the storages
        Parameters:
            state (dict): Dictionary with the coordinates of the robot, the boxes and the storages
        Returns:
            sum_distance (float): Sum of the manhattan distances between the boxes and the storages
    """
    boxes = state["boxes"]
    storages = state["storages"]
    sum_distance = 0
    
    for box in boxes:
        min_distance = 1000
        for storage in storages:
            distance = manhattan_distance(box, storage)
            if distance < min_distance:
                min_distance = distance
        sum_distance = sum_distance + min_distance
    return sum_distance

# 7. Get solution path from visited list
def get_solution_path(search_output):
    """Returns the solution path from the visited list
        Parameters:
            visited_list (list): List of visited states in the format [(depth,state1), (depth,state2), ...]
        Returns:
            time (float): Time in minutes that the search took
            ids (list): List of ids of the states in the solution path
            parent_ids (list): List of parent ids of the states in the solution path
            states (list): List of states in the solution path
    """
    #Check that a solution was found
    if "states" in search_output.keys():
        states = [search_output["states"][-1]]
        ids = [search_output["ids"][-1]]
        parent_ids = [search_output["parent_ids"][-1]]
        parent = parent_ids[0]
        
        while parent >= 0:
            for i in range(len(search_output["ids"])):
                if search_output["ids"][i] == parent:
                    # Get the parent state, id and its parent id
                    parent_state = search_output["states"][i]
                    states.append(parent_state)
                    
                    parent_id = search_output["ids"][i]
                    ids.append(parent_id)
                    
                    parent_parent_id = search_output["parent_ids"][i]
                    parent_ids.append(parent_parent_id)
                    parent = parent_parent_id
        
        return search_output["time"], ids, parent_ids, states
    else:
        return search_output