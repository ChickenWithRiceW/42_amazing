from src.config import loading_setup
from mazegen import MazeGenerator, write_maze
from src.display import render_maze

if __name__ == "__main__":
    cfg = loading_setup("config.txt")
    if not cfg:
        exit(0)
    gen = MazeGenerator(
        cfg.width,
        cfg.height,
        cfg.entry,
        cfg.exit,
        cfg.output_file,
        cfg.perfect,
        None   # ! keine seed attribute in Config bitte fixen danke
    )
    print(gen)
    gen.generate()
    print("\nGrid:", gen.grid, sep="\n")

    path = gen.solve()
    write_maze(gen)
    render_maze(gen, path, True, "magenta", "blue")
    print(gen.solution)
