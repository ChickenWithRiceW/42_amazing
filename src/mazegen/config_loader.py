def load_config(file_name: str) -> dict[str, str]:
    """Parses the given config file and returns a dict of k, v pairs"""
    cfg: dict[str, str] = {}
    with open(file_name) as f:
        for line in f:
            # Remove any trailing white spaces
            line = line.strip()

            # If empty or is a comment skip
            if not line or line.startswith('#'):
                continue

            key, _, val = line.partition("=")

            # Checks if the partition method actually found the seperator
            if key != line:
                # Strips any spaces again and removes comments
                val = val.strip().split(" ", 1)[0]
                cfg[key.strip()] = val
    return cfg


if __name__ == "__main__":
    cfg = load_config("config.txt")

    for k, v in cfg.items():
        print(f"{k} = {v}")