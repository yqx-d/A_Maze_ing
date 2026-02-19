*This project has been created as part of the 42 curriculum by ncontrem, efoyer.*

---

# 🌀 A-Maze-ing

## Description

**A-Maze-ing** is an interactive terminal-based maze generator and solver. The program generates mazes with a unique twist: the **"42" pattern** is embedded at the center of every maze as a visual easter egg, rendered using fully walled cells.

The project supports two maze modes:
- **Perfect mazes**: a single unique path exists between entry and exit (a proper spanning tree).
- **Random mazes**: multiple loops are introduced, creating alternative routes and a more complex structure.

Once generated, the maze can be displayed with color themes, solved with an animated path visualization, and exported to a hexadecimal file format.

---

## Instructions

### Requirements

- Python 3.10 or higher
- Optional linting tools: `flake8`, `mypy`, `pygame`, `build`

### Installation

```bash
# Install optional linting tools
make install
# or manually:
pip install flake8 mypy
```

No external Python libraries are required to run the project.

### Running the Program

```bash
python3 a_maze_ing.py config.txt
# or using the Makefile:
make run
```

### Configuration File Format

The program reads its parameters from a configuration file (e.g. `config.txt`). Below is the complete structure:

```
WIDTH=20          # (int, required) Number of columns in the maze. Must be ≥ 7.
HEIGHT=15         # (int, required) Number of rows in the maze. Must be ≥ 5.
ENTRY=0,0         # (x,y, required) Entry cell coordinates. Must differ from EXIT.
EXIT=19,14        # (x,y, required) Exit cell coordinates. Must differ from ENTRY.
OUTPUT_FILE=maze.txt  # (str, required) Path where the exported maze file will be saved.
PERFECT=True      # (bool, required) True for a perfect maze, False for a looped maze.
SEED=None         # (int or None, optional) Random seed for reproducibility. Defaults to None.
```

Rules:
- Lines starting with `#` are treated as comments and ignored.
- `WIDTH` and `HEIGHT` must be positive integers.
- `ENTRY` and `EXIT` must have non-negative coordinates within bounds.
- `PERFECT` must be `True` or `False` (case-insensitive).
- `SEED` can be any integer or `None`.

### Interactive Menu

Once the maze is displayed, the following options are available:

```
1. Re-generate a new maze
2. Show/Hide path from entry to exit
3. Rotate maze colors
4. Export the maze in hexadecimal format
5. Quit
```

### Linting

```bash
make lint         # Standard linting (flake8 + mypy)
make lint-strict  # Strict mypy check
```

---

## Features

### Color Themes

Four color themes are available and can be cycled with option `3`:
- `DEFAULT` — White walls, green path
- `BLUE` — Blue walls, cyan path
- `YELLOW` — Yellow walls, white path
- `PURPLE` — Purple walls, cyan path

### Animated Path

When showing the solution (option `2`), the path is revealed progressively with a smooth animation before being displayed statically.

### Export Format

Option `4` exports the maze to the configured `OUTPUT_FILE` in the following format:

```
<hex grid>     One character per cell, each a hex digit (0–F) encoding wall state.
               Bits (LSB to MSB): North, East, South, West (1=closed, 0=open).

<blank line>

<entry_x>,<entry_y>
<exit_x>,<exit_y>
<path_directions>   e.g. EESSSWWNN... using N, E, S, W characters.
```

---

## Maze Generation Algorithm

### Algorithm: Depth-First Search (Recursive Backtracking)

The maze is generated using **iterative depth-first search (DFS)** with a stack, also known as *recursive backtracking*. The steps are:

1. Start from the `ENTRY` cell and mark it as visited.
2. Randomly choose an unvisited neighbor and remove the wall between them.
3. Push the new cell onto the stack and continue.
4. When a cell has no unvisited neighbors, backtrack by popping from the stack.
5. Repeat until the stack is empty.

The **"42" pattern cells** are pre-marked as visited before generation starts, so the algorithm naturally routes corridors around them without passing through.

For **random (non-perfect) mazes**, after the full DFS pass, additional random walls are removed to introduce loops. The number of extra removals is proportional to `WIDTH + HEIGHT - 1`.

### Why this algorithm?

DFS was chosen for several reasons:
- It produces **long, winding corridors** with a natural aesthetic.
- It is **simple to implement** both recursively and iteratively.
- It generates **true perfect mazes** (spanning trees) by construction.
- The stack-based iterative version avoids Python's recursion depth limit, which would be hit on large mazes.
- It integrates cleanly with the "42" pattern by simply pre-marking those cells.

---

## Reusable Components

The project is structured as a Python package (`Maze/`) with clearly separated modules. Each component is independently usable:

| Module | Class | Reusable for |
|---|---|---|
| `Maze/generator.py` | `MazeGenerator` | Generating any grid-based maze with DFS. Accepts any config dict. |
| `Maze/solver.py` | `MazeSolver` | Solving any 2D grid maze using BFS. Takes a maze + dimensions + entry/exit. |
| `Maze/parser.py` | `Parser` | Parsing key=value config files with type validation. |
| `Maze/display.py` | `Display` | Terminal rendering of any Cell-based maze with ANSI colors. |
| `Maze/exporter.py` | `Exporter` | Serializing maze data to hex format files. |

To use the solver standalone, for example:

```python
from Maze.solver import MazeSolver

path = MazeSolver.solve_maze(maze, width, height, entry, exit)
```

To use the generator standalone:

```python
from Maze.generator import MazeGenerator

config = {"WIDTH": 20, "HEIGHT": 15, "ENTRY": (0,0), "EXIT": (19,14),
          "PERFECT": True, "SEED": 42}
gen = MazeGenerator(config)
gen.generate()
```

---

## Team & Project Management

### Team Members

| Member | Role |
|---|---|
| **ncontrem** | Maze generation algorithm, generator module, "42" pattern integration, config parser |
| **efoyer** | Solver (BFS), display/rendering with ANSI themes, animated path, exporter, main loop |

### Planning

**Initial plan:**
- Week 1: Define architecture, implement config parser and generator.
- Week 2: Implement solver and basic display.
- Week 3: Add export, themes, animation, polish.

**How it evolved:**
- The "42" pattern constraint introduced complexity earlier than expected — pre-marking cells required careful handling to avoid disconnected maze regions.
- The animated path feature was added late but required a display refactoring (`path_override` parameter) to avoid code duplication.
- Strict typing with `mypy` added some development overhead but improved overall reliability.

### What Worked Well

- Clear module separation made parallel development easy.
- BFS for solving was a natural fit and was implemented quickly.
- The `path_override` abstraction allowed both static and animated display to share one rendering function.

### What Could Be Improved

- The entry/exit validation could enforce boundary constraints more strictly.
- The animation currently re-renders the entire maze on each frame; a diff-based approach would be smoother.
- Multiple generation algorithms (e.g. Prim's, Kruskal's) could be offered as a config option.
- Unit tests would improve confidence when refactoring.

### Tools Used

- **Python 3.10+** — Main language
- **flake8** — Style linting
- **mypy** — Static type checking
- **Git** — Version control
- **Make** — Task automation
- **AI** — Used for:
  - Help understanding the algorithm
  - Help with complying with standards
  - Debugging during complex situations

---

## Resources

- [Depth-first search — Wikipedia](https://en.wikipedia.org/wiki/Depth-first_search)
- [Breadth-first search — Wikipedia](https://en.wikipedia.org/wiki/Breadth-first_search)
- [ANSI escape codes — Wikipedia](https://en.wikipedia.org/wiki/ANSI_escape_code)
- [Python `typing` module documentation](https://docs.python.org/3/library/typing.html)
- [mypy documentation](https://mypy.readthedocs.io/)