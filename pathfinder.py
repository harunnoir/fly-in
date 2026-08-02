import math
from heapq import heappop, heappush

from map_parser import Graph, Link, ZoneType


class PathFinder:
    """Provides shortest-path finding utilities."""

    @staticmethod
    def find(graph: Graph, start: str, end: str) -> tuple[float, list[str]]:
        """Return (cost, path) for the current best route, or (inf, []) if none exists.

        Args:
            graph: The parsed drone network graph.
            start: Zone name to start from.
            end: Zone name to reach.
        """
        return PathFinder._dijkstra(graph, start, end)

    @staticmethod
    def _dijkstra(
        graph: Graph,
        src: str,
        dst: str,
    ) -> tuple[float, list[str]]:
        """Standard Dijkstra, using live congestion-scaled edge weights.

        Args:
            graph: The parsed drone network graph.
            src: Zone name to start from.
            dst: Zone name to reach.
        """
        best_cost: dict[str, float] = {src: 0.0}
        via: dict[str, str | None] = {src: None}

        to_visit: list[tuple[float, int, str]] = [(0.0, 1, src)]
        visited: set[str] = set()

        while to_visit:
            cost_so_far, _, current_zone_name = heappop(to_visit)

            if current_zone_name in visited:
                continue

            visited.add(current_zone_name)

            if current_zone_name == dst:
                return (
                    cost_so_far,
                    PathFinder._reconstruct_path(via, current_zone_name),
                )

            current_zone = graph.zones[current_zone_name]

            for link in current_zone.links:
                neighbor_name = link.target.name

                if not link.target.is_accessible():
                    continue

                neighbor_cost = cost_so_far + PathFinder._get_dynamic_weight(link)

                if neighbor_cost < best_cost.get(neighbor_name, math.inf):
                    best_cost[neighbor_name] = neighbor_cost
                    via[neighbor_name] = current_zone_name

                    heappush(
                        to_visit,
                        (
                            neighbor_cost,
                            0 if link.target.zone_type == ZoneType.PRIORITY else 1,
                            neighbor_name,
                        ),
                    )

        return (math.inf, [])

    @staticmethod
    def _get_dynamic_weight(link: Link) -> float:
        """Zone weight, scaled up as the link fills toward capacity.

        Args:
            link: The link being traversed.
        """
        base_weight = link.target.get_path_weight()
        drones_on_link = len(link.connection.drones_in_transit)
        congestion_ratio = drones_on_link / link.connection.max_link_capacity

        return base_weight * (1 + congestion_ratio)

    @staticmethod
    def _reconstruct_path(
        via: dict[str, str | None],
        destination: str,
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
