"""
Branch and Bound search algorithm for the 8-puzzle problem.
"""

from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from .puzzle_state import PuzzleState
from .heuristics import Heuristic
import time


@dataclass
class SearchStatistics:
    """Statistics collected during search."""
    heuristic_name: str
    solution_found: bool
    solution_length: int
    nodes_expanded: int
    optimal_cost: int
    execution_time: float
    lower_bound_sum: float
    lower_bound_count: int
    
    @property
    def average_lower_bound(self) -> float:
        """Calculate average lower bound estimate."""
        if self.lower_bound_count == 0:
            return 0
        return self.lower_bound_sum / self.lower_bound_count
    
    @property
    def ratio(self) -> float:
        """Calculate ratio of average lower bound to optimal cost."""
        if self.optimal_cost == 0:
            return 0
        return self.average_lower_bound / self.optimal_cost


class BranchAndBoundSolver:
    """
    Branch and Bound solver for the 8-puzzle problem.
    Expands nodes in order of f(n) = g(n) + h(n), where:
    - g(n) is the cost from initial state to n
    - h(n) is the lower bound (heuristic) estimate from n to goal
    """
    
    def __init__(self, heuristic: Heuristic):
        """
        Initialize solver with a heuristic.
        
        Args:
            heuristic: Heuristic function to use for search
        """
        self.heuristic = heuristic
        self.statistics = None
    
    def solve(self, initial_state: PuzzleState) -> Tuple[Optional[List[PuzzleState]], SearchStatistics]:
        """
        Solve the puzzle using Branch and Bound search.
        
        Args:
            initial_state: Starting puzzle state
        
        Returns:
            Tuple of (solution_path, statistics)
            - solution_path: List of states from initial to goal (None if no solution)
            - statistics: SearchStatistics object with performance metrics
        """
        start_time = time.time()
        
        # Initialize statistics
        stats = SearchStatistics(
            heuristic_name=self.heuristic.get_name(),
            solution_found=False,
            solution_length=0,
            nodes_expanded=0,
            optimal_cost=0,
            execution_time=0,
            lower_bound_sum=0,
            lower_bound_count=0
        )
        
        # Check if puzzle is solvable
        if not initial_state.is_solvable():
            stats.execution_time = time.time() - start_time
            return None, stats
        
        # Special case: already at goal
        if initial_state.is_goal():
            stats.solution_found = True
            stats.solution_length = 0
            stats.optimal_cost = 0
            stats.execution_time = time.time() - start_time
            return [initial_state], stats
        
        # Initialize best solution cost to infinity
        best_solution_cost = float('inf')
        best_solution_path = None
        
        # Open list (priority queue): (f_value, g_value, state, path)
        open_list = []
        open_set = set()
        
        # Initialize open list with initial state
        h_initial = self.heuristic.compute(initial_state)
        f_initial = h_initial
        open_list.append((f_initial, 0, initial_state, [initial_state]))
        open_set.add(initial_state)
        
        # Closed set for visited states
        closed_set = set()
        
        # Sort by f-value (we'll manually maintain priority)
        open_list.sort(key=lambda x: x[0])
        
        while open_list:
            # Get node with minimum f-value
            open_list.sort(key=lambda x: x[0])
            f_value, g_value, current_state, path = open_list.pop(0)
            
            if current_state in open_set:
                open_set.remove(current_state)
            
            # Skip if we've already visited this state
            if current_state in closed_set:
                continue
            
            closed_set.add(current_state)
            stats.nodes_expanded += 1
            
            # Prune: if current lower bound + g >= best solution, skip
            h_value = self.heuristic.compute(current_state)
            stats.lower_bound_sum += h_value
            stats.lower_bound_count += 1
            
            if g_value + h_value >= best_solution_cost:
                continue
            
            # Check if goal
            if current_state.is_goal():
                best_solution_cost = g_value
                best_solution_path = path
                stats.solution_found = True
                stats.solution_length = g_value
                stats.optimal_cost = g_value
                continue
            
            # Expand neighbors
            for neighbor in current_state.get_neighbors():
                if neighbor not in closed_set and neighbor not in open_set:
                    new_g = g_value + 1
                    h_neighbor = self.heuristic.compute(neighbor)
                    f_neighbor = new_g + h_neighbor
                    
                    # Only add if potentially better than current best
                    if f_neighbor < best_solution_cost:
                        new_path = path + [neighbor]
                        open_list.append((f_neighbor, new_g, neighbor, new_path))
                        open_set.add(neighbor)
        
        stats.execution_time = time.time() - start_time
        self.statistics = stats
        
        return best_solution_path, stats
    
    def solve_multiple(self, initial_states: List[PuzzleState]) -> List[Tuple[Optional[List[PuzzleState]], SearchStatistics]]:
        """
        Solve multiple puzzle instances.
        
        Args:
            initial_states: List of initial puzzle states
        
        Returns:
            List of (solution_path, statistics) tuples
        """
        results = []
        for state in initial_states:
            result = self.solve(state)
            results.append(result)
        return results
