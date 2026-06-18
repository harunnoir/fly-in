from src.parser.map_parser import MapParser


def main() -> None:
    parser = MapParser('./maps/easy/01_linear_path.txt')
    data = parser.parse()
    print(data.model_dump_json())


if __name__ == "__main__":
    main()
