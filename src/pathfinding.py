from __future__ import annotations

import math
from heapq import heappop, heappush

from src.map_parser import Graph


class PathFinder:
    """K-shortest paths using Dijkstra + Yen's algorithm.

    Finds up to K loopless paths from start_hub to end_hub,
    useful for distributing drones across alternative routes.
    """

    _graph: Graph
    _k: int
    _start: str
    _goal: str

    def __init__(self, graph: Graph, k: int = 5) -> None:
        """Initialize the pathfinder.

        Args:
            graph: The parsed drone network graph.
            k: Number of shortest paths to find.
        """
        self._graph = graph
        self._k = k
        self._start = graph.start_hub.name
        self._goal = graph.end_hub.name

    def find(self) -> list[tuple[float, list[str]]]:
        """Find K shortest paths from start to end.

        Returns:
            List of (cost, path) tuples sorted by cost.
            path is a list of zone names from start to end.
            Returns empty list if no path exists.
        """
        return self._yen()

    def _dijkstra(
        self,
        src: str,
        dst: str,
        excluded_nodes: set[str] | None = None,
        excluded_edges: set[frozenset[str]] | None = None,
    ) -> tuple[float, list[str]]:
        """Run Dijkstra from src to dst.

        Args:
            src: Source zone name.
            dst: Destination zone name.
            excluded_nodes: Zone names to skip during traversal.
            excluded_edges: Edges (as frozensets) to skip during traversal.

        Returns:
            Tuple of (cost, path_names) where path_names goes from src to dst.
            Returns (inf, []) if no path exists.
        """
        if excluded_nodes is None:
            excluded_nodes = set()
        if excluded_edges is None:
            excluded_edges = set()

        dist: dict[str, float] = {src: 0.0}
        came_from: dict[str, str | None] = {src: None}
        heap: list[tuple[float, str]] = [(0.0, src)]
        visited: set[str] = set()

        while heap:
            cost, current = heappop(heap)

            if current in visited:
                continue
            visited.add(current)

            if current == dst:
                return (cost, self._reconstruct_path(came_from, current))

            zone = self._graph.zones[current]

            for link in zone.links:
                neighbor_name = link.target.name

                if neighbor_name in excluded_nodes:
                    continue

                edge = frozenset({current, neighbor_name})
                if edge in excluded_edges:
                    continue

                if not link.target.is_accessible():
                    continue

                new_cost = cost + link.target.get_path_weight()

                if new_cost < dist.get(neighbor_name, math.inf):
                    dist[neighbor_name] = new_cost
                    came_from[neighbor_name] = current
                    heappush(heap, (new_cost, neighbor_name))

        return (math.inf, [])

    def _reconstruct_path(
        self,
        came_from: dict[str, str | None],
        current: str,
    ) -> list[str]:
        """Reconstruct path from came_from map.

        Args:
            came_from: Mapping of zone name to its predecessor.
            current: The destination zone name to trace back from.

        Returns:
            List of zone names from start to current (inclusive).
        """
        path: list[str] = []
        node: str | None = current
        while node is not None:
            path.append(node)
            node = came_from.get(node)
        path.reverse()
        return path

    def _yen(self) -> list[tuple[float, list[str]]]:
        """Yen's K-shortest loopless paths algorithm.

        Returns:
            List of (cost, path) tuples sorted by cost.
        """
        first_cost, first_path = self._dijkstra(self._start, self._goal)
        if not first_path:
            return []

        paths: list[tuple[float, list[str]]] = [(first_cost, first_path)]

        for _k in range(1, self._k):
            if _k - 1 >= len(paths):
                break
            prev_path = paths[_k - 1][1]

            for i in range(len(prev_path) - 1):
                spur_node = prev_path[i]
                root_path = prev_path[: i + 1]

                excluded_nodes: set[str] = set(root_path) - {spur_node}

                excluded_edges: set[frozenset[str]] = set()
                for _, existing_path in paths:
                    if existing_path[: i + 1] == root_path and i + 1 < len(
                        existing_path
                    ):
                        edge = frozenset({existing_path[i], existing_path[i + 1]})
                        excluded_edges.add(edge)

                spur_cost, spur_path = self._dijkstra(
                    spur_node, self._goal, excluded_nodes, excluded_edges
                )

                if not spur_path:
                    continue

                total_path = root_path[:-1] + spur_path
                total_cost = self._path_cost(total_path)

                if not any(p == total_path for _, p in paths):
                    paths.append((total_cost, total_path))
                    paths.sort(key=lambda x: x[0])

            if len(paths) >= self._k:
                break

        return paths[: self._k]

    def _path_cost(self, path: list[str]) -> float:
        """Calculate total cost of a path.

        Args:
            path: List of zone names.

        Returns:
            Total movement cost (start zone weight excluded).
        """
        if len(path) <= 1:
            return 0.0
        cost = 0.0
        for name in path[1:]:
            cost += self._graph.zones[name].get_path_weight()
        return cost
