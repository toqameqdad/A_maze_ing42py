*This activity has been created as part of
the 42 curriculum by tobaidat tmeqdad*

# Maze Project

## Description
This project is an interactive maze generation and solving application developed in Python.
The primary goal of the activity is to generate perfect or imperfect, fully-connected mazes dynamically and compute their optimal paths from a specified entry point to an exit point.
The project emphasizes clean code architecture, efficient graph traversal algorithms, strict type safety, and robust visualization within the terminal using ANSI escape sequences.

## Instructions
- make : To compile all files and build the virtual environment
- make run : Generate the maze and show menu
- make instal :  Install activity dependencies using pip
- make debug :  Run the main script in debug mode using Python’s built-in debugger (pdb)
- make lint : flake8 . and mypy . --warn-return-any --warn-unused-ignores
--ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
- make lint-strict : flake8 . and mypy . --strict
- make clean :  Remove temporary files or caches (e.g., __pycache__, .mypy_cache) to keep
the activity environment clean.

## Additional
- The complete format of config file : KEY=VALUE
for example:
WIDTH=20                    # Maze width (number of cells)
HEIGHT=15                   # Maze height
ENTRY=0,0                   # Entry coordinates (x,y)
EXIT=19,14                  # Exit coordinates (x,y)
OUTPUT_FILE=maze.txt        # Output filename
PERFECT = True              # Is the maze perfect?

- The maze generation algorithm we chose:
(Depth-First Search) to generate the maze
- Why DFS for Maze Generation?
DFS (Depth-First Search) goes as deep as possible down one path before backtracking. This naturally creates long, winding, and complex passages, which makes for a great, challenging maze.
(Breadth-First Search) to find the shortest path
- Why BFS for Finding the Shortest Path?
Because it explores uniformly, the first time BFS reaches the exit, it is guaranteed to have found the absolute shortest path in an unweighted maze. DFS, on the other hand, might just find a random, highly convoluted path first.

## Reusable Maze Generator Package (`mazegen`)

The maze generation core has been implemented as a standalone, reusable Python package called `mazegen`. This package is designed to be easily bundled, installed via `pip`, and integrated into future projects.

The pre-built package files (e.g., `mazegen-1.0.0-py3-none-any.whl`) are located at the root of this repository along with all necessary build configurations (`pyproject.toml` or `setup.py`).

#### 1. Installation
To install the package locally from the build files at the root of the repository, run:
```bash
pip install mazegen-1.0.0-py3-none-any.whl
```
#### 2. How to Rebuild the Package
To verify the build or compile the source code into package distributions again, follow these steps in a clean virtual environment:

Install the standard Python build tool:

```bash
pip install build
Run the build command from the root of the repository:
```
```bash
python -m build
```
This will regenerate the .tar.gz and .whl files inside the dist/ folder.

## Team and Project Management

1. Roles of each team member:
* **tobaidat** : ASCII rendering , Generate imperfect maze, Output file, MakeFile, Build Package
* **tmeqdad** : Generate perfect maze, Solve the maze, Validate config file, Handling the edge cases

2. Anticipated planning and how it evolved until the end:
**Initial Plan:** We originally planned to complete the entire project in approximately two weeks, assuming the setup and error-handling would be straightforward.
**How it Evolved:** The project timeline extended to about a month. This happened for two main reasons: 
  * 1. We spent a significant amount of time studying how to properly build and package a reusable Python library (`.whl` and `.tar.gz`).
  * 2. We decided to build a highly robust system, which required us to anticipate and handle every possible user error or edge case within the configuration files and input arguments.
### 3. Retrospective (What Worked vs. What Could Be Improved)
* **What Worked Well:** 
  * **Exceptional Teamwork:** Our collaboration was incredibly smooth. We communicated seamlessly throughout the month, which made resolving complex bugs much easier.
  * **Fair Task Distribution:** Tasks were divided equally and comfortably based on everyone's strengths, ensuring no single member was overwhelmed.
* **What Could Be Improved:** 
  * **UI/Visuals Trade-off:** We initially wanted to implement a graphical display using the **MiniLibX (MLX)** library. However, due to time constraints and the core requirements, we realized that an **ASCII rendering** was much more straightforward to implement and perfectly served the project's purpose. In the future, we would allocate time early on to integrate a full graphical interface.

### 4. Tools Used
* **GitHub:** Our primary tool for collaboration. It allowed us to share files seamlessly, track changes, review each other's code, and work on different features concurrently without losing progress.


## Resources
- https://www.kufunda.net/publicdocs/Mazes%20for%20Programmers%20Code%20Your%20Own%20Twisty%20Little%20Passages%20(Jamis%20Buck).pdf
- Gemini AI : learning the algorithms and the ASCII rendering
