"""
Depth-First Search (DFS) Solver Module.

Used as a comparative baseline to demonstrate why uninformed DFS does NOT
guarantee shortest paths on uniform-cost grids, contrasting with BFS.
"""

from typing import List, Dict, Set, Optional
import time

try:
    from .maze import MazeGrid, Coord
    from .bfs_solver import SearchResult
except ImportError:
    from maze import MazeGrid, Coord
    from bfs_solver import SearchResult


class DFSSolver:
    """
    Depth-First Search (DFS) solver using a LIFO stack.
    Explores paths deeply before backtracking.
    Does NOT guarantee shortest path.
    """

    def __init__(self, grid: MazeGrid):
        self.grid = grid

    def solve(self, start: Optional[Coord] = None, goal: Optional[Coord] = None) -> SearchResult:
        """Execute DFS from start to goal."""
        start_coord = start if start is not None else self.grid.start
        goal_coord = goal if goal is not None else self.grid.goal

        if start_coord is None or goal_coord is None:
            return SearchResult(found=False, error_message="Start and Goal must be defined.")

        if not self.grid.is_passable(*start_coord) or not self.grid.is_passable(*goal_coord):
            return SearchResult(found=False, error_message="Start or Goal is impassable.")

        if start_coord == goal_coord:
            return SearchResult(
                found=True,
                path=[start_coord],
                path_length=0,
                explored_order=[start_coord],
                distance_map={start_coord: 0},
                parent_map={start_coord: None},
                nodes_explored=1,
                max_frontier_size=1
            )

        start_time = time.perf_counter()

        stack: List[Coord] = [start_coord]
        visited: Set[Coord] = {start_coord}
        parent: Dict[Coord, Optional[Coord]] = {start_coord: None}
        distance: Dict[Coord, int] = {start_coord: 0}
        explored_order: List[Coord] = []
        max_frontier = 1
        goal_found = False

        while stack:
            max_frontier = max(max_frontier, len(stack))
            current = stack.pop()
            explored_order.append(current)

            curr_dist = distance[current]

            if current == goal_coord:
                goal_found = True
                break

            neighbors = self.grid.get_neighbors(*current)
            for neighbor in reversed(neighbors):
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = current
                    distance[neighbor] = curr_dist + 1
                    stack.append(neighbor)

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        if not goal_found:
            return SearchResult(
                found=False,
                explored_order=explored_order,
                distance_map=distance,
                parent_map=parent,
                nodes_explored=len(explored_order),
                max_frontier_size=max_frontier,
                elapsed_time_ms=elapsed_ms,
                error_message="No accessible path exists."
            )

        path: List[Coord] = []
        curr: Optional[Coord] = goal_coord
        while curr is not None:
            path.append(curr)
            curr = parent.get(curr)
        path.reverse()

        return SearchResult(
            found=True,
            path=path,
            path_length=len(path) - 1,
            explored_order=explored_order,
            distance_map=distance,
            parent_map=parent,
            nodes_explored=len(explored_order),
            max_frontier_size=max_frontier,
            elapsed_time_ms=elapsed_ms,
            monotonic_distance_verified=False
        )
