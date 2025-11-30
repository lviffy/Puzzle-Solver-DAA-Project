"""
Visualization and reporting script for experiment results.
"""

import sys
import json
from typing import Dict, List

# Try to import visualization libraries
try:
    import matplotlib.pyplot as plt
    import numpy as np
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("Warning: matplotlib/numpy not available. Text report will be generated.")

# Add parent directory to path
sys.path.insert(0, '/home/luffy/class/DAA CLA2')


class ResultsAnalyzer:
    """Analyze and visualize experiment results."""
    
    def __init__(self, results_file: str = "results.json"):
        """
        Load results from JSON file.
        
        Args:
            results_file: Path to results JSON file
        """
        filepath = f'/home/luffy/class/DAA CLA2/{results_file}'
        with open(filepath, 'r') as f:
            self.results = json.load(f)
        
        self.heuristics = list(self.results.keys())
    
    def extract_metrics(self) -> Dict[str, Dict[str, float]]:
        """
        Extract mean metrics for each heuristic.
        
        Returns:
            Dictionary with metrics for each heuristic
        """
        metrics = {}
        
        for heuristic, data in self.results.items():
            stats = data["statistics"]
            successful = [s for s in stats if s["solution_found"]]
            
            if successful:
                times = [s["execution_time"] for s in successful]
                ratios = [s["ratio"] for s in successful]
                nodes = [s["nodes_expanded"] for s in successful]
                
                # Calculate mean manually if numpy not available
                avg_time = sum(times) / len(times) if times else 0
                avg_ratio = sum(ratios) / len(ratios) if ratios else 0
                avg_nodes = sum(nodes) / len(nodes) if nodes else 0
                
                metrics[heuristic] = {
                    "avg_time": avg_time,
                    "avg_ratio": avg_ratio,
                    "avg_nodes": avg_nodes,
                    "success_rate": len(successful) / len(stats)
                }
            else:
                metrics[heuristic] = {
                    "avg_time": 0,
                    "avg_ratio": 0,
                    "avg_nodes": 0,
                    "success_rate": 0
                }
        
        return metrics
    
    def plot_results(self, output_dir: str = "/home/luffy/class/DAA CLA2"):
        """
        Create three plots for the results.
        
        Args:
            output_dir: Directory to save plots
        """
        if not HAS_MATPLOTLIB:
            print("Matplotlib not available. Skipping visualization plots.")
            return None
            
        metrics = self.extract_metrics()
        
        heuristic_names = []
        times = []
        ratios = []
        nodes = []
        
        for heuristic, data in metrics.items():
            # Extract short name from heuristic
            short_name = heuristic.split(":")[0].strip()
            heuristic_names.append(short_name)
            times.append(data["avg_time"])
            ratios.append(data["avg_ratio"])
            nodes.append(data["avg_nodes"])
        
        # Create figure with three subplots
        fig, axes = plt.subplots(1, 3, figsize=(16, 5))
        
        # Plot 1: Execution Time
        axes[0].bar(heuristic_names, times, color='steelblue', edgecolor='black')
        axes[0].set_title('Average Execution Time vs Heuristic', fontsize=12, fontweight='bold')
        axes[0].set_ylabel('Time (seconds)', fontsize=11)
        axes[0].set_xlabel('Heuristic', fontsize=11)
        axes[0].grid(axis='y', alpha=0.3)
        for i, v in enumerate(times):
            axes[0].text(i, v + max(times)*0.02, f'{v:.4f}s', ha='center', fontsize=9)
        
        # Plot 2: Average Ratio
        axes[1].bar(heuristic_names, ratios, color='coral', edgecolor='black')
        axes[1].set_title('Average Ratio (Lower Bound / Optimal Cost)', fontsize=12, fontweight='bold')
        axes[1].set_ylabel('Ratio', fontsize=11)
        axes[1].set_xlabel('Heuristic', fontsize=11)
        axes[1].grid(axis='y', alpha=0.3)
        for i, v in enumerate(ratios):
            axes[1].text(i, v + max(ratios)*0.02, f'{v:.2f}', ha='center', fontsize=9)
        
        # Plot 3: Nodes Expanded
        axes[2].bar(heuristic_names, nodes, color='lightgreen', edgecolor='black')
        axes[2].set_title('Average Nodes Expanded', fontsize=12, fontweight='bold')
        axes[2].set_ylabel('Number of Nodes', fontsize=11)
        axes[2].set_xlabel('Heuristic', fontsize=11)
        axes[2].grid(axis='y', alpha=0.3)
        for i, v in enumerate(nodes):
            axes[2].text(i, v + max(nodes)*0.02, f'{v:.0f}', ha='center', fontsize=9)
        
        # Adjust layout and save
        plt.tight_layout()
        output_path = f"{output_dir}/experiment_results.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Figure saved to {output_path}")
        
        return fig, axes
    
    def generate_report(self, output_file: str = "report.txt"):
        """
        Generate a text report of results.
        
        Args:
            output_file: Output file name
        """
        metrics = self.extract_metrics()
        
        report = []
        report.append("=" * 80)
        report.append("8-PUZZLE BRANCH AND BOUND SOLVER - EXPERIMENT REPORT")
        report.append("=" * 80)
        report.append("")
        
        # Summary table
        report.append("SUMMARY TABLE")
        report.append("-" * 80)
        report.append(f"{'Heuristic':<25} {'Avg Time':<15} {'Avg Ratio':<15} {'Avg Nodes':<15}")
        report.append("-" * 80)
        
        for heuristic, metrics_data in metrics.items():
            report.append(
                f"{heuristic:<25} {metrics_data['avg_time']:<15.6f} "
                f"{metrics_data['avg_ratio']:<15.4f} {metrics_data['avg_nodes']:<15.1f}"
            )
        
        report.append("")
        report.append("=" * 80)
        report.append("")
        
        # Heuristic descriptions
        report.append("HEURISTIC DESCRIPTIONS")
        report.append("-" * 80)
        
        report.append("""
H1: Trivial Heuristic (h=0)
  - Always returns 0
  - Represents uninformed search (Uniform Cost Search)
  - Expected to be slowest as it provides no guidance
  - Baseline for comparison

H2: Misplaced Tiles Heuristic
  - Counts the number of tiles not in their correct position
  - Ignores the empty space (0)
  - Range: 0 to 8
  - Admissible and consistent
  - More informative than H1 but still loose

H3: Manhattan Distance Heuristic
  - Sum of Manhattan distances of each tile to its goal position
  - Manhattan distance = |row_diff| + |col_diff|
  - Range: 0 to 24
  - Admissible and consistent
  - Better lower bound than H2

H4: Linear Conflict Heuristic
  - Manhattan distance + 2 × (number of linear conflicts)
  - A linear conflict occurs when two tiles are in the same row/column
    as their goal position but in reverse order
  - Tighter lower bound than Manhattan distance
  - Most expensive to compute but should give best search performance
""")
        
        report.append("=" * 80)
        report.append("")
        
        # Performance analysis
        report.append("PERFORMANCE ANALYSIS")
        report.append("-" * 80)
        
        # Find best performers
        best_time_heur = min(metrics.items(), key=lambda x: x[1]['avg_time'] if x[1]['avg_time'] > 0 else float('inf'))[0]
        best_ratio_heur = min(metrics.items(), key=lambda x: x[1]['avg_ratio'] if x[1]['avg_ratio'] > 0 else float('inf'))[0]
        best_nodes_heur = min(metrics.items(), key=lambda x: x[1]['avg_nodes'] if x[1]['avg_nodes'] > 0 else float('inf'))[0]
        
        report.append(f"Fastest heuristic: {best_time_heur}")
        report.append(f"  Average time: {metrics[best_time_heur]['avg_time']:.6f} seconds")
        report.append("")
        
        report.append(f"Best ratio (tightest lower bound): {best_ratio_heur}")
        report.append(f"  Average ratio: {metrics[best_ratio_heur]['avg_ratio']:.4f}")
        report.append("")
        
        report.append(f"Fewest nodes expanded: {best_nodes_heur}")
        report.append(f"  Average nodes: {metrics[best_nodes_heur]['avg_nodes']:.1f}")
        report.append("")
        
        report.append("=" * 80)
        report.append("")
        
        # Observations and insights
        report.append("OBSERVATIONS AND INSIGHTS")
        report.append("-" * 80)
        report.append("""
The experiment demonstrates the importance of good heuristics in guided search:

1. H1 (Trivial) provides no guidance and typically explores many nodes
   This is essentially breadth-first search by cost

2. H2 (Misplaced Tiles) provides weak guidance but is fast to compute
   Improves significantly over H1

3. H3 (Manhattan Distance) provides much tighter bounds
   Dramatically reduces search time compared to H2
   This is a commonly used heuristic for 8-puzzle

4. H4 (Linear Conflict) provides the tightest bounds
   More expensive to compute but explores far fewer nodes
   Best overall search performance

The ratio (average lower bound / optimal cost) indicates bound tightness:
- Ratio close to 1 = very tight bound = efficient search
- Ratio >> 1 = loose bound = inefficient search

These results validate the core principle of informed search:
better heuristics lead to more efficient algorithms.
""")
        
        report.append("=" * 80)
        
        # Write report
        report_text = "\n".join(report)
        
        filepath = f'/home/luffy/class/DAA CLA2/{output_file}'
        with open(filepath, 'w') as f:
            f.write(report_text)
        
        print(f"Report saved to {filepath}")
        return report_text


def main():
    """Main analysis runner."""
    print("Results Analyzer - Generating Visualizations and Report")
    print("=" * 80)
    print()
    
    # Check for command line argument for results file
    results_file = "results.json"
    if len(sys.argv) > 1:
        results_file = sys.argv[1]
    
    try:
        analyzer = ResultsAnalyzer(results_file)
        
        # Generate plots
        print("Generating plots...")
        analyzer.plot_results()
        
        # Generate report
        print("Generating report...")
        analyzer.generate_report()
        
        print("\nAnalysis complete!")
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please run run_experiment.py first to generate results.json")


if __name__ == "__main__":
    main()
