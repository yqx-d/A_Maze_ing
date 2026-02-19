# MazeGen 1.0.0 - Installation & Usage Guide

**MazeGen** is a Python package for generating and solving mazes with advanced features including perfect/random maze generation, solution visualization, and multiple color themes.

---

## Package Information

| Property | Details |
|---|---|
| **Package Name** | `mazegen` |
| **Version** | 1.0.0 |
| **Archive** | `mazegen-1.0.0-py3-none-any.whl` |
| **Python Requirement** | 3.10 or higher |
| **Authors** | ncontrem, efoyer |

---

## Installation

### Prerequisites

Ensure you have Python 3.10+ installed:

```bash
python3 --version
```

### Step 1: Install the Package with pip

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

### Step 2: (Optional) Install Development Tools

```bash
pip install flake8 mypy
```

**Component Details:**
- `flake8` — Code linting and style checking
- `mypy` — Static type checking

### Step 3: Verify Installation

```bash
python3 -c "from Maze.generator import MazeGenerator; print('✓ MazeGen installed successfully!')"
```

---

## Quick Start

### Running the Interactive Program

After installation, you can run the maze generator with:

```bash
python3 a_maze_ing.py config.txt
```

### Example Configuration File

Create a `config.txt` with the following content:

```
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42
```

### Configuration Options

| Parameter | Type | Required | Description | Example |
|---|---|---|---|---|
| `WIDTH` | int | Yes | Number of maze columns (≥ 7) | `20` |
| `HEIGHT` | int | Yes | Number of maze rows (≥ 5) | `15` |
| `ENTRY` | x,y | Yes | Entry point coordinates | `0,0` |
| `EXIT` | x,y | Yes | Exit point coordinates | `19,14` |
| `OUTPUT_FILE` | str | Yes | File path for exported maze | `maze.txt` |
| `PERFECT` | bool | Yes | True for perfect maze, False for looped | `True` |
| `SEED` | int or None | No | Random seed for reproducibility | `42` or `None` |

---

## Using MazeGen as a Library

### Generate a Maze Programmatically

```python
from Maze.generator import MazeGenerator
from MazeUtils.display import Display

# Configure the maze
config = {
    "WIDTH": 30,
    "HEIGHT": 20,
    "ENTRY": (0, 0),
    "EXIT": (29, 19),
    "PERFECT": True,
    "SEED": 123,
    "OUTPUT_FILE": "my_maze.txt"
}

# Generate
gen = MazeGenerator(config)
gen.generate()

# Display with theme
Display.show_maze(gen.maze, config["WIDTH"], config["HEIGHT"], theme="BLUE")

# Solve and export
path = MazeGenerator.solve_maze(
    gen.maze,
    config["WIDTH"],
    config["HEIGHT"],
    config["ENTRY"],
    config["EXIT"]
)
MazeGenerator.export_to(gen.maze, config)
```

### Parse Configuration Files

```python
from MazeUtils.parser import Parser

config = Parser.parse_config("config.txt")
print(f"Maze size: {config['WIDTH']}x{config['HEIGHT']}")
```

### Generate Different Maze Types

**Perfect Maze (Single Path):**
```python
config["PERFECT"] = True
gen = MazeGenerator(config)
gen.generate()
```

**Random Maze (Multiple Paths):**
```python
config["PERFECT"] = False
gen = MazeGenerator(config)
gen.generate()
```

---

## Available Color Themes

The interactive program supports four color themes (cycle with option `3`):

| Theme | Wall Color | Path Color | Description |
|---|---|---|---|
| `DEFAULT` | White | Green | Classic terminal colors |
| `BLUE` | Blue | Cyan | Cool blue tones |
| `YELLOW` | Yellow | White | Warm yellow tones |
| `PURPLE` | Purple | Cyan | Dark purple aesthetic |

---

## Interactive Menu Options

Once the maze is displayed:

```
1. Re-generate a new maze (DFS or BFS algorithm)
2. Show/Hide solution path
3. Rotate color themes
4. Export maze to hexadecimal format
5. Change configuration settings
6. Quit the program
```

---

## Export Format

When exporting (option `4`), the maze is saved in hexadecimal format:

```
<hex grid>         One character per cell (0–F).
                   Bits: North, East, South, West (1=wall closed, 0=open).

<blank line>

<entry_x>,<entry_y>
<exit_x>,<exit_y>
<path_directions>   Movement sequence: N, E, S, W characters.
```

**Example exported maze file:**
```
FFF9FFFF
F0F0F0F1
F0F0F0F1
F0F0F0F1
F0F0F0F1
FFF0FFF3

0,0
7,5
EESSSWWNN
```

---

### Issue: Configuration file parsing errors

**Ensure `config.txt` follows the correct format:**
- No spaces around `=` (use `WIDTH=20`, not `WIDTH = 20`)
- Comments start with `#` and are ignored
- Empty lines are allowed
- ENTRY and EXIT must be different coordinates

---

## Maze Generation Algorithm

**MazeGen uses Depth-First Search (DFS)** with iterative backtracking:

1. Start from the entry point
2. Randomly choose unvisited neighbors
3. Remove walls to connect cells
4. Backtrack when stuck
5. Complete when all cells are visited

For **random (non-perfect) mazes**, additional walls are randomly removed after DFS to create loops and alternative paths.

---

## Maze Solving Algorithm

**MazeGen uses Breadth-First Search (BFS)** to find the optimal path from entry to exit:

- Guarantees the shortest path
- Provides smooth animation for large mazes
- O(width × height) time complexity
