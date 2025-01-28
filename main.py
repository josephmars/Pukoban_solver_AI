import os
import json

from game import Game, map2objects
from search import (
    breadth_first_search,
    depth_first_search,
    greedy_best_search,
    a_star_search,
    get_solution_path
)

def run_search_algorithms(game, blanks, max_time, map_size):
    """
    Runs various search algorithms on the provided game and saves the solutions.

    Args:
        game (Game): The game instance.
        blanks (list): List of blank objects in the game.
        max_time (int): Maximum time to run the algorithm (in minutes).
        map_size (str): Size of the map ('tiny', 'medium', 'large').
    """
    algorithms = {
        'greedy': greedy_best_search,
        'a_star': a_star_search,
        'breadth_first': breadth_first_search,
        'depth_first': depth_first_search
    }

    for name, algorithm in algorithms.items():
        print(f"Running {name.replace('_', ' ').title()} for {map_size} map...")
        result = algorithm(game, blanks, max_time)
        solution = get_solution_path(result)
        filename = f'solutions/solution_{map_size}_map_{name}.json'
        with open(filename, 'w') as outfile:
            json.dump(solution, outfile)
        print(f"Solution saved to {filename}\n")

def main():
    # Create solutions directory if it doesn't exist
    os.makedirs('solutions', exist_ok=True)

    # Define maps
    tiny_map = """OOOOOO
O BR O
O BO O
OO   O
OOSS O
OOOOOO"""

    medium_map = """OOOOOOO
OS   SO
O BBB O
O BRB O
OSBBBSO
OSS SSO
OOOOOOO"""

    large_map = """OOOOOOOOO
OO  OOOOO
OOB OOOOO
O B B   O
ORSSSSSO
O BS   OO
OOBO OOOO
OO   OOOO
OOOOOOOOO"""

    # Parse maps into game objects
    objects_tiny_map = map2objects(tiny_map)
    state_tiny_map = objects_tiny_map["state"]
    blanks_tiny_map = objects_tiny_map["blanks"]

    objects_medium_map = map2objects(medium_map)
    state_medium_map = objects_medium_map["state"]
    blanks_medium_map = objects_medium_map["blanks"]

    objects_large_map = map2objects(large_map)
    state_large_map = objects_large_map["state"]
    blanks_large_map = objects_large_map["blanks"]

    # Initialize games with parsed states and blanks
    game_tiny_map = Game(state_tiny_map, blanks_tiny_map)
    max_time_tiny_map = 5  # in minutes

    game_medium_map = Game(state_medium_map, blanks_medium_map)
    max_time_medium_map = 5 * 60  # in minutes

    game_large_map = Game(state_large_map, blanks_large_map)
    max_time_large_map = 4 * 60  # in minutes

    # Run search algorithms for each map size
    run_search_algorithms(game_tiny_map, blanks_tiny_map, max_time_tiny_map, 'tiny')
    run_search_algorithms(game_medium_map, blanks_medium_map, max_time_medium_map, 'medium')
    run_search_algorithms(game_large_map, blanks_large_map, max_time_large_map, 'large')

if __name__ == "__main__":
    main() 