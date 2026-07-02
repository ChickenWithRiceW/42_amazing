from . import MazeGenerator


def write_maze(gen: MazeGenerator, solution: list[str]) -> None:
    with open(gen.output_file, mode="w") as f:
        grid = '\n'.join(
            ''.join(format(cell, 'X') for cell in row) for row in gen.grid)
        entry = f"\n{gen.entry[0]},{gen.entry[1]}\n"
        exit_str = f"{gen.exit[0]},{gen.exit[1]}\n"
        path = ''.join(solution) + '\n'

        output = grid + '\n' + entry + exit_str + path
        f.write(output)
