# Pukoban Puzzle Solver

## Introduction

The **Pukoban Puzzle Solver** is an advanced AI-driven solution designed to tackle the challenging Pukoban puzzle game, a variant of the classic Sokoban game. The solver employs various search algorithms to efficiently determine the optimal sequence of moves required to navigate boxes into their designated storage locations using a robot. 

<p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/4/4b/Sokoban_ani.gif" width="60%"/>
  <br>
  <em>A Sokoban puzzle being solved</em>
</p>

## Project Overview

The solver is implemented in Python and leverages several search strategies to explore possible states of the puzzle. The key components of the project include:

- **Game Representation:** The puzzle is modeled as a grid board with distinct characters representing obstacles, walls, the robot, boxes, storage locations, and open spaces. Each game state is encapsulated in a dictionary detailing the positions of the robot, boxes, and storage areas.

- **Search Algorithms:** Four primary search algorithms are implemented to solve the puzzle:
  - **Breadth-First Search (BFS)**
  - **Depth-First Search (DFS)**
  - **Greedy Best-First Search**
  - **A-Star Search**

- **Solution Path Extraction:** After executing the search algorithms, the solution path can be extracted, providing the sequence of moves along with performance metrics.

## Solutions and Analysis

### Solution Files

All solutions and their corresponding analyses are stored in the `solutions/` directory in JSON format:

- `solution_tiny_map_<algorithm>.json`
- `solution_medium_map_<algorithm>.json`
- `solution_large_map_<algorithm>.json`

If a solution is not found within the specified time frame, the output will indicate the reason, such as `{"time": Computing time, "reason": "Time exceeded"}`.

### Search Algorithm Performance

The following tables summarize the performance of each search algorithm across different map sizes:

#### Table 1. Solution Length (Number of States)

| Search Algorithm   | Tiny Map | Medium Map | Large Map |
|--------------------|----------|------------|-----------|
| Breadth-First Search (BFS) | 24       | -          | -         |
| Depth-First Search (DFS)    | 340      | -          | -         |
| Greedy Best-First Search    | 42       | 69         | -         |
| A* Search                   | 24       | -          | -         |

#### Table 2. Computation Time (Minutes)

| Search Algorithm   | Tiny Map | Medium Map | Large Map |
|--------------------|----------|------------|-----------|
| Breadth-First Search (BFS) | 0.0050   | -          | -         |
| Depth-First Search (DFS)    | 0.0023   | -          | -         |
| Greedy Best-First Search    | 0.0006   | 0.0034     | -         |
| A* Search                   | 0.0032   | -          | -         |

### Insights

- **Optimal Solutions:** Both **Breadth-First Search (BFS)** and **A\*** consistently provide optimal solutions for the tiny map, ensuring the minimal number of moves required to solve the puzzle.

- **Efficiency:** **Greedy Best-First Search** demonstrated the fastest computation times, especially in smaller grids, by aggressively pursuing the most promising moves based on the Manhattan distance heuristic.

- **Exploration Strategy:** **Depth-First Search (DFS)**, while effective, tends to explore deeper paths first, resulting in longer solution paths due to its exhaustive exploration approach.

- **Map Size Impact:** No solutions were found for the medium map within the allotted time, and only the greedy search succeeded in solving the large map, highlighting the increased complexity and computational demands of larger puzzles.

## How to Use the Solver

1. **Setup:**
   - Ensure you have Python installed on your system.
   - Install the required dependencies using `pip`:
     ```bash
     pip install -r requirements.txt
     ```

2. **Running the Solver:**
   - Execute the `main.py` script to run the solver on predefined maps:
     ```bash
     python main.py
     ```

3. **Understanding the Output:**
   - Solutions for each map size and algorithm are saved in the `solutions/` directory in JSON format.
   - Analyze the solution paths and performance metrics using the provided analysis tools or by reviewing the JSON files directly.

## Additional Notes

- **Heuristic Function:** The solver utilizes the Manhattan distance heuristic in both the **Greedy Best-First Search** and **A\* Search** algorithms. This heuristic calculates the sum of the absolute differences in coordinates between each box and its nearest storage location, guiding the search towards the most promising moves.

- **Extensibility:** The project is designed with modularity in mind, allowing for the easy addition of new search algorithms or enhancements to existing ones.

- **Performance Optimization:** Future iterations could explore parallel processing or more sophisticated heuristics to improve solver efficiency, especially for more complex and larger puzzle maps.

