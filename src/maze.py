"""
Maze and Grid Data Structure Module.

Handles grid representation, obstacle collision detection, neighbor generation,
conversion between string/matrix formats, and maze generation.
"""

import os
from typing import List, Tuple, Optional, Set
import random

# Cell representation constants
EMPTY = 0
WALL = 1

# Coordinate type alias: (row, col)
Coord = Tuple[int, int]


class MazeGrid:
    """
    Represents a 2D uniform-cost grid maze where each step between
    adjacent orthogonal cells has cost c = 1.
    """

    def __init__(self, rows: int, cols: int, walls: Optional[Set[Coord]] = None,
                 start: Optional[Coord] = None, goal: Optional[Coord] = None):
        self.rows = rows
        self.cols = cols
        self.walls: Set[Coord] = set(walls) if walls else set()
        self.start: Optional[Coord] = start
        self.goal: Optional[Coord] = goal

    def is_valid_coord(self, r: int, c: int) -> bool:
        """Check if (r, c) is within the grid boundaries."""
        return 0 <= r < self.rows and 0 <= c < self.cols

    def is_passable(self, r: int, c: int) -> bool:
        """Check if (r, c) is valid and not an obstacle/wall."""
        return self.is_valid_coord(r, c) and (r, c) not in self.walls

    def get_neighbors(self, r: int, c: int) -> List[Coord]:
        """
        Get valid orthogonal (Up, Right, Down, Left) unblocked neighbors.
        Each move represents a uniform cost of 1.
        """
        # Standard 4-directional moves: Up, Right, Down, Left
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        neighbors = []
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if self.is_passable(nr, nc):
                neighbors.append((nr, nc))
        return neighbors

    def add_wall(self, r: int, c: int) -> None:
        """Add an obstacle cell."""
        if self.is_valid_coord(r, c):
            self.walls.add((r, c))

    def remove_wall(self, r: int, c: int) -> None:
        """Remove an obstacle cell."""
        self.walls.discard((r, c))

    @classmethod
    def from_string(cls, maze_str: str) -> "MazeGrid":
        """
        Parse a maze from an ASCII string.
        Supports both space-delimited grids ('S . .') and compact grids ('S..').
        Tokens:
          '#' -> Wall / Obstacle
          '.' or ' ' -> Open passable cell
          'S' -> Start cell
          'G' -> Goal cell
        """
        raw_lines = [line.rstrip("\r\n") for line in maze_str.strip().splitlines() if line.strip()]
        if not raw_lines:
            raise ValueError("Maze string cannot be empty.")

        # Check if first line uses space-separated tokens
        first_split = raw_lines[0].strip().split()
        is_space_separated = len(first_split) > 1 and all(len(t) == 1 for t in first_split)

        parsed_grid: List[List[str]] = []
        for line in raw_lines:
            if is_space_separated:
                row = line.strip().split()
            else:
                row = list(line)
            parsed_grid.append(row)

        rows = len(parsed_grid)
        cols = max(len(row) for row in parsed_grid)

        walls: Set[Coord] = set()
        start: Optional[Coord] = None
        goal: Optional[Coord] = None

        for r, row in enumerate(parsed_grid):
            for c, ch in enumerate(row):
                if ch == "#":
                    walls.add((r, c))
                elif ch in ("S", "s"):
                    start = (r, c)
                elif ch in ("G", "g"):
                    goal = (r, c)
                elif ch in (".", " "):
                    pass
                else:
                    pass

        return cls(rows=rows, cols=cols, walls=walls, start=start, goal=goal)

    @classmethod
    def from_file(cls, filepath: str) -> "MazeGrid":
        """Load and parse a maze from a text file."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Maze file not found: {filepath}")
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        return cls.from_string(content)

    @classmethod
    def from_matrix(cls, matrix: List[List[int]], start: Coord, goal: Coord) -> "MazeGrid":
        """
        Construct a maze from a 2D integer matrix where:
          0 = Passable empty cell
          1 = Obstacle / wall
        """
        rows = len(matrix)
        cols = len(matrix[0]) if rows > 0 else 0
        walls: Set[Coord] = set()

        for r in range(rows):
            for c in range(cols):
                if matrix[r][c] == 1:
                    walls.add((r, c))

        return cls(rows=rows, cols=cols, walls=walls, start=start, goal=goal)

    @classmethod
    def generate_random(cls, rows: int, cols: int, obstacle_density: float = 0.20,
                        seed: Optional[int] = None) -> "MazeGrid":
        """Generate a random grid maze with a given obstacle density (0.0 to 0.5)."""
        if seed is not None:
            random.seed(seed)

        start = (0, 0)
        goal = (rows - 1, cols - 1)
        walls: Set[Coord] = set()

        for r in range(rows):
            for c in range(cols):
                if (r, c) == start or (r, c) == goal:
                    continue
                if random.random() < obstacle_density:
                    walls.add((r, c))

        return cls(rows=rows, cols=cols, walls=walls, start=start, goal=goal)

    def to_ascii(self, path: Optional[List[Coord]] = None,
                 explored: Optional[Set[Coord]] = None) -> str:
        """
        Render the maze as an ASCII string.
        Priority: Start/Goal > Path > Explored > Wall > Empty.
        """
        path_set = set(path) if path else set()
        explored_set = set(explored) if explored else set()

        lines = []
        for r in range(self.rows):
            row_chars = []
            for c in range(self.cols):
                coord = (r, c)
                if coord == self.start:
                    row_chars.append("S")
                elif coord == self.goal:
                    row_chars.append("G")
                elif coord in path_set:
                    row_chars.append("*")
                elif coord in self.walls:
                    row_chars.append("#")
                elif coord in explored_set:
                    row_chars.append(".")
                else:
                    row_chars.append(" ")
            lines.append("".join(row_chars))
        return "\n".join(lines)


# ==========================================
# Built-in Preset Mazes for Demonstration
# ==========================================

PRESET_MAZES = {
    "simple": """
S . . . .
# # # . #
. . . . .
. # # # #
. . . . G
""",

    "branching_choice": """
S . . . . . .
. # # # # # .
. # . . . # .
. # . G . # .
. # # # . # .
. . . . . . .
""",

    "dfs_trap": """
S . . . . . . . . . .
. # # # # # # # # # .
. # . . . . . . . # .
. # . . . . . . . # .
G . . . . . . . . . .
""",

    "no_path": """
S . . # . .
. . . # . .
# # # # # #
. . . # . .
. . . # . G
""",

    "labyrinth": """
#####################
#S........#.........#
#.#######.#.#######.#
#.#.....#.#.#.....#.#
#.#.###.#.#.#.###.#.#
#...#...#.....#...#.#
#####.#########.###.#
#...#.#.........#...#
#.#.#.#.#########.#.#
#.#...#...........#G#
#####################
"""
}


def load_preset(name: str) -> MazeGrid:
    """Load one of the built-in preset mazes."""
    if name not in PRESET_MAZES:
        raise ValueError(f"Unknown preset '{name}'. Available: {list(PRESET_MAZES.keys())}")
    return MazeGrid.from_string(PRESET_MAZES[name])
