import heapq

from src.map_parser import Graph, Zone


class ShortestPathFinder:
    """Finds the shortest path in a drone network graph using Dijkstra's algorithm.

    Weights are determined by zone type:
        - normal:     1.0
        - priority:   0.9  (preferred over normal)
        - restricted: 2.0  (costs 2 turns to enter)
        - blocked:    skipped (inaccessible)
    """

    # -------------------------
    # PUBLIC API
    # -------------------------

    def find(self, graph: Graph) -> list[Zone]:
        """Find the shortest path from start_hub to end_hub.

        Args:
            graph: The parsed drone network graph.

        Returns:
            Ordered list of zones from start to goal.
            Empty list if no path exists.
        """
        start_name, goal_name = self._get_start_and_goal_names(graph)
        cost_table, came_from = self._init_tables(graph, start_name)
        self._dijkstra(graph, start_name, goal_name, cost_table, came_from)
        return self._reconstruct_path(graph, goal_name, came_from)

    # -------------------------
    # INITIALIZATION
    # -------------------------

    def _get_start_and_goal_names(self, graph: Graph) -> tuple[str, str]:
        """Extract zone names of the start and goal hubs.

        Args:
            graph: The drone network graph.

        Returns:
            Tuple of (start_name, goal_name).
        """
        return (graph.start_hub.name, graph.end_hub.name)

    def _init_tables(
        self,
        graph: Graph,
        start_name: str,
    ) -> tuple[dict[str, float], dict[str, str | None]]:
        """Initialize cost and path-tracking tables for Dijkstra.

        All zones start with infinite cost except start (cost=0).
        All zones start with no known predecessor.

        Args:
            graph: The drone network graph.
            start_name: Name of the starting zone.

        Returns:
            cost_table: Maps zone name -> best known cost to reach it.
            came_from:  Maps zone name -> name of zone we came from.
        """
        cost_table: dict[str, float] = {
            zone_name: float("inf") for zone_name in graph.zones
        }
        came_from: dict[str, str | None] = {
            zone_name: None for zone_name in graph.zones
        }
        cost_table[start_name] = 0.0
        return cost_table, came_from

    # -------------------------
    # CORE DIJKSTRA
    # -------------------------

    def _dijkstra(
        self,
        graph: Graph,
        start_name: str,
        goal_name: str,
        cost_table: dict[str, float],
        came_from: dict[str, str | None],
    ) -> None:
        """Run Dijkstra's algorithm, updating cost_table and came_from in place.

        Uses a min-heap (priority queue) to always explore the cheapest
        unvisited zone first. Stops as soon as the goal is popped -
        guaranteed to be the shortest path at that point.

        Args:
            graph:      The drone network graph.
            start_name: Name of the starting zone.
            goal_name:  Name of the destination zone.
            cost_table: Best known cost to reach each zone (modified in place).
            came_from:  Predecessor of each zone on best path (modified in place).
        """
        # Heap entries are (cost, zone_name) — heapq pops smallest cost first
        heap: list[tuple[float, str]] = [(0.0, start_name)]

        while heap:
            current_cost, current_zone_name = heapq.heappop(heap)

            # Skip stale heap entries — a cheaper path was already found
            if current_cost > cost_table[current_zone_name]:
                continue

            # Goal reached — shortest path is guaranteed, stop early
            if current_zone_name == goal_name:
                return

            current_zone = graph.zones[current_zone_name]

            for link in current_zone.links:
                neighbor_name = link.target.name
                edge_weight = float(link.target.get_path_weight())
                cost_through_current = current_cost + edge_weight

                # Found a cheaper path to this neighbor — update and push
                if cost_through_current < cost_table[neighbor_name]:
                    cost_table[neighbor_name] = cost_through_current
                    came_from[neighbor_name] = current_zone_name
                    heapq.heappush(heap, (cost_through_current, neighbor_name))

    # -------------------------
    # PATH RECONSTRUCTION
    # -------------------------

    def _reconstruct_path(
        self,
        graph: Graph,
        goal_name: str,
        came_from: dict[str, str | None],
    ) -> list[Zone]:
        """Reconstruct the shortest path by walking came_from backwards from goal.

        Args:
            graph:     The drone network graph.
            goal_name: Name of the destination zone.
            came_from: Predecessor map built by Dijkstra.

        Returns:
            Ordered list of Zone objects from start to goal.
            Empty list if goal was never reached.
        """
        # Goal unreachable — came_from[goal] was never updated from None
        if came_from.get(goal_name) is None and goal_name != graph.start_hub.name:
            return []

        path: list[str] = []
        current_zone_name: str | None = goal_name

        # Walk backwards: goal -> ... -> start (stops when came_from is None)
        while current_zone_name is not None:
            path.append(current_zone_name)
            current_zone_name = came_from[current_zone_name]

        path.reverse()
        return [graph.zones[zone_name] for zone_name in path]
