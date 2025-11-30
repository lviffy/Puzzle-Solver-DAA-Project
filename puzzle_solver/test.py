"""
Quick test script to validate the implementation.
"""

import sys
sys.path.insert(0, '/home/luffy/class/DAA CLA2')

from puzzle_solver.puzzle_state import PuzzleState
from puzzle_solver.heuristics import h1, h2, h3, h4
from puzzle_solver.branch_and_bound import BranchAndBoundSolver
from puzzle_solver.generator import PuzzleGenerator


def test_puzzle_state():
    """Test PuzzleState class."""
    print("Testing PuzzleState...")
    
    # Test goal state
    goal = PuzzleState()
    assert goal.is_goal(), "Goal state should be goal"
    
    # Test with custom state
    custom = PuzzleState((1, 0, 2, 3, 4, 5, 6, 7, 8))
    assert not custom.is_goal(), "Custom state should not be goal"
    
    # Test neighbors
    neighbors = custom.get_neighbors()
    assert len(neighbors) == 3, f"Should have 3 neighbors, got {len(neighbors)}"
    
    # Test solvability
    assert custom.is_solvable(), "This puzzle should be solvable"
    
    print("✓ PuzzleState tests passed")


def test_heuristics():
    """Test heuristic functions."""
    print("\nTesting Heuristics...")
    
    goal = PuzzleState()
    assert h1.compute(goal) == 0, "H1 should be 0"
    assert h2.compute(goal) == 0, "H2 should be 0 at goal"
    assert h3.compute(goal) == 0, "H3 should be 0 at goal"
    assert h4.compute(goal) == 0, "H4 should be 0 at goal"
    
    # Test with non-goal state
    custom = PuzzleState((1, 2, 3, 4, 5, 6, 7, 8, 0))
    h1_val = h1.compute(custom)
    h2_val = h2.compute(custom)
    h3_val = h3.compute(custom)
    h4_val = h4.compute(custom)
    
    assert h1_val == 0, "H1 should always be 0"
    assert h2_val > 0, "H2 should be > 0 for non-goal"
    assert h3_val > 0, "H3 should be > 0 for non-goal"
    assert h4_val >= h3_val, "H4 should be >= H3"
    
    print(f"  Non-goal state heuristics: H1={h1_val}, H2={h2_val}, H3={h3_val}, H4={h4_val}")
    print("✓ Heuristic tests passed")


def test_generator():
    """Test puzzle generator."""
    print("\nTesting Puzzle Generator...")
    
    # Generate single puzzle
    puzzle = PuzzleGenerator.generate_single()
    assert puzzle.is_solvable(), "Generated puzzle should be solvable"
    
    # Generate batch
    batch = PuzzleGenerator.generate_batch(5)
    assert len(batch) == 5, "Should generate 5 puzzles"
    for p in batch:
        assert p.is_solvable(), "All generated puzzles should be solvable"
    
    print(f"✓ Generated {len(batch)} unique solvable puzzles")


def test_solver():
    """Test Branch and Bound solver."""
    print("\nTesting Branch and Bound Solver...")
    
    # Create simple puzzle (just one move from goal)
    puzzle = PuzzleState((1, 0, 2, 3, 4, 5, 6, 7, 8))
    
    # Test with H3
    solver = BranchAndBoundSolver(h3)
    solution, stats = solver.solve(puzzle)
    
    assert solution is not None, "Should find solution"
    assert stats.solution_found, "Should mark solution as found"
    assert stats.solution_length == 1, f"Should find 1-move solution, got {stats.solution_length}"
    
    print(f"✓ Solved {stats.solution_length}-move puzzle in {stats.execution_time:.4f}s")
    print(f"  Nodes expanded: {stats.nodes_expanded}")
    print(f"  Average ratio: {stats.ratio:.4f}")


def test_goal_state():
    """Test solving goal state."""
    print("\nTesting Goal State...")
    
    goal = PuzzleState()
    solver = BranchAndBoundSolver(h3)
    solution, stats = solver.solve(goal)
    
    assert solution is not None, "Should handle goal state"
    assert len(solution) == 1, "Goal state solution should have 1 step"
    assert stats.solution_length == 0, "Goal state cost should be 0"
    
    print("✓ Goal state handled correctly")


def main():
    """Run all tests."""
    print("=" * 50)
    print("Running Validation Tests")
    print("=" * 50)
    
    try:
        test_puzzle_state()
        test_heuristics()
        test_generator()
        test_solver()
        test_goal_state()
        
        print("\n" + "=" * 50)
        print("✓ All tests passed!")
        print("=" * 50)
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
