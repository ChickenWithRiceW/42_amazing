import yaml


def parse_yaml_config() -> None:
    with open("config.yaml") as f:
        cfg = yaml.load(f, Loader=yaml.FullLoader)
        print(cfg)


if __name__ == "__main__":
    parse_yaml_config()