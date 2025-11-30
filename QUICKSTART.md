# Quick Start Guide

## Installation & Setup

No additional dependencies needed beyond Python 3.6+. For visualization, install matplotlib:

```bash
pip install matplotlib numpy
```

## Running the Project

### Option 1: Interactive Menu (Recommended)

```bash
cd /home/luffy/class/DAA\ CLA2
python main.py
```

This provides an interactive menu to:
1. Run validation tests
2. Run experiments (50 or 100 puzzles)
3. Generate visualizations
4. Exit

### Option 2: Direct Experiment Execution

```bash
cd /home/luffy/class/DAA\ CLA2/puzzle_solver
python run_experiment.py
```

This automatically runs 50 puzzles and saves results.

### Option 3: Run Tests Only

```bash
cd /home/luffy/class/DAA\ CLA2/puzzle_solver
python test.py
```

## What Gets Generated

After running experiments, you'll get:

1. **results.json** - Raw data with all metrics for every puzzle
2. **experiment_results.png** - Three visualization plots
3. **report.txt** - Complete analysis with observations

## Example Output

Running a quick test gives:

```
==================================================
Running Validation Tests
==================================================
✓ PuzzleState tests passed
✓ Heuristic tests passed  
✓ Generated 5 unique solvable puzzles
✓ Solved 1-move puzzle in 0.0000s
  Nodes expanded: 4
  Average ratio: 1.2500
✓ Goal state handled correctly

==================================================
✓ All tests passed!
==================================================
```

## Key Files

**Source Code** (in `puzzle_solver/`):
- `puzzle_state.py` - Core puzzle representation
- `heuristics.py` - All 4 heuristic implementations
- `branch_and_bound.py` - B&B search algorithm
- `generator.py` - Puzzle generation
- `run_experiment.py` - Experiment orchestration
- `analyze_results.py` - Visualization & reporting
- `test.py` - Validation tests

**Documentation**:
- `README.md` - Full technical documentation
- `main.py` - Interactive menu system

## Understanding the Results

### Key Metrics

1. **Execution Time**: How long the solver takes
   - Better heuristics = faster solving
   
2. **Average Ratio**: Average heuristic value / optimal solution cost
   - Ratio closer to 1 = tighter lower bound = more efficient search
   - Ratio >> 1 = loose bound = explores many nodes

3. **Nodes Expanded**: How many states explored
   - Shows effectiveness of pruning
   - Better heuristics prune more

### Expected Performance Scaling

Typical results on 50 medium-difficulty puzzles:

| Heuristic | Relative Time | Ratio | Speedup |
|-----------|--------------|-------|---------|
| H1 (h=0) | 100× | >5 | 1× |
| H2 (Misplaced) | 10× | 1-2 | 10× |
| H3 (Manhattan) | 1× | 0.5-1 | 100× |
| H4 (Conflict) | 0.5× | 0.3-0.5 | 200× |

H4 is typically **100-200× faster** than H1!

## Advanced Usage

### Solving a Single Puzzle

```python
from puzzle_solver.puzzle_state import PuzzleState
from puzzle_solver.branch_and_bound import BranchAndBoundSolver
from puzzle_solver.heuristics import h3

# Create puzzle (0 = empty space)
puzzle = PuzzleState((1, 2, 3, 4, 0, 5, 6, 7, 8))

# Solve using Manhattan distance heuristic
solver = BranchAndBoundSolver(h3)
solution, stats = solver.solve(puzzle)

if stats.solution_found:
    print(f"Found solution with {stats.solution_length} moves!")
    print(f"Expanded {stats.nodes_expanded} nodes")
    print(f"Time: {stats.execution_time:.4f}s")
else:
    print("Puzzle is unsolvable")
```

### Batch Processing

```python
from puzzle_solver.generator import PuzzleGenerator
from puzzle_solver.branch_and_bound import BranchAndBoundSolver
from puzzle_solver.heuristics import h4

# Generate 20 puzzles
puzzles = PuzzleGenerator.generate_batch(20)

# Solve all with best heuristic
solver = BranchAndBoundSolver(h4)
results = solver.solve_multiple(puzzles)

# Analyze results
for solution, stats in results:
    print(f"Time: {stats.execution_time:.4f}s, Nodes: {stats.nodes_expanded}")
```

## Troubleshooting

**"results.json not found"**
- Run experiments first using `python run_experiment.py`

**Slow performance on H1**
- This is expected! H1 has no heuristic guidance
- Try with fewer puzzles or shorter max search time if needed

**Plot not generated**
- Ensure matplotlib is installed: `pip install matplotlib`
- Check that results.json exists

## Project Structure Overview

```
DAA CLA2/
├── main.py                 # Interactive menu
├── README.md              # Full documentation  
├── QUICKSTART.md          # This file
├── puzzle_solver/         # Main package
│   ├── __init__.py
│   ├── puzzle_state.py    # Puzzle representation
│   ├── heuristics.py      # H1, H2, H3, H4
│   ├── branch_and_bound.py # Search algorithm
│   ├── generator.py       # Puzzle generator
│   ├── run_experiment.py  # Run experiments
│   ├── analyze_results.py # Visualizations
│   └── test.py            # Unit tests
├── results.json           # Generated after experiments
├── experiment_results.png # Generated visualization
└── report.txt             # Generated analysis report
```

## Time Estimates

- **Validation tests**: < 1 second
- **50-puzzle experiment**: 30 seconds - 2 minutes
- **100-puzzle experiment**: 2-5 minutes  
- **Visualization generation**: 1 second

## For Assignment Submission

The project provides:

1. ✓ **Code Implementation**
   - All 4 heuristics (H1-H4)
   - Branch & Bound algorithm
   - Solvability checking
   - Statistics collection

2. ✓ **Experiments**
   - Multiple puzzle instances
   - Performance measurements
   - Statistical analysis

3. ✓ **Visualizations**
   - Time vs heuristic
   - Ratio vs heuristic
   - Nodes vs heuristic

4. ✓ **Documentation**
   - README with full explanations
   - Inline code comments
   - Analysis report

## Performance Optimization Tips

For very large experiments:

1. Modify `run_experiment.py` line `runner = ExperimentRunner(num_puzzles=50)` to higher value
2. H1 can be slow on hard puzzles - consider using a timeout mechanism
3. Linear Conflict (H4) is most expensive to compute but worth it for efficiency

## Getting Help

Refer to:
- `README.md` - Technical documentation
- Inline code comments in `*.py` files
- `report.txt` - Analysis with insights
- `test.py` - Working examples
