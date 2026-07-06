from rich.console import Console
from mazegen import MazeGenerator
from mazegen.generator import Wall
from mazegen.solver import Solver, NoSolutionError
from mazegen.output import write_maze

console = Console()

WALL_COLORS = ["white", "cyan", "yellow", "green"]


def render_maze(
        gen: MazeGenerator,
        path: list[tuple[int, int]],
        show_path: bool = False,
        wall_color: str = "white",
        path_color: str = "blue",
        entry_color: str = "red",
        exit_color: str = "green"
) -> None:
    """Render the maze to the terminal using rich colored blocks."""

    for row in range(gen.height):
        for col in range(gen.width):
            console.print("█", end="", style=wall_color)  # corner
            if gen.grid[row][col] & Wall.NORTH:
                console.print("██", end="", style=wall_color)
            else:
                # Printing path
                if show_path and (col, row) in path and (col, row - 1) in path:
                    console.print("██", end="", style=path_color)
                else:
                    console.print("  ", end="")

        console.print("█", style=wall_color)  # right border + newline

        # Side wall + interior
        for col in range(gen.width):
            if gen.grid[row][col] & Wall.WEST:
                console.print("█", end="", style=wall_color)
            else:
                # Printing path
                if show_path and (col, row) in path and (col - 1, row) in path:
                    console.print("█", end="", style=path_color)
                else:
                    console.print(" ", end="")

            # Checks if we can draw a normal path or set a entry/exit
            if (col, row) not in path:
                console.print("  ", end="")
            else:
                # Entry
                if (col, row) == path[0]:
                    console.print("██", end="", style=entry_color)
                # Exit
                elif (col, row) == path[-1]:
                    console.print("██", end="", style=exit_color)
                # Path
                elif show_path:
                    console.print("██", end="", style=path_color)
                else:
                    console.print("  ", end="")
        console.print("█", style=wall_color)  # Right border + newline

    # Printing bottom row
    for col in range(gen.width):
        console.print("███", end="", style=wall_color)
    console.print("█", style=wall_color)  # Bottom right corner


def _solve_maze(gen: MazeGenerator) -> list[tuple[int, int]]:
    try:
        solver = Solver(gen)
        path = solver.solver(gen.entry, gen.exit)
    except NoSolutionError as e:
        print(f"Error: {e}")
        path = []

    return path


def run_display(gen: MazeGenerator) -> None:
    """Run the interactive display loop"""
    path_color = "blue"
    show_path = True
    path = _solve_maze(gen)
    write_maze(gen)

    color = 0
    while True:
        render_maze(gen, path, show_path, WALL_COLORS[color], path_color)
        console.print(
            "[1] Regenerate  [2] Toggle path  [3] Wall color  [q] Quit"
        )
        choice = input("> ").strip().lower()

        if choice == "q":
            break
        elif choice == "1":
            gen.generate()
            path = _solve_maze(gen)
            write_maze(gen)
        elif choice == "2":
            show_path = not show_path
        elif choice == "3":
            color = (color + 1) % len(WALL_COLORS)
