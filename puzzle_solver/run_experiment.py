"""
Main experiment script for 8-puzzle branch and bound solver.
Runs experiments with all four heuristics and collects statistics.
"""

import sys
import json
from typing import List, Dict
import statistics
import time

# Add parent directory to path
sys.path.insert(0, '/home/luffy/class/DAA CLA2')

from puzzle_solver.puzzle_state import PuzzleState
from puzzle_solver.generator import PuzzleGenerator
from puzzle_solver.heuristics import HEURISTICS
from puzzle_solver.branch_and_bound import BranchAndBoundSolver, SearchStatistics


class ExperimentRunner:
    """Run experiments with different heuristics."""
    
    def __init__(self, num_puzzles: int = 100):
        """
        Initialize experiment runner.
        
        Args:
            num_puzzles: Number of puzzle instances to test
        """
        self.num_puzzles = num_puzzles
        self.puzzles = None
        self.results = {}
    
    def generate_puzzles(self) -> List[PuzzleState]:
        """Generate test puzzle instances."""
        print(f"Generating {self.num_puzzles} puzzle instances...")
        self.puzzles = PuzzleGenerator.generate_batch(self.num_puzzles)
        print(f"Successfully generated {len(self.puzzles)} unique puzzles.\n")
        return self.puzzles
    
    def run_experiment(self) -> Dict[str, List[SearchStatistics]]:
        """
        Run experiments with all heuristics.
        
        Returns:
            Dictionary mapping heuristic names to lists of statistics
        """
        if self.puzzles is None:
            self.generate_puzzles()
        
        results = {}
        
        for heuristic in HEURISTICS:
            print(f"Testing {heuristic.get_name()}...")
            solver = BranchAndBoundSolver(heuristic)
            
            statistics_list = []
            successful = 0
            
            for i, puzzle in enumerate(self.puzzles):
                solution, stats = solver.solve(puzzle)
                statistics_list.append(stats)
                
                if stats.solution_found:
                    successful += 1
                
                # Progress indicator
                if (i + 1) % 10 == 0:
                    print(f"  Completed {i + 1}/{self.num_puzzles} puzzles")
            
            results[heuristic.get_name()] = statistics_list
            print(f"  Completed! Success rate: {successful}/{self.num_puzzles}\n")
        
        self.results = results
        return results
    
    def print_summary(self):
        """Print summary of results."""
        if not self.results:
            print("No results to display. Run experiment first.")
            return
        
        print("=" * 80)
        print("EXPERIMENT SUMMARY")
        print("=" * 80)
        print(f"Number of puzzle instances tested: {self.num_puzzles}\n")
        
        print(f"{'Heuristic':<30} {'Avg Time (s)':<15} {'Avg Ratio':<15} {'Avg Nodes':<15}")
        print("-" * 75)
        
        for heuristic_name, stats_list in self.results.items():
            successful_stats = [s for s in stats_list if s.solution_found]
            
            if successful_stats:
                avg_time = statistics.mean([s.execution_time for s in successful_stats])
                avg_ratio = statistics.mean([s.ratio for s in successful_stats])
                avg_nodes = statistics.mean([s.nodes_expanded for s in successful_stats])
                success_rate = len(successful_stats) / len(stats_list)
                
                print(f"{heuristic_name:<30} {avg_time:<15.4f} {avg_ratio:<15.4f} {avg_nodes:<15.1f}")
                print(f"  Success rate: {success_rate*100:.1f}%")
            else:
                print(f"{heuristic_name:<30} {'FAILED':<15} {'N/A':<15} {'N/A':<15}")
        
        print("=" * 80 + "\n")
    
    def print_detailed_stats(self):
        """Print detailed statistics for each heuristic."""
        if not self.results:
            print("No results to display. Run experiment first.")
            return
        
        print("=" * 100)
        print("DETAILED STATISTICS")
        print("=" * 100)
        
        for heuristic_name, stats_list in self.results.items():
            successful_stats = [s for s in stats_list if s.solution_found]
            
            if not successful_stats:
                print(f"\n{heuristic_name}: NO SUCCESSFUL SOLUTIONS\n")
                continue
            
            print(f"\n{heuristic_name}")
            print("-" * 100)
            
            times = [s.execution_time for s in successful_stats]
            ratios = [s.ratio for s in successful_stats]
            nodes = [s.nodes_expanded for s in successful_stats]
            costs = [s.optimal_cost for s in successful_stats]
            
            print(f"  Execution Time (seconds):")
            print(f"    Mean: {statistics.mean(times):.6f}, Median: {statistics.median(times):.6f}")
            print(f"    Min:  {min(times):.6f}, Max:  {max(times):.6f}")
            print(f"    StdDev: {statistics.stdev(times) if len(times) > 1 else 0:.6f}")
            
            print(f"\n  Average Lower Bound / Optimal Cost Ratio:")
            print(f"    Mean: {statistics.mean(ratios):.4f}, Median: {statistics.median(ratios):.4f}")
            print(f"    Min:  {min(ratios):.4f}, Max:  {max(ratios):.4f}")
            print(f"    StdDev: {statistics.stdev(ratios) if len(ratios) > 1 else 0:.4f}")
            
            print(f"\n  Nodes Expanded:")
            print(f"    Mean: {statistics.mean(nodes):.1f}, Median: {statistics.median(nodes):.1f}")
            print(f"    Min:  {min(nodes):.1f}, Max:  {max(nodes):.1f}")
            print(f"    StdDev: {statistics.stdev(nodes) if len(nodes) > 1 else 0:.1f}")
            
            print(f"\n  Optimal Solution Cost (moves):")
            print(f"    Mean: {statistics.mean(costs):.1f}, Median: {statistics.median(costs):.1f}")
            print(f"    Min:  {min(costs):.1f}, Max:  {max(costs):.1f}")
            
            success_rate = len(successful_stats) / len(stats_list)
            print(f"\n  Success Rate: {success_rate*100:.1f}% ({len(successful_stats)}/{len(stats_list)})")
        
        print("\n" + "=" * 100 + "\n")
    
    def save_results(self, filename: str = "results.json"):
        """
        Save results to JSON file.
        
        Args:
            filename: Output filename
        """
        if not self.results:
            print("No results to save. Run experiment first.")
            return
        
        # Convert statistics to serializable format
        serializable_results = {}
        
        for heuristic_name, stats_list in self.results.items():
            serializable_results[heuristic_name] = {
                "successful_count": len([s for s in stats_list if s.solution_found]),
                "total_count": len(stats_list),
                "statistics": []
            }
            
            for stats in stats_list:
                serializable_results[heuristic_name]["statistics"].append({
                    "solution_found": stats.solution_found,
                    "solution_length": stats.solution_length,
                    "nodes_expanded": stats.nodes_expanded,
                    "optimal_cost": stats.optimal_cost,
                    "execution_time": stats.execution_time,
                    "average_lower_bound": stats.average_lower_bound,
                    "ratio": stats.ratio
                })
        
        filepath = f'/home/luffy/class/DAA CLA2/{filename}'
        with open(filepath, 'w') as f:
            json.dump(serializable_results, f, indent=2)
        
        print(f"Results saved to {filepath}")


def main():
    """Main experiment runner."""
    print("8-Puzzle Branch and Bound Solver - Experiment Runner")
    print("=" * 80)
    print()
    
    # Run with 50 puzzles for quick testing (can increase to 100+ for full results)
    runner = ExperimentRunner(num_puzzles=50)
    
    # Generate puzzles
    runner.generate_puzzles()
    
    # Run experiments
    print("Starting experiments...\n")
    runner.run_experiment()
    
    # Print results
    runner.print_summary()
    runner.print_detailed_stats()
    
    # Save results
    runner.save_results()


if __name__ == "__main__":
    main()
