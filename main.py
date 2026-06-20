from src.parser.map_parser import MapParser


def main() -> None:
    parser = MapParser('./maps/medium/03_priority_puzzle.txt')
    data = parser.parse()
    print(data.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
