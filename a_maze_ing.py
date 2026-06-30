from src.config import loading_setup
from mazegen import MazeGenerator

if __name__ == "__main__":
    cfg = loading_setup("config.txt")
    if not cfg:
        exit(0)
        print(cfg)
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
