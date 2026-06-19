from models import Connection, Zone


class Graph:
    """Represents the drone navigation graph.

    Attributes:
        zones: Dictionary of all zones keyed by name.
        connections: List of all connections between zones.
        adjacency: Adjacency dict mapping each zone to its neighbors.
    """

    def __init__(
        self,
        zones: dict[str, Zone],
        connections: list[Connection]
    ) -> None:
        """Build the adjacency dict from zones and connections.

        Args:
            zones: Dictionary of zones keyed by name.
            connections: List of connections between zones.
        """
        self.adjacency: dict[str, list[str]] = {}
        self.zones: dict[str, Zone] = zones
        self.connections: list[Connection] = connections

        for zone in zones:
            self.adjacency[zone] = []

        for conn in self.connections:
            self.adjacency[conn.zone1].append(conn.zone2)
            self.adjacency[conn.zone2].append(conn.zone1)

    def get_neighbors(self, name: str) -> list[str]:
        """Return the list of neighbors for a given zone.

        Args:
            name: The name of the zone.

        Returns:
            List of neighboring zone names.
        """
        return self.adjacency[name]

    def get_zone(self, name: str) -> Zone:
        """Return the Zone object for a given zone name.

        Args:
            name: The name of the zone.

        Returns:
            The Zone object corresponding to the name.
        """
        return self.zones[name]

    def is_accessible(self, name: str) -> bool:
        """Return True if the zone is not blocked.

        Args:
            name: The name of the zone.

        Returns:
            True if the zone is accessible, False if blocked.
        """
        return self.zones[name].zone_type != "blocked"
