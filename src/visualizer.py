from __future__ import annotations
from src.simulation import TurnResult
from src.map_parser import Graph
from enum import Enum


# ANSI color codes — no libraries needed
class Color(Enum):
    """Terminal ANSI color codes."""

    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    RED = "\033[31m"
    CYAN = "\033[36m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


class Visualizer:
    """Renders simulation output to the terminal.

    Responsibilities:
        - Print the mandatory output format (D1-zone D2-zone per turn)
        - Add color to drone movements based on zone type
        - Print a summary at the end (total turns, drones delivered)
    """

    def __init__(self, graph: Graph) -> None: ...

    def render(self, turns: list[TurnResult]) -> None:
        """Print all turns to terminal, one line per turn.

        Args:
            turns: List of TurnResult from the simulator.
        """
        ...

    def _render_turn(self, turn_number: int, turn: TurnResult) -> None:
        """Print a single turn line with colors.

        Format: 'D1-zone D2-zone ...'
        """
        ...

    def _render_summary(self, total_turns: int) -> None:
        """Print final stats: total turns, drones delivered."""
        ...

    def _colorize_zone(self, zone_name: str) -> str:
        """Wrap zone name in ANSI color based on its type."""
        ...
