from graph import Graph


class Display:
    """Handles colored terminal output for the simulation."""

    COLORS = {
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "gray": "\033[90m",
        "cyan": "\033[36m",
        "reset": "\033[0m",
    }

    SEPARATOR = "=" * 45

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

    def colorize_zone(self, zone_name: str, graph: Graph) -> str:
        """Return a zone name wrapped in its configured color.

        Args:
            zone_name: The name of the zone to colorize.
            graph: The zone network graph, used to look up colors.

        Returns:
            The colorized zone name, or plain text if no color.
        """
        if zone_name not in graph.zones:
            return zone_name
        color = graph.zones[zone_name].color
        return self.colorize(zone_name, color)

    def print_path(self, path: list[str], graph: Graph) -> None:
        """Print the computed path from start to end.

        Args:
            path: Ordered list of zone names from start to end.
            graph: The zone network graph, used to look up colors.
        """
        colored = [self.colorize_zone(z, graph) for z in path]
        print(f"\nPath: {' --> '.join(colored)}\n")

    def print_turn(
        self,
        turn_number: int,
        moves: list[str],
        graph: Graph,
        end_zone: str,
    ) -> None:
        """Print a single simulation turn with formatted movements.

        Args:
            turn_number: The current turn number.
            moves: List of movement strings like "D1-roof1".
            graph: The zone network graph, used to look up colors.
            end_zone: Name of the end zone to detect deliveries.
        """
        print(self.SEPARATOR)
        print(f"Turn {turn_number}")
        print(self.SEPARATOR)

        for move in moves:
            drone, rest = move.split("-", 1)

            if "-" in rest:
                origin, destination = rest.split("-", 1)
                c_origin = self.colorize_zone(origin, graph)
                c_dest = self.colorize_zone(destination, graph)
                print(
                    f"  {drone}: {c_origin} ~~~~~~~~~~>"
                    f" [{c_dest}]   (in transit)"
                )
            elif rest == end_zone:
                colored = self.colorize_zone(rest, graph)
                print(f"  {drone}: -----------> {colored}   [DELIVERED]")
            else:
                colored = self.colorize_zone(rest, graph)
                print(f"  {drone}: -----------> {colored}")

    def print_summary(self, nb_turns: int, nb_drones: int) -> None:
        """Print the simulation summary.

        Args:
            nb_turns: Total number of turns taken.
            nb_drones: Total number of drones delivered.
        """
        print(f"\n{self.SEPARATOR}")
        print(f"Simulation complete in {nb_turns} turns")
        print(f"{nb_drones}/{nb_drones} drones delivered")
        print(f"{self.SEPARATOR}\n")
