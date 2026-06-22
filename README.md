*This project has been created as part of the 42 curriculum by mkacemi.*

# Fly-in

## Description

Fly-in is a drone routing simulation system written in Python. The project
models a network of zones connected by links, and computes the most
efficient way to route a fleet of drones from a starting zone (`start_hub`)
to a destination zone (`end_hub`), while respecting movement constraints,
zone occupancy limits, and connection capacity limits.

The simulation proceeds in discrete turns. At each turn, every drone can
move to an adjacent zone (if capacity allows), stay in place, or be in
transit toward a `restricted` zone (which takes two turns to reach). The
goal is to deliver all drones to the end zone in the fewest possible turns
while respecting every constraint defined in the zone network.

## Instructions

### Requirements

- Python 3.10 or later
- A virtual environment is recommended (`venv`)

### Installation

```bash
python3 -m venv venv
source venv/bin/activate
make install
```

### Running the simulation

```bash
make run
```

This executes `python3 main.py config.txt`, using the provided `config.txt`
map file. To run a different map, edit the `Makefile`'s `run` rule or call
the script directly:

```bash
python3 main.py <path_to_map_file>
```

### Debugging

```bash
make debug
```

### Linting

```bash
make lint
make lint-strict
```

### Cleaning

```bash
make clean
```

## Project structure

- `parser.py` — Parses the map configuration file into zones, connections,
  and the number of drones, with full validation and error handling.
- `models.py` — Pydantic data models: `Zone` (with subclasses `Start_hub`,
  `Hub`, `End_hub`), `Connection`, and `Drone`.
- `graph.py` — `Graph` class building an adjacency representation of the
  zone network from parsed zones and connections.
- `dijkstra.py` — `Dijkstra` class implementing a custom shortest-path
  algorithm (no external graph library used, per project constraints).
- `simulation.py` — `Simulation` class running the turn-by-turn movement
  of all drones, enforcing zone occupancy, connection capacity, and
  restricted-zone multi-turn movement rules.
- `display.py` — `Display` class providing ANSI-colored terminal output
  of the simulation, based on each zone's configured color.
- `main.py` — Entry point wiring the parser, graph, pathfinding,
  simulation, and display together.

## Algorithm choices and implementation strategy

### Pathfinding

Dijkstra's algorithm was implemented from scratch using Python's built-in
`heapq` module as a priority queue, since external graph libraries
(e.g. `networkx`) are forbidden by the project constraints. The algorithm
computes the lowest-cost path between the start and end zones, where the
cost of entering a zone depends on its type:

- `normal`: 1 turn
- `priority`: 1 turn
- `restricted`: 2 turns
- `blocked`: zones are excluded entirely from the graph traversal

The algorithm maintains a `distances` dictionary (best known cost to reach
each zone) and a `previous` dictionary (used to reconstruct the final path
once the destination is reached), giving Dijkstra's standard
`O((V + E) log V)` complexity using a binary heap.

### Simulation

All drones currently follow the same single path returned by Dijkstra.
Each turn, the simulation engine attempts to advance every drone that is
not currently "in flight":

- **Normal/priority zones**: the drone moves into the next zone
  immediately if the destination zone and the connection both have
  available capacity.
- **Restricted zones**: the drone "departs" on the current turn (freeing
  its previous zone and reserving its destination slot immediately, to
  prevent another drone from claiming the same slot mid-transit), and is
  tracked in an `in_flight` registry until it lands on the following turn.
  This matches the project's two-turn, no-early-arrival, no-extra-wait
  rule for restricted zones.

Zone and connection occupancy are tracked with dictionaries updated
incrementally as drones move, which keeps each turn's complexity
proportional to the number of active drones rather than the size of the
whole network.

### Output format

Each simulation turn produces one line of space-separated `D<id>-<zone>`
(or `D<id>-<zone1>-<zone2>` while a drone is in transit toward a
restricted zone) entries, matching the format specified in the subject.

## Visual representation

The `Display` class wraps each zone name in ANSI escape codes matching the
zone's configured `color` attribute from the map file (e.g. `color=red`
renders that zone's name in red in the terminal). This provides immediate
visual feedback on which zones drones are moving through during the
simulation, directly in the terminal, without requiring any external
graphics library.

## Example

**Input (`config.txt`):**
```
nb_drones: 3
start_hub: hub 0 0 [color=green]
end_hub: goal 10 10 [color=yellow]
hub: roof1 3 4 [zone=restricted color=red]
connection: hub-roof1
connection: roof1-goal
```

**Output:**
```
D1-hub-roof1
D1-roof1
D1-goal D2-hub-roof1
D2-roof1
D2-goal D3-hub-roof1
D3-roof1
D3-goal
```

Each line represents one simulation turn. Each entry follows the format:
- `D<ID>-<zone>` — the drone arrived at this zone this turn
- `D<ID>-<zone1>-<zone2>` — the drone is in transit toward a restricted zone (2-turn movement)
- Drones that did not move are omitted from the line
- Drones that reached the end zone are considered delivered and no longer appear

## Resources

- [Dijkstra's algorithm — Wikipedia](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)
- [Python `heapq` documentation](https://docs.python.org/3/library/heapq.html)
- [Pydantic documentation](https://docs.pydantic.dev/)
- [ANSI escape code reference](https://en.wikipedia.org/wiki/ANSI_escape_code)
- [PEP 257 — Docstring Conventions](https://peps.python.org/pep-0257/)

### AI usage

Claude (Anthropic) was used throughout this project as a learning and
debugging aid, primarily through guided, step-by-step explanations rather
than direct code generation:

- Explaining core concepts (Dijkstra's algorithm, priority queues, Pydantic
  validation, OOP design) before any code was written, often with manual
  traced examples.
- Reviewing code written by the author and pointing out bugs (e.g.
  incorrect distance calculations, missing capacity checks, type errors
  surfaced by mypy) without rewriting the logic outright.
- Assisting in drafting this README based on the project's actual,
  already-implemented architecture.

All core logic (the parser, the graph, Dijkstra's algorithm, the
simulation engine, and the display) was written and understood by the
author, with AI used as a tutor and code reviewer rather than as a
replacement for the author's own implementation work.