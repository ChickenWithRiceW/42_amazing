from src.config import loading_setup

if __name__ == "__main__":
    cfg = loading_setup("config.txt")
    if not cfg:
        exit(0)
        print(cfg)
