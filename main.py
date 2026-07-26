import sys
from src import MapParser, ParsingError, PathFinder
import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fly-in drone routing simulator")
    _ = parser.add_argument("map_file", help="Path to the map file")
    _ = parser.add_argument(
        "--visual", action="store_true", help="Enable colored terminal output"
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        graph = MapParser().parse(args.map_file)
    except ParsingError as e:
        print(f"[PARSING ERROR]: {e}")
        return 1

    paths = PathFinder(graph).find()
    if not paths:
        print("No path possible on this map!")
        return 1
    for cost, path in paths:
        print(f"[cost={cost}] {' -> '.join(path)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
