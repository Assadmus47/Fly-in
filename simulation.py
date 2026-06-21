from models import Drone, Start_hub, End_hub, Connection
from graph import Graph


class Simulation:
    """Simulates drone movement through the zone network turn by turn.

    Attributes:
        graph: The zone network graph.
        path: The shortest path computed by Dijkstra.
        zone_occupancy: Number of drones currently in each zone.
        connection_occupancy: Number of drones currently using
            each connection during the current turn.
        drone_progress: Index of each drone's progress in the path.
        nb_drones: Total number of drones to deliver.
        output: List of formatted strings, one per simulation turn.
        drones: List of all drones in the simulation.
    """

    def __init__(
        self, graph: Graph, nb_drones: int, path: list[str]
    ) -> None:
        """Initialize the simulation state.

        Args:
            graph: The zone network graph.
            nb_drones: Number of drones to simulate.
            path: Ordered list of zone names from start to end.
        """
        self.graph = graph
        self.path = path
        self.zone_occupancy: dict[str, int] = {}
        self.connection_occupancy: dict[tuple[str, ...], int] = {}
        self.drone_progress: dict[int, int] = {}
        self.nb_drones: int = nb_drones
        self.output: list[str] = []
        self.drones: list[Drone] = []

        for i in range(1, nb_drones + 1):
            self.drones.append(
                Drone(id=i, current_position=path[0], path=path)
            )
            self.drone_progress[i] = 0

        for zone in self.graph.zones:
            if isinstance(self.graph.zones[zone], Start_hub):
                self.zone_occupancy[zone] = nb_drones
                continue
            self.zone_occupancy[zone] = 0

    def can_enter_zone(self, zone_name: str) -> bool:
        """Check whether a drone can enter the given zone.

        Args:
            zone_name: The name of the zone to check.

        Returns:
            True if the zone has available capacity.
        """
        zone = self.graph.zones[zone_name]
        if isinstance(zone, (Start_hub, End_hub)):
            return True
        return self.zone_occupancy[zone_name] < zone.max_drones

    def get_connection(self, zone1: str, zone2: str) -> Connection:
        """Find the connection linking two zones.

        Args:
            zone1: Name of the first zone.
            zone2: Name of the second zone.

        Returns:
            The Connection object linking the two zones.
        """
        for connection in self.graph.connections:
            if (
                (connection.zone1 == zone1 and connection.zone2 == zone2)
                or (connection.zone2 == zone1 and connection.zone1 == zone2)
            ):
                return connection

        raise SystemExit(
            f"ERROR: no connection found between '{zone1}' and '{zone2}'"
        )

    def can_use_connection(self, zone1: str, zone2: str) -> bool:
        """Check whether the connection between two zones has capacity.

        Args:
            zone1: Name of the first zone.
            zone2: Name of the second zone.

        Returns:
            True if the connection has available capacity.
        """
        connection = self.get_connection(zone1, zone2)
        key = tuple(sorted([zone1, zone2]))

        return self.connection_occupancy[key] < connection.max_link_capacity

    def get_next_zone(self, drone: Drone) -> str | None:
        """Return the next zone in a drone's path.

        Args:
            drone: The drone to check.

        Returns:
            The next zone name, or None if the drone has arrived.
        """
        index: int = self.drone_progress[drone.id] + 1

        if index == len(self.path):
            return None

        return self.path[index]

    def move_drone(self, drone: Drone) -> bool:
        """Attempt to move a drone to its next zone.

        Args:
            drone: The drone to move.

        Returns:
            True if the drone moved, False otherwise.
        """
        next_zone: str | None = self.get_next_zone(drone)
        if not next_zone:
            return False

        can_enter = self.can_enter_zone(next_zone)
        can_use = self.can_use_connection(drone.current_position, next_zone)
        if not can_enter or not can_use:
            return False

        key = tuple(sorted([drone.current_position, next_zone]))
        self.connection_occupancy[key] += 1

        index = self.drone_progress[drone.id]
        self.drone_progress[drone.id] += 1
        self.zone_occupancy[self.path[index]] -= 1
        self.zone_occupancy[next_zone] += 1
        drone.current_position = next_zone

        return True

    def run(self) -> None:
        """Run the simulation until all drones reach the end zone."""
        counter: int = 0
        delivered: set[int] = set()

        while counter < self.nb_drones:
            turn_moves: list[str] = []
            self.connection_occupancy = {
                key: 0 for key in self.connection_occupancy
            }

            for drone in self.drones:
                if self.move_drone(drone):
                    turn_moves.append(
                        f"D{drone.id}-{drone.current_position}"
                    )
                index = self.drone_progress[drone.id]
                is_last = index == len(self.path) - 1
                if is_last and drone.id not in delivered:
                    counter += 1
                    delivered.add(drone.id)

            self.output.append(" ".join(turn_moves))


if __name__ == "__main__":
    from parser import parse_file
    from dijkstra import Dijkstra

    nb_drones, zones, connections = parse_file("config.txt")
    graph = Graph(zones, connections)
    dijkstra = Dijkstra(graph)
    path = dijkstra.find_path("hub", "goal")

    sim = Simulation(graph, nb_drones, path)
    sim.run()
    for line in sim.output:
        print(line)
