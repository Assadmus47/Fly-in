from models import Start_hub, End_hub, Zone
from parser import parse_file
from dijkstra import Dijkstra
from simulation import Simulation
from graph import Graph
from display import Display
import sys


def find_start_end(zones: dict[str, Zone]) -> tuple[str, str]:
    start = ""
    end = ""

    for zone in zones.values():
        if isinstance(zone, Start_hub):
            start = zone.name
        if isinstance(zone, End_hub):
            end = zone.name
    return (start, end)


def main() -> None:
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
    for turn in sim.output:
        turn_list = turn.split()
        colored_turn = display.format_turn(turn_list, graph)
        print(" ".join(colored_turn))


if __name__ == "__main__":
    main()
