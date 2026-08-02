import argparse
import sys

from map_parser import MapParser, ParsingError
from pathfinder import PathFinder


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

    path = PathFinder(graph).find()
    if not path:
        print("No path possible on this map!")
        return 1
    print(f"[cost={path[0]}] {' -> '.join(path[1])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
