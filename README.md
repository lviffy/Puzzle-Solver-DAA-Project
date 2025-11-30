# 8-Puzzle Branch and Bound Solver

A comprehensive implementation of the Branch and Bound algorithm applied to the 8-puzzle problem with multiple lower-bound heuristics.

## Project Structure

```
puzzle_solver/
├── __init__.py                 # Package initialization
├── puzzle_state.py             # Core puzzle state class and operations
├── heuristics.py               # Four heuristic functions (H1-H4)
├── branch_and_bound.py         # Branch and Bound search algorithm
├── generator.py                # Random solvable puzzle generator
├── run_experiment.py           # Main experiment runner
└── analyze_results.py          # Results visualization and analysis
```

## Features

### Four Heuristics Implemented

1. **H1: Trivial Heuristic (h=0)**
   - Baseline uninformed search
   - No guidance, explores all nodes

2. **H2: Misplaced Tiles**
   - Counts tiles not in correct position
   - Simple and fast to compute
   - Better than H1 but still loose

3. **H3: Manhattan Distance**
   - Sum of Manhattan distances to goal
   - Much tighter bound than H2
   - Industry standard for 8-puzzle

4. **H4: Linear Conflict**
   - Manhattan distance + 2 × linear conflicts
   - Tightest bound available
   - Solves puzzles most efficiently

### Key Components

- **PuzzleState**: Represents 3×3 grid with operations
- **BranchAndBoundSolver**: Implements B&B search with statistics collection
- **PuzzleGenerator**: Creates random solvable instances
- **SearchStatistics**: Tracks performance metrics (time, nodes, ratio)

## Usage

### 1. Run Experiments

```bash
cd /home/luffy/class/DAA\ CLA2/puzzle_solver
python run_experiment.py
```

This will:
- Generate 50 random solvable puzzle instances
- Test each puzzle with all 4 heuristics using Branch and Bound
- Collect comprehensive statistics
- Print summary and detailed results
- Save results to `results.json`

### 2. Generate Visualizations and Report

```bash
python analyze_results.py
```

This will:
- Create `experiment_results.png` with three plots:
  - Average Execution Time vs Heuristic
  - Average Ratio (Lower Bound / Optimal Cost) vs Heuristic  
  - Average Nodes Expanded vs Heuristic
- Generate `report.txt` with detailed analysis

### 3. Use as a Library

```python
from puzzle_solver.puzzle_state import PuzzleState
from puzzle_solver.branch_and_bound import BranchAndBoundSolver
from puzzle_solver.heuristics import h3  # Manhattan distance

# Create a puzzle
puzzle = PuzzleState((1, 0, 2, 3, 4, 5, 6, 7, 8))

# Solve it
solver = BranchAndBoundSolver(h3)
solution, stats = solver.solve(puzzle)

# Check results
if stats.solution_found:
    print(f"Solution found in {stats.solution_length} moves")
    print(f"Expanded {stats.nodes_expanded} nodes")
    print(f"Execution time: {stats.execution_time:.4f}s")
```

## Algorithm Details

### Branch and Bound Search

The algorithm expands nodes in order of f(n) = g(n) + h(n), where:
- g(n) = cost from initial state to n
- h(n) = heuristic lower bound from n to goal

**Pruning Strategy**:
- If g(n) + h(n) ≥ best_solution_found, skip this node
- This dramatically reduces the search space

### Solvability Check

The solver uses the inversion count property:
- A permutation is solvable if it has an even number of inversions
- An inversion is when a larger number appears before a smaller number
- This prevents trying to solve unsolvable puzzle configurations

## Expected Results

When running the experiment with 50 puzzles, expect:

| Heuristic | Avg Time (s) | Avg Ratio | Avg Nodes |
|-----------|-------------|-----------|-----------|
| H1 (h=0) | ~0.5-2.0 | >>1.0 | 10000+ |
| H2 (Misplaced) | ~0.1-0.5 | 0.8-1.2 | 1000-5000 |
| H3 (Manhattan) | ~0.01-0.1 | 0.5-0.8 | 100-1000 |
| H4 (Linear Conflict) | ~0.005-0.05 | 0.4-0.7 | 50-500 |

**Key Observations**:
- Better heuristics dramatically reduce search time
- The ratio shows how tight the lower bound is
- H4 typically solves puzzles 50-100× faster than H1

## Metrics Collected

For each puzzle instance, the solver collects:
- `solution_found`: Whether optimal solution was found
- `solution_length`: Number of moves in solution
- `nodes_expanded`: Total nodes expanded during search
- `optimal_cost`: Cost of optimal solution (always = solution_length)
- `execution_time`: Wall clock time in seconds
- `average_lower_bound`: Average h(n) value computed
- `ratio`: average_lower_bound / optimal_cost

## Files Generated

After running experiments:

1. **results.json**: Raw experimental data for all puzzles and heuristics
2. **experiment_results.png**: Visualization with 3 plots
3. **report.txt**: Detailed analysis and observations

## Complexity Analysis

**Time Complexity per Puzzle**:
- H1: O(b^d) where b ≈ 3 (branching factor), d = optimal depth
- H3, H4: Much smaller search space due to better pruning

**Space Complexity**:
- O(number of nodes in search tree)

**Heuristic Computation**:
- H1: O(1)
- H2: O(9)
- H3: O(18)
- H4: O(18) + linear conflict checking

## References

This implementation is based on:
- Branch and Bound search algorithms
- Admissible heuristics for state space search
- The 8-puzzle problem from classical AI

Key papers:
- Nilsson, N. J. (1971). "Problem-solving methods in artificial intelligence"
- Korf, R. E. (1985). "Depth-first iterative-deepening"

## Author

Developed for Design and Analysis of Algorithms (DAA) Course
