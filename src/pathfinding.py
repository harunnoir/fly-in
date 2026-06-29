from __future__ import annotations
import heapq

from src.map_parser import Graph, Zone, ZoneType


class ShortestPathFinder:
    def find(self, graph: Graph) -> list[Zone]:
        """Returns ordered list of zones: [start, ..., end]"""
        ...
