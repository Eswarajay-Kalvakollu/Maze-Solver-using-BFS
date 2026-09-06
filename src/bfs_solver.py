"""
Breadth-First Search (BFS) Solver Module.

Implements standard FIFO queue-based exploration for uniform-cost grid mazes.
Guarantees the shortest path and provides step-by-step exploration metrics.
"""

import sys
from collections import deque
from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Set, Optional
import time

try:
    from .maze import MazeGrid, Coord
except ImportError:
    from maze import MazeGrid, Coord


@dataclass
class SearchResult:
    """Stores the complete outcome and search metrics of a maze run."""
    found: bool
    path: List[Coord] = field(default_factory=list)
    path_length: int = 0  # Number of steps (edges)
    explored_order: List[Coord] = field(default_factory=list)
    distance_map: Dict[Coord, int] = field(default_factory=dict)
    parent_map: Dict[Coord, Optional[Coord]] = field(default_factory=dict)
    nodes_explored: int = 0
    max_frontier_size: int = 0
    elapsed_time_ms: float = 0.0
    monotonic_distance_verified: bool = True
    error_message: Optional[str] = None


class BFSSolver:
    """
    Breadth-First Search solver operating on a MazeGrid.

    Optimality Invariant on Uniform-Cost Grids (edge cost c = 1):
    1. Monotonic Queue Distances: Nodes are removed from the FIFO queue
       in non-decreasing order of distance from start:
       d(v1) <= d(v2) <= d(v3) <= ...
    2. Minimal Path Guarantee: The first time the goal node is dequeued,
       its recorded distance d(goal) is guaranteed to be minimal.
    """

    def __init__(self, grid: MazeGrid):
        self.grid = grid

    def solve(self, start: Optional[Coord] = None, goal: Optional[Coord] = None) -> SearchResult:
        """
        Execute Breadth-First Search from start to goal.
        Returns a comprehensive SearchResult object.
        """
        start_coord = start if start is not None else self.grid.start
        goal_coord = goal if goal is not None else self.grid.goal

        # Validation of endpoints
        if start_coord is None or goal_coord is None:
            return SearchResult(
                found=False,
                error_message="Start and Goal coordinates must be specified."
            )

        if not self.grid.is_valid_coord(*start_coord):
            return SearchResult(
                found=False,
                error_message=f"Start coordinate {start_coord} is out of bounds."
            )

        if not self.grid.is_valid_coord(*goal_coord):
            return SearchResult(
                found=False,
                error_message=f"Goal coordinate {goal_coord} is out of bounds."
            )

        if not self.grid.is_passable(*start_coord):
            return SearchResult(
                found=False,
                error_message=f"Start coordinate {start_coord} is blocked by an obstacle."
            )

        if not self.grid.is_passable(*goal_coord):
            return SearchResult(
                found=False,
                error_message=f"Goal coordinate {goal_coord} is blocked by an obstacle."
            )

        # Edge Case: Start equals Goal
        if start_coord == goal_coord:
            return SearchResult(
                found=True,
                path=[start_coord],
                path_length=0,
                explored_order=[start_coord],
                distance_map={start_coord: 0},
                parent_map={start_coord: None},
                nodes_explored=1,
                max_frontier_size=1,
                monotonic_distance_verified=True
            )

        start_time = time.perf_counter()

        queue: deque[Coord] = deque([start_coord])
        visited: Set[Coord] = {start_coord}
        parent: Dict[Coord, Optional[Coord]] = {start_coord: None}
        distance: Dict[Coord, int] = {start_coord: 0}
        explored_order: List[Coord] = []

        max_frontier = 1
        prev_distance = 0
        monotonic_verified = True
        goal_found = False

        while queue:
            max_frontier = max(max_frontier, len(queue))
            current = queue.popleft()
            explored_order.append(current)

            curr_dist = distance[current]

            # Invariant Check: Distance must be non-decreasing (monotonic wavefront)
            if curr_dist < prev_distance:
                monotonic_verified = False
            prev_distance = curr_dist

            # Goal reached!
            if current == goal_coord:
                goal_found = True
                break

            # Explore all unblocked orthogonal neighbors
            for neighbor in self.grid.get_neighbors(*current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = current
                    distance[neighbor] = curr_dist + 1
                    queue.append(neighbor)

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
                monotonic_distance_verified=monotonic_verified,
                error_message="No accessible path exists from start to goal."
            )

        # Reconstruct path by following parent pointers backwards
        path: List[Coord] = []
        curr: Optional[Coord] = goal_coord
        while curr is not None:
            path.append(curr)
            curr = parent.get(curr)
        path.reverse()

        path_length = len(path) - 1

        return SearchResult(
            found=True,
            path=path,
            path_length=path_length,
            explored_order=explored_order,
            distance_map=distance,
            parent_map=parent,
            nodes_explored=len(explored_order),
            max_frontier_size=max_frontier,
            elapsed_time_ms=elapsed_ms,
            monotonic_distance_verified=monotonic_verified
        )
