from graph import Graph


class Display:
    """Handles colored terminal output for the simulation."""

    COLORS = {
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "gray": "\033[90m",
        "reset": "\033[0m",
    }

    def colorize(self, text: str, color: str | None) -> str:
        """Wrap text in ANSI color codes if the color is known.

        Args:
            text: The text to colorize.
            color: The color name, or None for no color.

        Returns:
            The colorized text, or the original text if the
            color is unknown or None.
        """
        if color not in self.COLORS or not color:
            return text
        return f"{self.COLORS[color]}{text}{self.COLORS['reset']}"

    def format_turn(self, output: list[str], graph: Graph) -> list[str]:
        """Colorize the zone names in a turn's movement list.

        Args:
            output: List of movement strings like "D1-roof1".
            graph: The zone network graph, used to look up colors.

        Returns:
            List of movement strings with colored zone names.
        """
        new_output: list[str] = []

        for elem in output:
            drone, rest = elem.split("-", 1)
            if rest in graph.zones:
                color = graph.zones[rest].color
                colored = self.colorize(rest, color)
            else:
                colored = rest
            new_output.append(f"{drone}-{colored}")

        return new_output


if __name__ == "__main__":
    from parser import parse_file
    from dijkstra import Dijkstra
    from simulation import Simulation

    nb_drones, zones, connections = parse_file("config.txt")
    graph = Graph(zones, connections)
    dijkstra = Dijkstra(graph)
    path = dijkstra.find_path("hub", "goal")

    sim = Simulation(graph, nb_drones, path)
    sim.run()

    display = Display()
    for turn in sim.output:
        turn_list = turn.split()
        colored_turn = display.format_turn(turn_list, graph)
        print(" ".join(colored_turn))
