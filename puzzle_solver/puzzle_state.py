"""
Core puzzle state and operations for the 8-puzzle problem.
"""

from typing import List, Tuple, Set
import copy


class PuzzleState:
    """Represents an 8-puzzle state with a 3x3 grid."""
    
    GOAL_STATE = (0, 1, 2, 3, 4, 5, 6, 7, 8)
    
    def __init__(self, state: Tuple[int, ...] = None):
        """
        Initialize puzzle state.
        
        Args:
            state: tuple of 9 integers (0-8), where 0 represents the empty space
                   If None, initializes to GOAL_STATE
        """
        if state is None:
            self.state = self.GOAL_STATE
        else:
            self.state = tuple(state)
        
        # Find position of empty space (0)
        self.empty_pos = self.state.index(0)
    
    def __hash__(self):
        """Make state hashable for use in sets and dicts."""
        return hash(self.state)
    
    def __eq__(self, other):
        """Check equality of two states."""
        return self.state == other.state if isinstance(other, PuzzleState) else False
    
    def __repr__(self):
        """String representation of the puzzle."""
        result = ""
        for i in range(3):
            result += f"{self.state[i*3:(i+1)*3]}\n"
        return result
    
    def is_goal(self) -> bool:
        """Check if this is the goal state."""
        return self.state == self.GOAL_STATE
    
    def get_neighbors(self) -> List['PuzzleState']:
        """
        Generate all valid neighboring states (one move away).
        
        Returns:
            List of neighboring PuzzleState objects
        """
        neighbors = []
        empty = self.empty_pos
        
        # Row and column of empty space
        row = empty // 3
        col = empty % 3
        
        # Possible moves: up, down, left, right
        moves = []
        if row > 0:  # Up
            moves.append(empty - 3)
        if row < 2:  # Down
            moves.append(empty + 3)
        if col > 0:  # Left
            moves.append(empty - 1)
        if col < 2:  # Right
            moves.append(empty + 1)
        
        # Create new states for each move
        for move_pos in moves:
            new_state = list(self.state)
            # Swap empty with neighbor
            new_state[empty], new_state[move_pos] = new_state[move_pos], new_state[empty]
            neighbors.append(PuzzleState(tuple(new_state)))
        
        return neighbors
    
    def get_inverse_count(self) -> int:
        """
        Count the number of inversions in the puzzle.
        An inversion is when a larger number appears before a smaller number.
        Used to check if a puzzle is solvable.
        
        Returns:
            Number of inversions
        """
        inversions = 0
        state_without_zero = [x for x in self.state if x != 0]
        
        for i in range(len(state_without_zero)):
            for j in range(i + 1, len(state_without_zero)):
                if state_without_zero[i] > state_without_zero[j]:
                    inversions += 1
        
        return inversions
    
    def is_solvable(self) -> bool:
        """
        Check if the puzzle is solvable.
        A puzzle is solvable if the number of inversions is even.
        
        Returns:
            True if solvable, False otherwise
        """
        return self.get_inverse_count() % 2 == 0
    
    @staticmethod
    def format_solution(path: List['PuzzleState']) -> str:
        """
        Format a solution path as a string.
        
        Args:
            path: List of PuzzleState objects representing the solution
        
        Returns:
            Formatted string representation of the solution
        """
        result = ""
        for i, state in enumerate(path):
            result += f"Step {i}:\n{state}\n"
        return result
