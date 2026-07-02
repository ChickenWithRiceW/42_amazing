from src.config import loading_setup
from mazegen import MazeGenerator, write_maze

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
        42   # ! keine seed attribute in Config bitte fixen danke
    )
    print(gen)
    gen.generate()
    print("\nGrid:", gen.grid, sep="\n")
    write_maze(gen, ['P', 'E', 'N', 'I', 'S'])
