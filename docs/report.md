# Technical Report: BFS Maze Solver & Search Optimality

**Domain**: Uninformed Search / Graph Traversal  
**Algorithm**: Breadth-First Search (BFS)  
**Cost Model**: Uniform-Cost Grid (\(c(e) = 1\) for all orthogonal transitions)

---

## 1. Problem Definition & Objectives

Given a 2D grid of size \(R \times C\) with:
- Start coordinate \(S = (r_s, c_s)\),
- Goal coordinate \(G = (r_g, c_g)\),
- Obstacle set \(W \subset \{ (r, c) \mid 0 \le r < R, 0 \le c < C \}\),

The objective is to find a path \(p = (v_0, v_1, \dots, v_k)\) such that:
1. \(v_0 = S\) and \(v_k = G\),
2. Each transition \((v_i, v_{i+1})\) is a valid orthogonal step (Up, Down, Left, Right),
3. No vertex in \(p\) lies in \(W\),
4. The path length \(k\) is strictly minimized: \(k = \min_{p'} |p'|\).

---

## 2. Theoretical Proof of BFS Optimality on Uniform-Cost Grids

### 2.1 Uniform Transition Cost
In standard grid pathfinding with orthogonal connectivity, every step between adjacent cells incurs uniform cost:
\[
c(u, v) = 1, \quad \forall (u, v) \in E
\]

### 2.2 FIFO Queue Invariant
Let \(Q\) denote the FIFO queue maintained by BFS. Let \(\text{dist}(S, v)\) be the length of the shortest path from \(S\) to \(v\).
At any point during the execution of BFS:
1. If the vertices currently in \(Q\) are \((v_1, v_2, \dots, v_m)\), then:
   \[
   \text{dist}(S, v_1) \le \text{dist}(S, v_2) \le \dots \le \text{dist}(S, v_m)
   \]
2. Furthermore:
   \[
   \text{dist}(S, v_m) - \text{dist}(S, v_1) \le 1
   \]
   That is, the queue contains vertices from at most two consecutive distance layers: \(d\) and \(d + 1\).

### 2.3 Monotonic Expansion Property
Because vertices are dequeued from the front of \(Q\), the sequence of expanded vertices has non-decreasing distance:
\[
d_1 \le d_2 \le d_3 \le \dots \le d_k
\]

### 2.4 First-Visit Optimality Guarantee
When the Goal node \(G\) is first removed from the FIFO queue (or first discovered on layer \(d^*\)):
- Any vertex \(u\) remaining in the frontier \(Q\) satisfies \(\text{dist}(S, u) \ge d^*\).
- Any path to \(G\) that has not yet been explored must pass through some node on the frontier.
- Since all edge costs are \(c = 1 \ge 0\), the cost of any alternate path is:
  \[
  \text{cost}(p') = \text{dist}(S, u) + \text{dist}(u, G) \ge d^* + 0 = d^*
  \]
Therefore, no shorter path can exist. BFS is mathematically guaranteed to return the optimal (shortest) path.

---

## 3. Empirical Benchmark: BFS vs DFS

To empirically demonstrate optimality, we compared BFS against Depth-First Search (DFS) on identical maze topologies:

| Maze Preset | Dimensions | BFS Path Length (Optimal) | DFS Path Length (Uninformed) | Difference (DFS Extra Steps) | Suboptimality Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `simple` | \(5 \times 5\) | **14** | 14 | +0 | 1.0x (Tie) |
| `branching_choice` | \(6 \times 7\) | **12** | 16 | +4 | 1.33x longer |
| `dfs_trap` | \(5 \times 11\) | **4** | 32 | +28 | **8.0x longer** |
| `labyrinth` | \(21 \times 11\) | **34** | 34 | +0 | 1.0x (Tie) |

### Key Insight
In `dfs_trap`, Start \((0,0)\) and Goal \((4,0)\) are separated by just 4 vertical steps. However, DFS greedily pushes along the upper horizontal corridor, falls into the outer perimeter loop, and wanders for **32 steps** before reaching Goal. BFS radiates outwards in concentric layers, identifying the 4-step path immediately.

---

## 4. Visual Artifacts

Generated plots located in `docs/plots/`:
1. `bfs_vs_dfs_comparison.png`: Path length bar chart comparing BFS and DFS across presets.
2. `wavefront_distance_heatmap.png`: Heatmap of distance layers and the optimal path overlay.
3. `layer_expansion.png`: Frequency distribution of nodes expanded per distance layer.
4. `report.pdf`: Printable multi-page PDF compilation.
