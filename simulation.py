from collections.abc import Callable

from map_parser import Graph


class Drone:
    id: int
    path: list[str]
    where: int

    def __init__(self, id: int, path: list[str], where: int = 0) -> None:
        self.id = id
        self.path = path
        self.where = where

    def is_reached(self) -> bool:
        return self.where == len(self.path) - 1

    def move(self) -> None:
        if not self.is_reached():
            self.where += 1


class Engine:
    _graph: Graph

    def __init__(self, graph: Graph) -> None:
        self._graph = graph

    def update(self) -> None:
        pass

    def render(self) -> None:
        pass

    def run(self, drones: set[Drone]) -> None:
        for drone in drones:
            drone.move()


class Simulator:
    _drones: set[Drone]
    _graph: Graph

    def __init__(
        self,
        graph: Graph,
        pathfinder: Callable[[Graph, str, str], tuple[float, list[str]]],
    ) -> None:
        _, path = pathfinder(graph, graph.start_hub.name, graph.end_hub.name)
        self._drones = set()
        for i in range(1, graph.nb_drones + 1):
            self._drones.add(Drone(i, path))

    def run(self) -> None:
        turns = 0
        engine = Engine(self._graph)
        while not all(drone.is_reached() for drone in self._drones):
            engine.run(self._drones)
            turns += 1
