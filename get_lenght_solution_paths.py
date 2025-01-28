# Description: This script is used to check the length of the solutions found by the different search algorithms.
    
import json

tiny_map_breadth_first = json.load(open('solutions/solution_tiny_map_breadth_first.json'))
print(f"Tiny map, Breadth first search, solution length: {len(tiny_map_breadth_first[1])}")

tiny_map_depth_first = json.load(open('solutions/solution_tiny_map_depth_first.json'))
print(f"Tiny map, Depth first search, solution length: {len(tiny_map_depth_first[1])}")

tiny_map_greedy = json.load(open('solutions/solution_tiny_map_greedy.json'))
print(f"Tiny map, Greedy search, solution length: {len(tiny_map_greedy[1])}")

tiny_map_a_star = json.load(open('solutions/solution_tiny_map_a_star.json'))
print(f"Tiny map, A* search, solution length: {len(tiny_map_a_star[1])}")

large_map_greedy = json.load(open('solutions/solution_large_map_greedy.json'))
print(f"Large map, Greedy search, solution length: {len(large_map_greedy[1])}")