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
    Wall.NORTH: (0, -1),
    Wall.SOUTH: (0, 1,),
    Wall.EAST: (1, 0),
    Wall.WEST: (-1, 0)
}

PATTERN: list[list[str]] = [
    ['X', ' ', 'X', ' ', 'X', 'X', 'X'],
    ['X', ' ', 'X', ' ', ' ', ' ', 'X'],
    ['X', 'X', 'X', ' ', 'X', 'X', 'X'],
    [' ', ' ', 'X', ' ', 'X', ' ', ' '],
    [' ', ' ', 'X', ' ', 'X', 'X', 'X']
]
PATTERN_WIDTH = 7
PATTERN_HEIGHT = 5


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

        if width < 2 or height < 2:
            raise ValueError(
                f"Width and height must be at least 2, got '{width}x{height}'"
            )
        if not (0 <= entry[0] < width and 0 <= entry[1] < height):
            raise ValueError(
                f"Entry {entry} is out of bounds for a '{width}x{height}' maze"
            )
        if not (0 <= exit[0] < width and 0 <= exit[1] < height):
            raise ValueError(
                f"Exit {exit} is out of bounds for a '{width}x{height}' maze"
            )
        if entry == exit:
            raise ValueError("Entry and exit cannot be the same cell")

        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.output_file = output_file
        self.perfect = perfect
        self.seed = seed
        self.grid: list[list[int]] = []
        self.solution: list[str] = []

    def generate(self) -> None:
        """Generate the maze grid using recursive backtracker (iterative DFS).
        Seeds the random generator, initializes all cells as fully walled,
        then carves passages until all cells are visited. Sets self.grid.
        """

        random.seed(self.seed)
        self.grid = [[0xF] * self.width for _ in range(self.height)]

        blocked: set[tuple[int, int]] = set()
        if self._check_pattern_fits():
            self._stamp_pattern(blocked)

        visited: set[tuple[int, int]] = set()
        start_x, start_y = self.entry
        stack: list[tuple[int, int]] = [(start_x, start_y)]
        visited.add((start_x, start_y))

        while stack:
            x, y = stack[-1]

            # Find all valid unvisited neighbours
            neighbours = self._find_neighbours(x, y, visited, blocked)
            if neighbours:
                # Pick a random neighbour
                direction, new_x, new_y = random.choice(neighbours)

                # Remove a wall between current cell and chosen neighbour
                self.grid[y][x] &= ~direction
                self.grid[new_y][new_x] &= ~OPPOSITE[direction]

                # Mark neighbour visited and push onto stack
                visited.add((new_x, new_y))
                stack.append((new_x, new_y))
            else:
                # Backtrack
                stack.pop()

        if not self.perfect:
            self._add_loops(blocked)

    def solve(self) -> list[tuple[int, int]]:
        from .solver import Solver

        solve_instance = Solver(self)
        return solve_instance.solver(self.entry, self.exit)

    def _find_neighbours(
            self, x: int, y: int,
            visited: set[tuple[int, int]],
            blocked: set[tuple[int, int]]
            ) -> list[tuple[Wall, int, int]]:
        """Return valid unvisited neighbours of a cell.
        Also checks for a blocked cells if they are set.
        Args:
            x: Column index of the current cell.
            y: Row index of the current cell.
            visited: Set of already visited (x, y) positions.
            blocked: Set of blocked cells (cannot open any wall)
        Returns:
            List of tuples for each valid neighbour.
        """

        neighbours: list[tuple[Wall, int, int]] = []
        for direction, (dx, dy) in DELTA.items():
            new_x = x + dx
            new_y = y + dy
            # Must be inside the grid and not visited yet
            if (0 <= new_y < self.height
                    and 0 <= new_x < self.width
                    and (new_x, new_y) not in visited
                    and (new_x, new_y) not in blocked):
                neighbours.append((direction, new_x, new_y))
        return neighbours

    def _check_pattern_fits(self) -> bool:
        """Check if the maze is large enough to fit the 42 pattern.
        Returns:
            True if the pattern fits, False otherwise.
        """

        if (self.width - 2 >= PATTERN_WIDTH
                and self.height - 2 >= PATTERN_HEIGHT):
            return True
        print("\n=== 42 pattern doesn't fit ===\n")
        return False

    def _stamp_pattern(self, blocked: set[tuple[int, int]]) -> None:
        """Populate the blocked set with cells forming the 42 pattern.
        Calculates the centered position and marks all pattern cells
        as blocked so the generator routes around them.
        Args:
            blocked: Set to populate with (x, y)
            positions of pattern cells.
        """

        start_x = (self.width - PATTERN_WIDTH) // 2
        start_y = (self.height - PATTERN_HEIGHT) // 2

        for y, row in enumerate(PATTERN):
            for x, cell in enumerate(row):
                if cell == 'X':
                    blocked.add((start_x + x, start_y + y))

    def _add_loops(self, blocked: set[tuple[int, int]]) -> None:
        candidates = []
        for y in range(self.height - 1):
            for x in range(self.width):
                if (x, y) not in blocked and (x, y+1) not in blocked:
                    if self.grid[y][x] & Wall.SOUTH:
                        candidates.append((x, y, Wall.SOUTH))

        for y in range(self.height):
            for x in range(self.width - 1):
                if (x, y) not in blocked and (x+1, y) not in blocked:
                    if self.grid[y][x] & Wall.EAST:
                        candidates.append((x, y, Wall.EAST))

        random.shuffle(candidates)

        target = len(candidates) // 7
        removed = 0

        for x, y, direction in candidates:
            if removed >= target:
                break

            dx, dy = DELTA[direction]
            nx, ny = x + dx, y + dy

            self.grid[y][x] &= ~direction
            self.grid[ny][nx] &= ~OPPOSITE[direction]

            # Check all nearby 3x3 blocks
            created_open_area = False
            for by in range(max(0, y - 2), min(self.height - 2, y + 1)):
                for bx in range(max(0, x - 2), min(self.width - 2, x + 1)):
                    if self._creates_3x3_area(bx, by):
                        created_open_area = True
                        break
                if created_open_area:
                    break

            if created_open_area:
                # UNDO
                self.grid[y][x] |= direction
                self.grid[ny][nx] |= OPPOSITE[direction]
            else:
                removed += 1

    def _creates_3x3_area(self, bx: int, by: int) -> bool:
        """Return True if the 3x3 block at (bx, by) is fully open"""
        for y in range(by, by + 3):
            for x in range(bx, bx + 2):
                if self.grid[y][x] & Wall.EAST:
                    return False
        for y in range(by, by + 2):
            for x in range(bx, bx + 3):
                if self.grid[y][x] & Wall.SOUTH:
                    return False
        return True

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
