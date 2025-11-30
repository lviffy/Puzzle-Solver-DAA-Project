#!/usr/bin/env python3
"""
Main entry point for the 8-Puzzle Branch and Bound Solver project.
"""

import sys
import os

sys.path.insert(0, '/home/luffy/class/DAA CLA2')

from puzzle_solver.test import main as run_tests
from puzzle_solver.run_experiment import main as run_experiments


def print_menu():
    """Print main menu."""
    print("\n" + "=" * 70)
    print("8-Puzzle Branch and Bound Solver - Main Menu")
    print("=" * 70)
    print("\n1. Run validation tests")
    print("2. Run full experiment (50 puzzles)")
    print("3. Run full experiment (100 puzzles)")
    print("4. Analyze results and generate visualizations")
    print("5. Exit")
    print()


def main():
    """Main menu loop."""
    while True:
        print_menu()
        choice = input("Select option (1-5): ").strip()
        
        if choice == "1":
            print("\nRunning validation tests...")
            print("-" * 70)
            run_tests()
            
        elif choice == "2":
            print("\nRunning experiment with 50 puzzles...")
            print("-" * 70)
            # Temporarily modify the experiment to use 50 puzzles
            from puzzle_solver.run_experiment import ExperimentRunner
            runner = ExperimentRunner(num_puzzles=50)
            runner.generate_puzzles()
            runner.run_experiment()
            runner.print_summary()
            runner.print_detailed_stats()
            runner.save_results()
            
        elif choice == "3":
            print("\nRunning experiment with 100 puzzles...")
            print("(This may take several minutes)")
            print("-" * 70)
            from puzzle_solver.run_experiment import ExperimentRunner
            runner = ExperimentRunner(num_puzzles=100)
            runner.generate_puzzles()
            runner.run_experiment()
            runner.print_summary()
            runner.print_detailed_stats()
            runner.save_results()
            
        elif choice == "4":
            print("\nAnalyzing results and generating visualizations...")
            print("-" * 70)
            
            # List available results files
            import glob
            results_files = sorted(glob.glob('/home/luffy/class/DAA CLA2/results*.json'))
            
            if not results_files:
                print("Error: No results.json files found.")
                print("Please run an experiment first (option 2 or 3).")
            else:
                # Show available files
                if len(results_files) == 1:
                    results_file = results_files[0]
                    print(f"Using {os.path.basename(results_file)}")
                else:
                    print("\nAvailable results files:")
                    for i, f in enumerate(results_files, 1):
                        size = os.path.getsize(f) / 1024
                        print(f"  {i}. {os.path.basename(f)} ({size:.1f} KB)")
                    
                    file_choice = input("\nSelect file number (or press Enter for latest): ").strip()
                    if file_choice and file_choice.isdigit() and 1 <= int(file_choice) <= len(results_files):
                        results_file = results_files[int(file_choice) - 1]
                    else:
                        results_file = results_files[-1]  # Use latest
                
                try:
                    from puzzle_solver.analyze_results import ResultsAnalyzer
                    analyzer = ResultsAnalyzer(os.path.basename(results_file))
                    analyzer.plot_results()
                    analyzer.generate_report()
                    print("\nVisualization and report generated successfully!")
                except Exception as e:
                    print(f"Error: {e}")
            
        elif choice == "5":
            print("\nExiting...")
            break
            
        else:
            print("Invalid choice. Please select 1-5.")


if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║        8-Puzzle Branch and Bound Solver with Multiple Heuristics            ║
║                                                                              ║
║  This project implements and compares four different lower-bound heuristics ║
║  for solving the 8-puzzle problem using Branch and Bound search:            ║
║                                                                              ║
║  • H1: Trivial Heuristic (h=0)                                              ║
║  • H2: Misplaced Tiles                                                      ║
║  • H3: Manhattan Distance                                                   ║
║  • H4: Linear Conflict                                                      ║
║                                                                              ║
║  Through experimentation on multiple puzzle instances, this project         ║
║  demonstrates how better heuristics lead to exponentially more efficient    ║
║  search algorithms.                                                          ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    main()
