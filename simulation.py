from models import Drone, Start_hub, End_hub
from graph import Graph

class Simulation:
    def __init__(self, graph: Graph, nb_drones: int, path: list[str]):
        self.graph = graph
        self.path = path
        self.zone_occupancy: dict[str, int] = {}
        self.connection_occupancy: dict[tuple[str, str], int] = {}
        self.drone_progress: dict[int, int] = {}
        self.nb_drones: int = nb_drones
        self.output: list[str] = [] 
        self.drones: list[Drone] = []

        for i in range(1, nb_drones + 1):
            self.drones.append(Drone(id=i, current_position=path[0], path=path))
            self.drone_progress[i] = 0

        for zone in self.graph.zones:
            if isinstance(self.graph.zones[zone], Start_hub):
                self.zone_occupancy[zone] = nb_drones
                continue
            self.zone_occupancy[zone] = 0


    def can_enter_zone(self, zone_name: str) -> bool:
        if isinstance(self.graph.zones[zone_name], (Start_hub, End_hub)):
            return True
        return self.zone_occupancy[zone_name] < self.graph.zones[zone_name].max_drones
    
    def can_use_connection(self, )
    def get_next_zone(self, drone: Drone) -> str | None:
        index: int = self.drone_progress[drone.id] + 1

        if index == len(self.path):
            return None

        return self.path[index]

    def move_drone(self, drone: Drone) -> bool:
        next_zone: str | None = self.get_next_zone(drone)
        if not next_zone:
            return False

        can_enter = self.can_enter_zone(next_zone)
        if not can_enter:
            return False

        index = self.drone_progress[drone.id]
        self.drone_progress[drone.id] += 1
        self.zone_occupancy[self.path[index]] -= 1
        self.zone_occupancy[next_zone] += 1
        drone.current_position = next_zone
        
        return True

    def run(self) -> None:
        counter: int = 0
        delivered: set[int] = set()
    
        while counter < self.nb_drones:
            turn_moves: list[str] = []
            for drone in self.drones:
                if self.move_drone(drone):
                    turn_moves.append(
                        f"D{drone.id}-{drone.current_position}"
                    )
                index = self.drone_progress[drone.id]
                if (index == len(self.path) - 1) and (drone.id not in delivered):
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