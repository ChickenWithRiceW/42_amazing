from rich.console import Console
from mazegen import MazeGenerator
from mazegen.generator import Wall

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
                    console.print("  ", end="", style=wall_color)

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
                    console.print(" ", end="", style=wall_color)

            # Checks if we can draw a normal path or set a entry/exit
            if (col, row) not in path:
                console.print("  ", end="", style=wall_color)
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
                    console.print("  ", end="", style=wall_color)
        console.print("█", style=wall_color)  # Right border + newline

    # Printing bottom row
    for col in range(gen.width):
        console.print("███", end="", style=wall_color)
    console.print("█", style=wall_color)  # Bottom right corner


def run_display(gen: MazeGenerator) -> None:
    """Run the interactive display loop"""
    pass
