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
pip install flake8 mypy pygame build
```

No external Python libraries are required to run the project (except for optional sound effects).

### Running the Program

```bash
python3 a_maze_ing.py config.txt
# or using the Makefile:
make run
```

### Configuration File Format

The program reads its parameters from a configuration file (e.g. `config.txt`). Below is the complete structure:

```
WIDTH=20              # (int, required) Number of columns in the maze. Must be ≥ 7.
HEIGHT=15             # (int, required) Number of rows in the maze. Must be ≥ 5.
ENTRY=0,0             # (x,y, required) Entry cell coordinates. Must differ from EXIT.
EXIT=19,14            # (x,y, required) Exit cell coordinates. Must differ from ENTRY.
OUTPUT_FILE=maze.txt  # (str, required) Path where the exported maze file will be saved.
PERFECT=True          # (bool, required) True for a perfect maze, False for a looped maze.
SEED=None             # (int or None, optional) Random seed for reproducibility. Defaults to None.
```

**Rules:**
- Lines starting with `#` are treated as comments and ignored and empty lines just ignored.
- `WIDTH` and `HEIGHT` must be positive integers.
- `ENTRY` and `EXIT` must have non-negative coordinates within bounds and different from each other.
- `PERFECT` must be `True` or `False` (case-insensitive).
- `SEED` can be any integer or `None`.

### Interactive Menu

Once the maze is displayed, the following options are available:

```
1. Re-generate a new maze (choose between DFS or BFS algorithm)
2. Show/Hide solution path from entry to exit
3. Rotate between color themes
4. Export the maze in hexadecimal format
5. Change configuration settings
6. Quit the program
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

When showing the solution (option `2`), the path is revealed progressively with a smooth animation before being displayed statically. For large mazes (HEIGHT > 95), only static display is available.

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

### Sound Effects

The program includes optional sound effects for:
- Error feedback (`assets/error.mp3`)
- Winning/solving a maze (`assets/win.mp3`)
- Program exit (`assets/bye.mp3`)

Sound playback requires `pygame` to be installed. If unavailable, the program continues without errors.

---

## Maze Generation Algorithm

### Algorithm: Depth-First Search (Recursive Backtracking) + Optional Loops

The maze is generated using **iterative depth-first search (DFS)** with a stack, also known as *recursive backtracking*. The steps are:

1. Start from the `ENTRY` cell and mark it as visited.
2. Randomly choose an unvisited neighbor and remove the wall between them.
3. Push the new cell onto the stack and continue.
4. When a cell has no unvisited neighbors, backtrack by popping from the stack.
5. Repeat until the stack is empty.

The **"42" pattern cells** are pre-marked as visited before generation starts, so the algorithm naturally routes corridors around them without passing through.

For **random (non-perfect) mazes**, after the full DFS pass, additional random walls are removed to introduce loops. The number of extra removals is proportional to `WIDTH + HEIGHT - 1`.

### Why DFS?

DFS was chosen for several reasons:
- It produces **long, winding corridors** with a natural aesthetic.
- It is **simple to implement** both recursively and iteratively.
- It generates **true perfect mazes** (spanning trees) by construction.
- The stack-based iterative version avoids Python's recursion depth limit, which would be hit on large mazes.
- It integrates cleanly with the "42" pattern by simply pre-marking those cells.
- Provides the best balance between **visual quality** and **computational simplicity**.

### Solving Algorithm: Breadth-First Search (BFS)

The maze is solved using **Breadth-First Search (BFS)** to find the shortest path from entry to exit. BFS guarantees the optimal solution and provides smooth animations due to its level-by-level exploration.

---

## Reusable Components

The project is structured as a Python package with clearly separated modules. Each component is independently usable:

| Module | Class | Reusable For |
|---|---|---|
| `Maze/generator.py` | `MazeGenerator` | Generating any grid-based maze with DFS. Accepts any config dict. |
| `Maze/solver.py` | `MazeSolver` | Solving any 2D grid maze using BFS. Takes a maze + dimensions + entry/exit. |
| `MazeUtils/parser.py` | `Parser` | Parsing key=value config files with type validation. |
| `MazeUtils/display.py` | `Display` | Terminal rendering of any Cell-based maze with ANSI colors. |
| `MazeUtils/exporter.py` | `Exporter` | Serializing maze data to hex format files. |

### Usage Examples

**To use the solver standalone:**

```python
from Maze.solver import MazeSolver

path = MazeSolver.solve_maze(maze, width, height, entry, exit)
```

**To use the generator standalone:**

```python
from Maze.generator import MazeGenerator

config = {"WIDTH": 20, "HEIGHT": 15, "ENTRY": (0,0), "EXIT": (19,14),
          "PERFECT": True, "SEED": 42}
gen = MazeGenerator(config)
gen.generate()
```

**To use the parser standalone:**

```python
from MazeUtils.parser import Parser

config = Parser.parse_config("config.txt")
```

---

## Team & Project Management

### Team Members and Roles

| Member | Role |
|---|---|
| **ncontrem** | Maze generation algorithm, generator module, "42" pattern integration, config parser |
| **efoyer** | Solver (BFS), display/rendering with ANSI themes, animated path, exporter, main interactive loop |

### Initial Planning vs. Actual Evolution

**Anticipated Planning:**
- **Week 1**: Define architecture, implement config parser and generator.
- **Week 2**: Implement solver and basic display.
- **Week 3**: Add export, themes, animation, and polish.

**How it Actually Evolved:**
- The **"42" pattern constraint** introduced complexity earlier than expected — pre-marking cells required careful handling to avoid disconnected maze regions.
- The **animated path feature** was added late but required a display refactoring (`path_override` parameter) to avoid code duplication.
- **Strict typing with `mypy`** added development overhead but significantly improved overall reliability and code maintainability.
- **Settings manager** was added to allow live configuration changes without restarting the program.
- **Sound effects** were integrated to enhance user experience (though optional).

### What Worked Well

✅ **Clear module separation** made parallel development straightforward and reduced merge conflicts.

✅ **BFS for solving** was a natural fit for finding the shortest path and provided fast computation.

✅ **Pre-marking the "42" pattern cells** before generation ensured they were naturally avoided during DFS without complex logic.

✅ **Type annotations** (with `mypy`) caught bugs early and made the codebase more maintainable.

### What Could Be Improved

🔧 **Animation performance** — The animated path currently re-renders the entire maze on each frame; a diff-based or cursor-positioning approach would be smoother.

🔧 **Additional generation algorithms** (e.g., Prim's, Kruskal's, Eller's) could be offered as config options for users who prefer different maze aesthetics.

🔧 **Large maze handling** — For very large mazes, the terminal rendering could be optimized with partial updates.

🔧 **Configuration hot-reload** could refresh the maze preview in real-time without requiring re-generation.

### Tools & Technologies Used

| Tool | Purpose |
|---|---|
| **Python 3.10+** | Main programming language |
| **flake8** | Style linting and code quality checks |
| **mypy** | Static type checking and type inference |
| **pygame** | Audio playback for sound effects |
| **Git** | Version control and collaboration |
| **Make** | Task automation (build, lint, run) |
| **ANSI escape codes** | Terminal color and cursor manipulation |

### AI Usage

**AI was used for the following tasks:**

1. **Algorithm understanding** — Helped clarify BFS concepts.
2. **Code standards compliance** — Provided guidance on `mypy` type annotations and `flake8` style conventions.
3. **Documentation** — Helped structure and improve README clarity and technical explanations.

---

## Resources

### Algorithmic References

- [Depth-first search — Wikipedia](https://en.wikipedia.org/wiki/Depth-first_search)
- [Breadth-first search — Wikipedia](https://en.wikipedia.org/wiki/Breadth-first_search)
- [Recursive backtracking — Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm#Recursive_backtracker)

### Technical References

- [ANSI escape codes — Wikipedia](https://en.wikipedia.org/wiki/ANSI_escape_code)
- [Python `typing` module documentation](https://docs.python.org/3/library/typing.html)
- [mypy documentation](https://mypy.readthedocs.io/)
- [flake8 documentation](https://flake8.pycqa.org/)

---

## Project Status

✅ **Complete and fully functional** with all required features implemented and tested.