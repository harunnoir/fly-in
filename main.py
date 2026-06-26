import sys
from src import MapParser, ParsingError


def main() -> int:
    try:
        graph = MapParser().parse("./maps/hard/03_ultimate_challenge.txt")
    except ParsingError as e:
        print(f"[PARSING ERROR]: {e}")
        return 1

    print(graph.model_dump_json(indent=2))
    return 0
    # 2. Find the path
    # path = find_shortest_path(graph, graph.start_hub, graph.end_hub)
    #
    # # 3. Print the result
    # if path:
    #     print(f"Path found ({len(path)} steps):")
    #     print(" -> ".join([z.name for z in path]))
    # else:
    #     print("No path possible on this map!")
    # return 0


if __name__ == "__main__":
    sys.exit(main())
