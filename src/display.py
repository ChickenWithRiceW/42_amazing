from rich.console import Console
from src.mazegen import MazeGenerator
from src.mazegen.generator import Wall

console = Console()

WALL_COLORS = ["white", "cyan", "yellow", "green"]


def render_maze(
        gen: MazeGenerator,
        show_path: bool = False,
        wall_color: str = "white"
) -> None:
    """Render the maze to the terminal using rich colored blocks."""
    # Top wall
    for row in range(gen.height):
        for col in range(gen.width):
            console.print("█", end="")  # corner
            if gen.grid[row][col] & Wall.NORTH:
                console.print("██", end="")
            else:
                console.print("  ", end="")
        console.print("█")  #right border + newline

        # Side wall + interior
        for col in range(gen.width):
            if gen.grid[row][col] & Wall.WEST:
                console.print("█", end="")
            else:
                console.print(" ", end="")
            console.print("  ", end="")
        console.print("█")  # Right border + newline
    for col in range(gen.width):
        console.print("███", end="")
    console.print("█")  # Bottom right corner

def run_display(gen: MazeGenerator) -> None:
    """Run the interactive display loop"""
    pass
