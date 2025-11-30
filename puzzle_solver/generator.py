"""
Random puzzle generator for creating solvable 8-puzzle instances.
"""

import random
from typing import List
from .puzzle_state import PuzzleState


class PuzzleGenerator:
    """Generate random solvable 8-puzzle instances."""
    
    @staticmethod
    def generate_single() -> PuzzleState:
        """
        Generate a single random solvable puzzle by applying random moves from goal state.
        This guarantees the puzzle is solvable.
        
        Returns:
            Random solvable PuzzleState
        """
        state = PuzzleState(PuzzleState.GOAL_STATE)
        
        # Apply random moves to guarantee solvability
        num_moves = random.randint(50, 100)
        
        for _ in range(num_moves):
            neighbors = state.get_neighbors()
            state = random.choice(neighbors)
        
        return state
    
    @staticmethod
    def generate_batch(count: int) -> List[PuzzleState]:
        """
        Generate multiple random solvable puzzles.
        
        Args:
            count: Number of puzzles to generate
        
        Returns:
            List of random solvable PuzzleState objects
        """
        puzzles = []
        seen = set()
        
        while len(puzzles) < count:
            puzzle = PuzzleGenerator.generate_single()
            # Avoid duplicates
            if puzzle not in seen:
                puzzles.append(puzzle)
                seen.add(puzzle)
        
        return puzzles
    
    @staticmethod
    def generate_with_inversion_check(count: int, max_attempts: int = 10000) -> List[PuzzleState]:
        """
        Generate solvable puzzles by random shuffling and inversion count check.
        (Alternative method to random moves)
        
        Args:
            count: Number of puzzles to generate
            max_attempts: Maximum attempts to find solvable puzzles
        
        Returns:
            List of random solvable PuzzleState objects
        """
        puzzles = []
        seen = set()
        attempts = 0
        
        while len(puzzles) < count and attempts < max_attempts:
            # Create random permutation
            tiles = list(range(9))
            random.shuffle(tiles)
            state = PuzzleState(tuple(tiles))
            
            # Check if solvable
            if state.is_solvable() and state not in seen:
                puzzles.append(state)
                seen.add(state)
            
            attempts += 1
        
        return puzzles
