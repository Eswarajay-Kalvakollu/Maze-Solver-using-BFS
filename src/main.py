"""
Main CLI Application for BFS Maze Solver.

Provides an interactive and command-line interface to:
1. Solve preset mazes with BFS and visualize explored cells and optimal paths.
2. Demonstrate BFS optimality and contrast with DFS.
3. Solve custom ASCII or matrix mazes.
4. Solve custom maze files (e.g. from tests/sample_inputs/).
5. Solve dynamically generated random mazes.
"""

import sys
from pathlib import Path
import argparse

# Allow running directly as a script: py src/main.py
current_dir = Path(__file__).resolve().parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

try:
    from .maze import MazeGrid, PRESET_MAZES, load_preset
    from .bfs_solver import BFSSolver
    from .dfs_solver import DFSSolver
    from .visualizer import MazeVisualizer
    from .optimality_demo import run_optimality_demonstration, compare_bfs_vs_dfs
except ImportError:
    from maze import MazeGrid, PRESET_MAZES, load_preset
    from bfs_solver import BFSSolver
    from dfs_solver import DFSSolver
    from visualizer import MazeVisualizer
    from optimality_demo import run_optimality_demonstration, compare_bfs_vs_dfs


def run_preset(preset_name: str, compare: bool = False):
    """Solve and display a chosen preset maze."""
    print(f"\n--- Loading Preset: '{preset_name}' ---")
    grid = load_preset(preset_name)
    viz = MazeVisualizer(use_color=True)

    bfs_solver = BFSSolver(grid)
    bfs_result = bfs_solver.solve()
    viz.print_result(grid, bfs_result, title=f"BFS Solution - '{preset_name}'")

    if compare:
        dfs_solver = DFSSolver(grid)
        dfs_result = dfs_solver.solve()
        viz.print_result(grid, dfs_result, title=f"DFS Baseline - '{preset_name}'")

        print("\n--- Direct Comparison ---")
        print(f"BFS Shortest Path Length: {bfs_result.path_length}")
        print(f"DFS Path Length         : {dfs_result.path_length}")
        if bfs_result.path_length > 0 and dfs_result.path_length > 0:
            diff = dfs_result.path_length - bfs_result.path_length
            print(f"BFS saved {diff} steps compared to DFS.")


def run_file_input(filepath: str, compare: bool = False):
    """Solve a maze loaded from a text file."""
    print(f"\n--- Loading Maze File: '{filepath}' ---")
    grid = MazeGrid.from_file(filepath)
    viz = MazeVisualizer(use_color=True)

    bfs_solver = BFSSolver(grid)
    bfs_result = bfs_solver.solve()
    viz.print_result(grid, bfs_result, title=f"BFS Solution - '{filepath}'")

    if compare:
        dfs_solver = DFSSolver(grid)
        dfs_result = dfs_solver.solve()
        viz.print_result(grid, dfs_result, title=f"DFS Baseline - '{filepath}'")


def run_matrix_demo():
    """Demonstrate solving a custom 2D integer matrix grid."""
    print("\n--- Solving Custom 2D Matrix Grid ---")
    matrix = [
        [0, 0, 0, 0, 1, 0, 0],
        [1, 1, 0, 1, 1, 0, 1],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0],
    ]
    start = (0, 0)
    goal = (4, 6)

    grid = MazeGrid.from_matrix(matrix, start=start, goal=goal)
    viz = MazeVisualizer(use_color=True)
    bfs = BFSSolver(grid)
    res = bfs.solve()
    viz.print_result(grid, res, title="2D Matrix Grid BFS")


def run_random_maze(rows: int = 15, cols: int = 25, density: float = 0.20):
    """Solve a randomly generated maze."""
    print(f"\n--- Solving Random {rows}x{cols} Maze (Obstacle Density: {int(density*100)}%) ---")
    grid = MazeGrid.generate_random(rows, cols, obstacle_density=density, seed=42)
    viz = MazeVisualizer(use_color=True)
    bfs = BFSSolver(grid)
    res = bfs.solve()
    viz.print_result(grid, res, title=f"Random {rows}x{cols} Maze BFS")


def main():
    parser = argparse.ArgumentParser(description="Breadth-First Search (BFS) Maze Solver")
    parser.add_argument("--preset", type=str, choices=list(PRESET_MAZES.keys()),
                        help="Run a specific preset maze")
    parser.add_argument("--file", type=str,
                        help="Load and solve a maze from a text file (e.g. tests/sample_inputs/maze_simple.txt)")
    parser.add_argument("--compare", action="store_true",
                        help="Compare BFS against DFS on the chosen maze")
    parser.add_argument("--demo-optimality", action="store_true",
                        help="Run the complete theoretical and empirical optimality demonstration")
    parser.add_argument("--matrix-demo", action="store_true",
                        help="Run demonstration using a 2D integer matrix input")
    parser.add_argument("--random", action="store_true",
                        help="Generate and solve a random maze")

    args = parser.parse_args()

    if args.demo_optimality:
        run_optimality_demonstration()
    elif args.file:
        run_file_input(args.file, compare=args.compare)
    elif args.matrix_demo:
        run_matrix_demo()
    elif args.random:
        run_random_maze()
    elif args.preset:
        run_preset(args.preset, compare=args.compare)
    else:
        # Default: Run the highlight preset (dfs_trap) with comparison + matrix demo
        print("No arguments provided. Running featured demonstrations...")
        run_preset("dfs_trap", compare=True)
        run_matrix_demo()
        print("\nTip: Run 'py -m src.main --demo-optimality' to view the full proof and benchmarks.")
        print(f"Available presets: {', '.join(PRESET_MAZES.keys())}")


if __name__ == "__main__":
    main()
