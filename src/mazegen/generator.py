from enum import IntEnum
import random


class Wall(IntEnum):
    """Wall direction flags encoded as bit values.
    Each value represents one wall of a cell. Multiple walls are
    combined with bitwise OR. Bit 0=North, 1=East, 2=South, 3=West.
    """

    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8


OPPOSITE = {
    Wall.NORTH: Wall.SOUTH,
    Wall.SOUTH: Wall.NORTH,
    Wall.EAST: Wall.WEST,
    Wall.WEST: Wall.EAST
}

DELTA = {
    Wall.NORTH: (-1, 0),
    Wall.SOUTH: (1, 0),
    Wall.EAST: (0, 1),
    Wall.WEST: (0, -1)
}


class MazeGenerator:
    """Generates a 2D maze using the recursive backtracker algorithm.
    Args:
        width: Number of columns.
        height: Number of rows.
        entry: Entry cell coordinates as (x, y).
        exit: Exit cell coordinates as (x, y).
        output_file: Path to write the maze output.
        perfect: If True, generates a perfect maze
        seed: Random seed for reproducibility. None picks a random seed.
    Attributes:
        grid: 2D list of ints encoding wall state per cell.
    """

    def __init__(
            self,
            width: int,
            height: int,
            entry: tuple[int, int],
            exit: tuple[int, int],
            output_file: str,
            perfect: bool,
            seed: int | None
            ) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.output_file = output_file
        self.perfect = perfect
        self.seed = seed

    def generate(self) -> None:
        """Generate the maze grid using recursive backtracker (iterative DFS).
        Seeds the random generator, initialises all cells as fully walled,
        then carves passages until all cells are visited. Sets self.grid.
        """

        random.seed(self.seed)
        self.grid = [[0xF] * self.width for _ in range(self.height)]

        visited: set[tuple[int, int]] = set()
        start_col, start_row = self.entry
        stack: list[tuple[int, int]] = [(start_row, start_col)]
        visited.add((start_row, start_col))

        while stack:
            row, col = stack[-1]

            # Find all valid unvisited neighbours
            neighbours = self._find_neighbours(row, col, visited)
            if neighbours:
                # Pick a random neighbour
                direction, new_row, new_col = random.choice(neighbours)

                # Remove a wall between current cell and chosen neighbour
                self.grid[row][col] &= ~direction
                self.grid[new_row][new_col] &= ~OPPOSITE[direction]

                # Mark neighbour visited and push onto stack
                visited.add((new_row, new_col))
                stack.append((new_row, new_col))
            else:
                # Backtrack
                stack.pop()

    def _find_neighbours(
            self, row: int, col: int, visited: set[tuple[int, int]]
            ) -> list[tuple[Wall, int, int]]:
        """Return valid unvisited neighbours of a cell.
        Args:
            row: Row index of the current cell.
            col: Column index of the current cell.
            visited: Set of already visited (row, col) positions.
        Returns:
            List of tuples for each valid neighbour.
        """

        neighbours: list[tuple[Wall, int, int]] = []
        for direction, (dr, dc) in DELTA.items():
            new_row = row + dr
            new_col = col + dc
            # Must be inside the grid and not visited yet
            if (0 <= new_row < self.height
                    and 0 <= new_col < self.width
                    and (new_row, new_col) not in visited):
                neighbours.append((direction, new_row, new_col))
        return neighbours

    def __str__(self) -> str:
        is_perfect = "Perfect" if self.perfect else "Not perfect"
        return (
            f"Width:\t{self.width}\n"
            f"Height:\t{self.height}\n"
            f"Entry:\t{self.entry}\n"
            f"Exit:\t{self.exit}\n"
            f"File:\t{self.output_file}\n"
            f"Type:\t{is_perfect}\n"
            f"Seed:\t{self.seed}\n"
        )
