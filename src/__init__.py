"""
BFS Maze Solver Package.
"""

from .maze import MazeGrid, load_preset, PRESET_MAZES, Coord
from .bfs_solver import BFSSolver, SearchResult
from .dfs_solver import DFSSolver
from .visualizer import MazeVisualizer
from .optimality_demo import verify_monotonic_wavefront, compare_bfs_vs_dfs

__all__ = [
    "MazeGrid",
    "load_preset",
    "PRESET_MAZES",
    "Coord",
    "BFSSolver",
    "SearchResult",
    "DFSSolver",
    "MazeVisualizer",
    "verify_monotonic_wavefront",
    "compare_bfs_vs_dfs",
]
