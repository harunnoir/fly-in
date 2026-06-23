import sys
from src import MapParser, ParsingError

def main() -> int:
    try:
        data = MapParser().parse('./maps/medium/03_priority_puzzle.txt')
    except ParsingError as e:
        print(f"[PARSING ERROR]: {e}")
        return 1

    print(data.model_dump_json(indent=2))
    return 0

if __name__ == "__main__":
    sys.exit(main())
