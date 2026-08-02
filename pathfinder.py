import math
from heapq import heappop, heappush

from map_parser import Graph, Link


class PathFinder:
    """Finds the current shortest path, accounting for live congestion."""

    _graph: Graph
    _start: str
    _goal: str

    def __init__(self, graph: Graph) -> None:
        """
        Args:
            graph: The parsed drone network graph.
        """
        self._graph = graph
        self._start = graph.start_hub.name
        self._goal = graph.end_hub.name

    def find(self) -> tuple[float, list[str]]:
        """Return (cost, path) for the current best route, or (inf, []) if none exists."""
        return self._dijkstra(self._start, self._goal)

    def _dijkstra(self, src: str, dst: str) -> tuple[float, list[str]]:
        """Standard Dijkstra, using live congestion-scaled edge weights.

        Args:
            src: Zone name to start from.
            dst: Zone name to reach.
        """
        best_cost: dict[str, float] = {src: 0.0}
        via: dict[str, str | None] = {src: None}
        to_visit: list[tuple[float, str]] = [(0.0, src)]
        visited: set[str] = set()

        while to_visit:
            cost_so_far, current_zone_name = heappop(to_visit)

            if current_zone_name in visited:
                continue
            visited.add(current_zone_name)

            if current_zone_name == dst:
                return (cost_so_far, self._reconstruct_path(via, current_zone_name))

            current_zone = self._graph.zones[current_zone_name]

            for link in current_zone.links:
                neighbor_name = link.target.name

                if not link.target.is_accessible():
                    continue

                neighbor_cost = cost_so_far + self._get_dynamic_weight(link)

                if neighbor_cost < best_cost.get(neighbor_name, math.inf):
                    best_cost[neighbor_name] = neighbor_cost
                    via[neighbor_name] = current_zone_name
                    heappush(to_visit, (neighbor_cost, neighbor_name))

        return (math.inf, [])

    def _get_dynamic_weight(self, link: Link) -> float:
        """Zone weight, scaled up as the link fills toward capacity.

        Args:
            link: The link being traversed.
        """
        base_weight = link.target.get_path_weight()
        drones_on_link = len(link.connection.drones_in_transit)
        congestion_ratio = drones_on_link / link.connection.max_link_capacity
        return base_weight * (1 + congestion_ratio)

    def _reconstruct_path(
        self, via: dict[str, str | None], destination: str
    ) -> list[str]:
        """Walk the via map backward from destination to build the path.

        Args:
            via: Maps each zone name to the zone it was reached from.
            destination: Zone name to trace back from.
        """
        path: list[str] = []
        zone_name: str | None = destination
        while zone_name is not None:
            path.append(zone_name)
            zone_name = via.get(zone_name)
        path.reverse()
        return path
