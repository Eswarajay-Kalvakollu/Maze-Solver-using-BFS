# BFS Maze Solver: Uninformed Search on Uniform-Cost Grids

An uninformed search implementation that solves 2D grid mazes using Breadth-First Search (BFS), returning the guaranteed shortest path from start to goal while providing comprehensive obstacle handling, wavefront visualization, and formal/empirical demonstration of BFS optimality.

---

## 1. Problem Description

Given a 2D discrete grid \(R \times C\) containing:
- **Start Node (\(S\))**: The initial cell coordinates.
- **Goal Node (\(G\))**: The target destination cell.
- **Obstacles (\(#\))**: Non-traversable wall cells that cannot be entered.
- **Passable Cells (\(.\))**: Open cells traversable in orthogonal directions (Up, Down, Left, Right).

Every step between adjacent cells incurs an identical unit cost (\(c(e) = 1\)). The objective is to find a collision-free path from \(S\) to \(G\) that strictly minimizes the total path cost (number of edges).

---

## 2. Approach & Optimality Guarantee

### Breadth-First Search (BFS) Engine
- **Data Structure**: Utilizes a First-In, First-Out (FIFO) queue (`collections.deque`).
- **State Tracking**: Maintains a `visited` set to avoid revisiting nodes, a `parent` mapping for backtracking the final shortest path, and a `distance_map` recording the step count from Start.

### Why is BFS Optimal on a Uniform-Cost Grid?
1. **Concentric Wavefront Expansion**: Nodes are discovered in expanding distance layers:
   \[
   L_d = \{ v \mid \text{dist}(S, v) = d \}
   \]
2. **Queue Invariant**: At any moment, the FIFO queue contains nodes of distance at most \(\{d, d + 1\}\).
3. **Monotonic Non-Decreasing Distances**: Vertices are dequeued in monotonically non-decreasing order of cost:
   \[
   d(v_1) \le d(v_2) \le d(v_3) \le \dots \le d(v_k)
   \]
4. **First-Hit Minimality**: When Goal \(G\) is first dequeued at distance \(d^*\), all remaining elements in the queue and unexplored space have distance \(\ge d^*\). Therefore, no alternate path can exist with fewer edges.

### Contrast with Depth-First Search (DFS)
DFS relies on a LIFO stack, diving aggressively down corridors. On uniform-cost grids with loops or open areas, DFS is vulnerable to getting trapped in deep detours, producing severely suboptimal paths (up to 8x longer than BFS).

---

## 3. Repository Structure

```
bfs-maze-solver/
├── src/                        # Source code
│   ├── __init__.py
│   ├── maze.py                 # Grid data structures, parsers & presets
│   ├── bfs_solver.py           # BFS engine & optimality invariant checks
│   ├── dfs_solver.py           # DFS baseline for comparison
│   ├── visualizer.py           # Terminal ANSI & ASCII renderer
│   ├── optimality_demo.py      # Formal proof & comparative benchmark
│   └── main.py                 # Unified CLI entry point
├── tests/                      # Test cases & sample inputs
│   ├── __init__.py
│   ├── test_bfs_solver.py      # Automated unittest suite
│   └── sample_inputs/          # Sample maze files (.txt & .json)
│       ├── maze_simple.txt
│       ├── maze_dfs_trap.txt
│       ├── maze_branching.txt
│       ├── maze_labyrinth.txt
│       ├── maze_no_path.txt
│       └── maze_matrix.json
├── docs/                       # Technical report, plots & PDF
│   ├── report.pdf              # Printable multi-page PDF report
│   ├── report.md               # Markdown report
│   ├── generate_docs_and_plots.py
│   └── plots/                  # Visual artifacts & figures
│       ├── bfs_vs_dfs_comparison.png
│       ├── wavefront_distance_heatmap.png
│       └── layer_expansion.png
├── README.md                   # Problem, approach, how-to-run, sample I/O
├── requirements.txt            # Project dependencies
├── .gitignore                  # Git exclusion rules
└── LICENSE                     # MIT License
```

---

## 4. How to Run

### Prerequisites
Python 3.8 or higher is required.

```powershell
# Optional: install matplotlib & numpy if you wish to re-generate plots in docs/
pip install -r requirements.txt
```

### 1. Default Run (Featured Demos)
Runs the DFS-trap demonstration followed by a 2D integer matrix input:
```powershell
py -m src.main
# or
py src/main.py
```

### 2. Solve a Maze from a Text File
Load and solve any custom text maze from `tests/sample_inputs/`:
```powershell
py -m src.main --file tests/sample_inputs/maze_simple.txt
py -m src.main --file tests/sample_inputs/maze_dfs_trap.txt --compare
```

### 3. Compare BFS vs DFS on Presets
```powershell
py -m src.main --preset dfs_trap --compare
py -m src.main --preset branching_choice --compare
```

### 4. Run Full Optimality Demonstration & Benchmarks
```powershell
py -m src.main --demo-optimality
```

### 5. Generate and Solve a Procedural Random Maze
```powershell
py -m src.main --random
```

### 6. Run the Automated Test Suite
```powershell
py -m unittest discover tests
```

---

## 5. Sample Input / Output (I/O)

### Sample Input (`tests/sample_inputs/maze_branching.txt`)
```
S . . . . . .
. # # # # # .
. # . . . # .
. # . G . # .
. # # # . # .
. . . . . . .
```

### Sample Output (`py -m src.main --preset branching_choice --compare`)
```
--- Loading Preset: 'branching_choice' ---

============================================================
 BFS SOLUTION - 'BRANCHING_CHOICE'
============================================================
STATUS: SUCCESS (Shortest Path Found)
Path Length (Steps/Edges) : 12
Nodes Explored            : 26
Max Frontier Queue Size   : 3
Execution Time            : 0.137 ms
Optimality Guarantee (BFS): VERIFIED (Monotonic Wavefront)

Grid Map (Legend: S=Start, G=Goal, *=Optimal Path, .=Explored, #=Wall):
+---------------+
| S . . . . . . |
| * # # # # # . |
| * #     . # . |
| * #   G * # . |
| * # # # * # . |
| * * * * * . . |
+---------------+

Wavefront Distance Map (Numbers indicate dist mod 10):
+---------------+
| S 1 2 3 4 5 6 |
| * # # # # # 7 |
| * #     2 # 8 |
| * #   G * # 9 |
| * # # # * # 0 |
| * * * * * 0 1 |
+---------------+
============================================================

--- Direct Comparison ---
BFS Shortest Path Length: 12
DFS Path Length         : 16
BFS saved 4 steps compared to DFS.
```

### Sample Optimality Benchmark Output (`py -m src.main --demo-optimality`)
```
----------------------------------------------------------------------------
2. COMPARATIVE BENCHMARK: BFS (OPTIMAL) VS DFS (UNINFORMED)
----------------------------------------------------------------------------
Maze Preset          | BFS Path   | DFS Path   | Extra Steps (DFS)  | DFS Suboptimality
----------------------------------------------------------------------------
simple               | 14         | 14         | +0                 | Optimal (1.0x)
branching_choice     | 12         | 16         | +4                 | 1.33x longer
dfs_trap             | 4          | 32         | +28                | 8.0x longer
labyrinth            | 34         | 34         | +0                 | Optimal (1.0x)
----------------------------------------------------------------------------
```

---

## 6. Interactive Web Visualizer

In addition to the CLI, an interactive web visualization widget is available at:
`maze_visualizer.html`

Open this file in any browser or in the Antigravity preview pane to interactively place obstacles, animate wavefront propagation, and visually inspect search frontiers in real time.

---

## 7. License

Distributed under the [MIT License](LICENSE)
