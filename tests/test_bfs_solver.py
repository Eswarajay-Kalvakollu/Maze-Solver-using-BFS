"""
Unit Tests for BFS Maze Solver, Grid Parser, Sample Inputs, and Optimality Guarantees.
"""

import os
import sys
from pathlib import Path
import unittest

# Ensure src/ is importable
repo_root = Path(__file__).resolve().parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from src.maze import MazeGrid, PRESET_MAZES, load_preset
from src.bfs_solver import BFSSolver
from src.dfs_solver import DFSSolver


class TestBFSMazeSolver(unittest.TestCase):

    def setUp(self):
        self.sample_inputs_dir = Path(__file__).resolve().parent / "sample_inputs"

    def test_simple_bfs_shortest_path(self):
        """Verify BFS returns shortest path on standard simple grid."""
        maze_str = """
S . .
# # .
. . G
"""
        grid = MazeGrid.from_string(maze_str)
        solver = BFSSolver(grid)
        result = solver.solve()

        self.assertTrue(result.found)
        self.assertEqual(result.path_length, 4)
        expected_path = [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)]
        self.assertEqual(result.path, expected_path)
        self.assertTrue(result.monotonic_distance_verified)

    def test_load_from_sample_input_files(self):
        """Verify loading maze from text file in tests/sample_inputs/."""
        filepath = self.sample_inputs_dir / "maze_simple.txt"
        self.assertTrue(filepath.exists(), f"Missing {filepath}")

        grid = MazeGrid.from_file(str(filepath))
        solver = BFSSolver(grid)
        result = solver.solve()

        self.assertTrue(result.found)
        self.assertEqual(result.path_length, 14)

    def test_start_equals_goal(self):
        """Edge case: start and goal are the same cell."""
        grid = MazeGrid(rows=3, cols=3, start=(1, 1), goal=(1, 1))
        solver = BFSSolver(grid)
        result = solver.solve()

        self.assertTrue(result.found)
        self.assertEqual(result.path_length, 0)
        self.assertEqual(result.path, [(1, 1)])
        self.assertEqual(result.nodes_explored, 1)

    def test_obstacle_blocking_and_isolation(self):
        """Verify obstacle handling when goal is completely blocked off."""
        filepath = self.sample_inputs_dir / "maze_no_path.txt"
        grid = MazeGrid.from_file(str(filepath))
        solver = BFSSolver(grid)
        result = solver.solve()

        self.assertFalse(result.found)
        self.assertEqual(result.path_length, 0)
        self.assertIn("No accessible path", result.error_message)

    def test_start_or_goal_in_obstacle(self):
        """Verify invalid start or goal placement on a wall."""
        maze_str = """
# . G
. . .
"""
        grid = MazeGrid.from_string(maze_str)
        grid.start = (0, 0)  # On wall '#'
        solver = BFSSolver(grid)
        result = solver.solve()

        self.assertFalse(result.found)
        self.assertIn("blocked by an obstacle", result.error_message)

    def test_matrix_parsing(self):
        """Verify loading from 2D integer matrix."""
        matrix = [
            [0, 1, 0],
            [0, 0, 0],
            [1, 1, 0]
        ]
        grid = MazeGrid.from_matrix(matrix, start=(0, 0), goal=(2, 2))
        solver = BFSSolver(grid)
        result = solver.solve()

        self.assertTrue(result.found)
        self.assertEqual(result.path_length, 4)

    def test_wavefront_distance_monotonicity(self):
        """Verify that every dequeued node's distance is >= previous dequeued node."""
        grid = load_preset("branching_choice")
        solver = BFSSolver(grid)
        result = solver.solve()

        self.assertTrue(result.found)
        self.assertTrue(result.monotonic_distance_verified)

        distances = [result.distance_map[node] for node in result.explored_order]
        for i in range(len(distances) - 1):
            self.assertLessEqual(distances[i], distances[i + 1])

    def test_bfs_optimality_vs_all_paths(self):
        """
        Verify BFS optimality against exhaustive search of all possible
        simple paths on a small grid with multiple viable routes.
        """
        maze_str = """
S . . .
. # . .
. . . G
"""
        grid = MazeGrid.from_string(maze_str)

        all_paths = []
        def find_all(curr, visited, path):
            if curr == grid.goal:
                all_paths.append(list(path))
                return
            for nbr in grid.get_neighbors(*curr):
                if nbr not in visited:
                    visited.add(nbr)
                    path.append(nbr)
                    find_all(nbr, visited, path)
                    path.pop()
                    visited.remove(nbr)

        find_all(grid.start, {grid.start}, [grid.start])
        self.assertGreater(len(all_paths), 1, "Should have multiple alternative paths.")

        min_path_length = min(len(p) - 1 for p in all_paths)

        bfs_solver = BFSSolver(grid)
        bfs_result = bfs_solver.solve()

        self.assertTrue(bfs_result.found)
        self.assertEqual(bfs_result.path_length, min_path_length)

    def test_bfs_strictly_no_longer_than_dfs(self):
        """Verify that across all presets, BFS path length <= DFS path length."""
        for preset_name in ["simple", "branching_choice", "dfs_trap", "labyrinth"]:
            grid = load_preset(preset_name)
            bfs_res = BFSSolver(grid).solve()
            dfs_res = DFSSolver(grid).solve()

            if bfs_res.found and dfs_res.found:
                self.assertLessEqual(
                    bfs_res.path_length,
                    dfs_res.path_length,
                    f"BFS failed optimality on preset '{preset_name}'"
                )


if __name__ == "__main__":
    unittest.main()
