# Heuristic Functions - Technical Guide

## Overview

This document provides detailed technical information about the four heuristic functions implemented in this project.

## H1: Trivial Heuristic

### Definition
```
h₁(n) = 0  for all n
```

### Description
The trivial heuristic always returns 0, providing no guidance to the search algorithm. This is equivalent to uninformed search (specifically, Uniform Cost Search for this problem).

### Implementation
```python
def compute(self, state: PuzzleState) -> int:
    return 0
```

### Complexity
- **Time**: O(1)
- **Space**: O(1)

### Properties
- **Admissible**: Yes (0 ≤ actual cost)
- **Consistent**: Yes (0 ≤ cost(s,s') + h(s'))
- **Informedness**: Minimal (no guidance)

### Expected Behavior
- Explores many nodes (often 10,000+)
- Very slow execution time
- Used as baseline for comparison
- Essentially breadth-first search by cost

## H2: Misplaced Tiles Heuristic

### Definition
```
h₂(n) = number of tiles not in correct position (excluding blank)
```

### Description
Counts how many tiles are in the wrong position compared to the goal state. The blank (0) is ignored since it can be in any position.

### Implementation
```python
def compute(self, state: PuzzleState) -> int:
    misplaced = 0
    for i in range(9):
        if state.state[i] != PuzzleState.GOAL_STATE[i] and state.state[i] != 0:
            misplaced += 1
    return misplaced
```

### Example
```
Current:  Goal:
1 2 3     1 2 3
4 0 5  vs 4 5 6
7 8 6     7 8 0

Misplaced: 2 tiles (5 and 6 are in wrong positions)
h₂ = 2
```

### Complexity
- **Time**: O(9) = O(1)
- **Space**: O(1)

### Properties
- **Admissible**: Yes (h₂ ≤ actual moves needed)
- **Consistent**: Yes
- **Informedness**: Weak (lower bound is loose)

### Range
- Minimum: 0 (at goal state)
- Maximum: 8 (all tiles misplaced)

### Performance Notes
- ~10-100× faster than H1
- Still explores thousands of nodes
- Very simple and fast to compute
- Good for teaching purposes

## H3: Manhattan Distance Heuristic

### Definition
```
h₃(n) = Σ(|current_row - goal_row| + |current_col - goal_col|) 
        for each tile (excluding blank)
```

### Description
Sums the Manhattan distances (taxicab distances) of all tiles from their goal positions. Manhattan distance is the number of steps needed to reach the goal if movement was only horizontal or vertical (no diagonals).

### Implementation
```python
def compute(self, state: PuzzleState) -> int:
    distance = 0
    for i in range(9):
        tile = state.state[i]
        if tile == 0:  # Skip empty space
            continue
        
        # Current position
        current_row = i // 3
        current_col = i % 3
        
        # Goal position
        goal_pos = tile
        goal_row = goal_pos // 3
        goal_col = goal_pos % 3
        
        # Manhattan distance
        distance += abs(current_row - goal_row) + abs(current_col - goal_col)
    
    return distance
```

### Example
```
Current:  Goal:
1 2 3     1 2 3
4 0 5  vs 4 5 6
7 8 6     7 8 0

Tile distances:
- Tile 5: at (1,2), goal (1,2) → distance = 0
- Tile 6: at (2,2), goal (1,2) → distance = 1
- Tile 0 (blank): ignored

h₃ = 0 + 1 = 1
```

### Complexity
- **Time**: O(18) = O(1)
- **Space**: O(1)

### Properties
- **Admissible**: Yes (actual moves ≥ Manhattan distance)
- **Consistent**: Yes
- **Informedness**: Good (much tighter than H2)

### Range
- Minimum: 0 (at goal state)
- Maximum: 24 (worst case when all tiles are opposite)

### Why It Works
Manhattan distance is an underestimate because:
1. Actual moves must overcome linear conflicts
2. Tiles can block each other
3. Movement is constrained to adjacent swaps with blank

### Performance Notes
- **100-1000× faster** than H1
- Standard heuristic for 8-puzzle
- Excellent balance of computation cost vs. effectiveness
- Commonly used in AI textbooks

## H4: Linear Conflict Heuristic

### Definition
```
h₄(n) = h₃(n) + 2 × LC(n)

where LC(n) = number of linear conflicts
```

A **linear conflict** occurs when:
1. Two tiles are in the same row or column as their goal
2. They are in reverse order relative to their goal positions

### Rationale
Linear conflicts represent wasted moves. When two tiles must swap positions and they're in the same row/column as their goals, at least 2 extra moves are needed to resolve the conflict. The "2×" multiplier accounts for this.

### Implementation
```python
def compute(self, state: PuzzleState) -> int:
    manhattan = H3_Manhattan().compute(state)
    conflicts = self._count_linear_conflicts(state)
    return manhattan + 2 * conflicts

def _count_linear_conflicts(self, state: PuzzleState) -> int:
    conflicts = 0
    
    # Check rows for conflicts
    for row in range(3):
        for i in range(3):
            for j in range(i + 1, 3):
                pos_i = row * 3 + i
                pos_j = row * 3 + j
                
                tile_i = state.state[pos_i]
                tile_j = state.state[pos_j]
                
                if tile_i == 0 or tile_j == 0:
                    continue
                
                # Check if both belong to this row in goal
                goal_row_i = tile_i // 3
                goal_row_j = tile_j // 3
                
                if goal_row_i == row and goal_row_j == row:
                    # Check if in reverse order
                    goal_col_i = tile_i % 3
                    goal_col_j = tile_j % 3
                    
                    if goal_col_i > goal_col_j:
                        conflicts += 1
    
    # Same check for columns...
    return conflicts
```

### Example
```
Current:  Goal:
1 2 3     1 2 3
4 5 6  vs 4 5 6
8 7 0     7 8 0

Tiles 7 and 8 are in the same row (row 2) as their goal.
In current state: 8 is at column 0, 7 is at column 1
In goal state: 7 should be at column 0, 8 at column 1
They are in reverse order → 1 linear conflict

h₃ = 2 (7 needs 1 move, 8 needs 1 move)
LC = 1 (one linear conflict)
h₄ = 2 + 2×1 = 4
```

### Complexity
- **Time**: O(9²) = O(1) 
- **Space**: O(1)

### Properties
- **Admissible**: Yes (still underestimates actual cost)
- **Consistent**: Yes
- **Informedness**: Excellent (tightest practical bound)

### Performance Notes
- **1000-10000× faster** than H1
- More expensive to compute than H3
- But still fast (only 9² constant operations)
- Worthwhile tradeoff for dramatic speedup

## Comparison Summary

| Property | H1 | H2 | H3 | H4 |
|----------|----|----|----|----|
| **Definition** | Always 0 | Misplaced tiles | Manhattan | Manhattan + Conflicts |
| **Computation Time** | O(1) | O(1) | O(1) | O(1) |
| **Admissible** | ✓ | ✓ | ✓ | ✓ |
| **Consistent** | ✓ | ✓ | ✓ | ✓ |
| **Lower Bound Tightness** | Worst | Weak | Good | Best |
| **Search Efficiency** | 1× | 10-100× | 100-1000× | 1000-10000× |
| **Puzzle Solving Time (avg)** | 1-10s | 0.1-1s | 0.01-0.1s | 0.001-0.05s |

## Theoretical Foundation

### Admissibility
A heuristic h is **admissible** if:
```
0 ≤ h(n) ≤ actual_cost(n)
```

All four heuristics are admissible because:
- H1: 0 ≤ any actual cost ✓
- H2: Misplaced tiles ≤ actual moves (can move 1 tile per move) ✓
- H3: Manhattan ≤ actual moves (can't move tile in fewer moves) ✓
- H4: Manhattan + conflicts ≤ actual moves (conflicts add 2 moves each) ✓

### Consistency
A heuristic h is **consistent** if:
```
h(n) ≤ cost(n,n') + h(n')
```

All four heuristics are consistent because they satisfy the triangle inequality.

### Dominance
An admissible heuristic h2 **dominates** h1 if:
```
h1(n) ≤ h2(n) for all n
```

In our case: **H1 ≺ H2 ≺ H3 ≺ H4**

H4 dominates all others, providing the most guidance while remaining admissible.

## Key Insights

1. **Better heuristics = Exponential speedup**
   - Not just 2× or 10× faster, but 100-1000× faster!

2. **Computation cost is negligible**
   - All four heuristics compute in O(1) time
   - The bottleneck is search space, not heuristic evaluation

3. **Tightness matters**
   - The closer h(n) to actual cost, the better the pruning
   - This is why H4 is so effective

4. **Tradeoff: Admissibility vs. Effectiveness**
   - Non-admissible heuristics (not used here) could be faster
   - But admissible guarantees optimal solutions

## References

- Nilsson, N. J. (1971). Problem-Solving Methods in Artificial Intelligence
- Korf, R. E. (1985). Depth-First Iterative-Deepening: An Optimal Admissible Tree Search
- Pearl, J. (1984). Heuristics: Intelligent Search Strategies
