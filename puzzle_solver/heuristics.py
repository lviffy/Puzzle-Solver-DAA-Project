"""
Heuristic functions for the 8-puzzle problem.
"""

from typing import Dict, Tuple
from .puzzle_state import PuzzleState


class Heuristic:
    """Base class for heuristics."""
    
    def compute(self, state: PuzzleState) -> int:
        """Compute heuristic value for a given state."""
        raise NotImplementedError
    
    def get_name(self) -> str:
        """Get heuristic name."""
        raise NotImplementedError


class H1_Trivial(Heuristic):
    """H1: Trivial heuristic (h = 0). Baseline uninformed search."""
    
    def compute(self, state: PuzzleState) -> int:
        """Always returns 0."""
        return 0
    
    def get_name(self) -> str:
        return "H1: Trivial (h=0)"


class H2_MisplacedTiles(Heuristic):
    """H2: Misplaced Tiles heuristic. Counts tiles not in correct position."""
    
    def compute(self, state: PuzzleState) -> int:
        """
        Count the number of misplaced tiles (not in goal position).
        Empty space (0) is ignored.
        
        Returns:
            Number of misplaced tiles (0-8)
        """
        misplaced = 0
        for i in range(9):
            if state.state[i] != PuzzleState.GOAL_STATE[i] and state.state[i] != 0:
                misplaced += 1
        return misplaced
    
    def get_name(self) -> str:
        return "H2: Misplaced Tiles"


class H3_Manhattan(Heuristic):
    """H3: Manhattan Distance heuristic. Sum of distances of each tile to goal position."""
    
    def compute(self, state: PuzzleState) -> int:
        """
        Calculate sum of Manhattan distances.
        Manhattan distance from position a to position b = |row_a - row_b| + |col_a - col_b|
        
        Returns:
            Sum of Manhattan distances for all tiles
        """
        distance = 0
        for i in range(9):
            tile = state.state[i]
            if tile == 0:  # Skip empty space
                continue
            
            # Current position of tile
            current_row = i // 3
            current_col = i % 3
            
            # Goal position of tile
            goal_pos = tile
            goal_row = goal_pos // 3
            goal_col = goal_pos % 3
            
            # Manhattan distance
            distance += abs(current_row - goal_row) + abs(current_col - goal_col)
        
        return distance
    
    def get_name(self) -> str:
        return "H3: Manhattan Distance"


class H4_LinearConflict(Heuristic):
    """
    H4: Linear Conflict heuristic.
    Manhattan distance + 2 × number of linear conflicts.
    A linear conflict occurs when two tiles are in the same row or column
    as their goal position, but are in reverse order.
    """
    
    def compute(self, state: PuzzleState) -> int:
        """
        Calculate Manhattan distance + 2 × linear conflicts.
        
        Returns:
            Heuristic value combining Manhattan distance and linear conflicts
        """
        # First, get Manhattan distance
        manhattan = H3_Manhattan().compute(state)
        
        # Count linear conflicts
        conflicts = self._count_linear_conflicts(state)
        
        return manhattan + 2 * conflicts
    
    def _count_linear_conflicts(self, state: PuzzleState) -> int:
        """
        Count the number of linear conflicts.
        A linear conflict is when two tiles are in the same row or column as their goal
        and are in reverse order relative to their goal positions.
        
        Args:
            state: PuzzleState to check
        
        Returns:
            Number of linear conflicts
        """
        conflicts = 0
        
        # Check each row
        for row in range(3):
            for i in range(3):
                for j in range(i + 1, 3):
                    pos_i = row * 3 + i
                    pos_j = row * 3 + j
                    
                    tile_i = state.state[pos_i]
                    tile_j = state.state[pos_j]
                    
                    # Skip empty space
                    if tile_i == 0 or tile_j == 0:
                        continue
                    
                    # Check if both tiles belong to this row in goal state
                    goal_row_i = tile_i // 3
                    goal_row_j = tile_j // 3
                    
                    if goal_row_i == row and goal_row_j == row:
                        # Both belong to this row
                        goal_col_i = tile_i % 3
                        goal_col_j = tile_j % 3
                        
                        # Check if they're in reverse order
                        if goal_col_i > goal_col_j:
                            conflicts += 1
        
        # Check each column
        for col in range(3):
            for i in range(3):
                for j in range(i + 1, 3):
                    pos_i = i * 3 + col
                    pos_j = j * 3 + col
                    
                    tile_i = state.state[pos_i]
                    tile_j = state.state[pos_j]
                    
                    # Skip empty space
                    if tile_i == 0 or tile_j == 0:
                        continue
                    
                    # Check if both tiles belong to this column in goal state
                    goal_col_i = tile_i % 3
                    goal_col_j = tile_j % 3
                    
                    if goal_col_i == col and goal_col_j == col:
                        # Both belong to this column
                        goal_row_i = tile_i // 3
                        goal_row_j = tile_j // 3
                        
                        # Check if they're in reverse order
                        if goal_row_i > goal_row_j:
                            conflicts += 1
        
        return conflicts
    
    def get_name(self) -> str:
        return "H4: Linear Conflict"


# Singleton instances for easy access
h1 = H1_Trivial()
h2 = H2_MisplacedTiles()
h3 = H3_Manhattan()
h4 = H4_LinearConflict()

HEURISTICS = [h1, h2, h3, h4]
