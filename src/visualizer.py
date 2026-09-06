"""
Maze Visualizer Module.

Provides rich text and ANSI-colored terminal visualizations of grid mazes,
highlighting explored cells, distance wavefront contours, and reconstructed shortest paths.
"""

import sys
from typing import Optional, Set, List

try:
    from .maze import MazeGrid, Coord
    from .bfs_solver import SearchResult
except ImportError:
    from maze import MazeGrid, Coord
    from bfs_solver import SearchResult

# Ensure safe UTF-8 output on Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# ANSI Color Codes
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"

COLOR_WALL = "\033[90m"        # Dark Gray
COLOR_EMPTY = "\033[37m"       # White
COLOR_START = "\033[92;1m"     # Bright Green
COLOR_GOAL = "\033[93;1m"      # Bright Yellow
COLOR_PATH = "\033[96;1m"      # Bright Cyan
COLOR_EXPLORED = "\033[34m"    # Blue


class MazeVisualizer:
    """Renders maze search states, paths, and exploration wavefronts."""

    def __init__(self, use_color: bool = True):
        self.use_color = use_color

    def _colorize(self, text: str, color_code: str) -> str:
        if not self.use_color:
            return text
        return f"{color_code}{text}{RESET}"

    def render_summary(self, grid: MazeGrid, result: SearchResult,
                       show_distances: bool = False) -> str:
        """
        Renders the grid with walls, explored nodes, and the shortest path.
        If show_distances is True, displays distance % 10 for explored nodes
        to visualize the expanding concentric wavefront.
        """
        path_set = set(result.path) if result.path else set()
        explored_set = set(result.explored_order) if result.explored_order else set()

        lines = []
        lines.append("+" + "-" * (grid.cols * 2 + 1) + "+")

        for r in range(grid.rows):
            row_str = ["| "]
            for c in range(grid.cols):
                coord = (r, c)
                if coord == grid.start:
                    cell_char = self._colorize("S ", COLOR_START)
                elif coord == grid.goal:
                    cell_char = self._colorize("G ", COLOR_GOAL)
                elif coord in path_set:
                    cell_char = self._colorize("* ", COLOR_PATH)
                elif coord in grid.walls:
                    cell_char = self._colorize("# ", COLOR_WALL)
                elif coord in explored_set:
                    if show_distances and coord in result.distance_map:
                        d = result.distance_map[coord] % 10
                        cell_char = self._colorize(f"{d} ", COLOR_EXPLORED)
                    else:
                        cell_char = self._colorize(". ", COLOR_EXPLORED)
                else:
                    cell_char = "  "
                row_str.append(cell_char)
            row_str.append("|")
            lines.append("".join(row_str))

        lines.append("+" + "-" * (grid.cols * 2 + 1) + "+")
        return "\n".join(lines)

    def print_result(self, grid: MazeGrid, result: SearchResult, title: str = "BFS Maze Solution"):
        """Print full visualization alongside detailed search metrics."""
        print("\n" + "=" * 60)
        print(f" {title.upper()}")
        print("=" * 60)

        if not result.found:
            print(f"STATUS: FAILURE - {result.error_message}")
            print(self.render_summary(grid, result))
            print(f"Explored: {result.nodes_explored} cells before failing.")
            print("=" * 60)
            return

        print(f"STATUS: SUCCESS (Shortest Path Found)")
        print(f"Path Length (Steps/Edges) : {result.path_length}")
        print(f"Nodes Explored            : {result.nodes_explored}")
        print(f"Max Frontier Queue Size   : {result.max_frontier_size}")
        print(f"Execution Time            : {result.elapsed_time_ms:.3f} ms")
        print(f"Optimality Guarantee (BFS): {'VERIFIED (Monotonic Wavefront)' if result.monotonic_distance_verified else 'N/A'}")
        print("\nGrid Map (Legend: S=Start, G=Goal, *=Optimal Path, .=Explored, #=Wall):")
        print(self.render_summary(grid, result, show_distances=False))

        print("\nWavefront Distance Map (Numbers indicate dist mod 10):")
        print(self.render_summary(grid, result, show_distances=True))
        print("=" * 60)
