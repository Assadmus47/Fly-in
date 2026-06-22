import sys
from models import Start_hub, End_hub, Zone
from parser import parse_file
from dijkstra import Dijkstra
from simulation import Simulation
from graph import Graph
from display import Display


def find_start_end(zones: dict[str, Zone]) -> tuple[str, str]:
    """Find the names of the start and end zones.

    Args:
        zones: Dictionary of zones keyed by name.

    Returns:
        Tuple of (start_zone_name, end_zone_name).
    """
    start = ""
    end = ""
    for zone in zones.values():
        if isinstance(zone, Start_hub):
            start = zone.name
        if isinstance(zone, End_hub):
            end = zone.name
    return (start, end)


def main() -> None:
    """Entry point — parse, simulate, and display the drone routing."""
    if len(sys.argv) < 2:
        raise SystemExit("ERROR: usage: python3 main.py <config_file>")

    nb_drones, zones, connections = parse_file(sys.argv[1])
    start_zone, end_zone = find_start_end(zones)
    graph = Graph(zones, connections)
    dijkstra = Dijkstra(graph)
    path = dijkstra.find_path(start_zone, end_zone)

    sim = Simulation(graph, nb_drones, path)
    sim.run()

    display = Display()
    display.print_path(path, graph)

    for i, turn in enumerate(sim.output):
        moves = turn.split()
        display.print_turn(i + 1, moves, graph, end_zone)

    display.print_summary(len(sim.output), nb_drones)


if __name__ == "__main__":
    main()
