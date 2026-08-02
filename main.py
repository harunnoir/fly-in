#!/usr/bin/env python
import argparse
import sys

# from rich.traceback import install
#
# install(show_locals=True)
from map_parser import MapParser, ParsingError
from pathfinder import PathFinder
from simulation import Simulator


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

    Simulator(graph, PathFinder.find).run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
