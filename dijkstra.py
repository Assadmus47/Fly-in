import heapq

from graph import Graph


class Dijkstra:
    """Computes shortest paths between zones using Dijkstra's algorithm."""

    def __init__(self, graph: Graph) -> None:
        """Initialize the Dijkstra solver with a graph.

        Args:
            graph: The graph to search paths on.
        """
        self.graph = graph

    def find_path(self, start: str, end: str) -> list[str]:
        """Find the lowest-cost path between two zones.

        Args:
            start: Name of the starting zone.
            end: Name of the destination zone.

        Returns:
            Ordered list of zone names from start to end.
        """
        previous: dict[str, str] = {}
        distances: dict[str, int | float] = {}
        heap: list[tuple[int | float, str]] = [(0, start)]

        for zone in self.graph.zones:
            if zone == start:
                distances[zone] = 0
            else:
                distances[zone] = float("inf")

        while heap:
            distance, zone = heapq.heappop(heap)

            for neighbor in self.graph.get_neighbors(zone):
                neighbor_type = self.graph.zones[neighbor].zone_type
                if neighbor_type == "blocked":
                    continue
                elif neighbor_type == "restricted":
                    new_distance = distance + 2
                else:
                    new_distance = distance + 1

                if new_distance > distances[neighbor]:
                    continue
                previous[neighbor] = zone
                distances[neighbor] = new_distance
                heapq.heappush(heap, (distances[neighbor], neighbor))

        current: str = end
        path: list[str] = []
        while current != start:
            path.append(current)
            current = previous[current]
        path.append(current)
        path.reverse()

        return path
