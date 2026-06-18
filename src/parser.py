from models import Start_hub, Hub, End_hub, Zone, Connection
from typing import Any


def read_file(filename: str) -> list[str]:
    try:
        with open(filename, "r") as f:
            return f.readlines()
    except FileNotFoundError:
        print("ERROR: File Not Found.")
        return []


def extract_zone(info: str, zone_type: str) -> Zone:
    try:
        metadata: dict[str, Any] = {}
        data = info.split()
        if len(data) > 3:
            meta_parts = " ".join(data[3:]).strip("[]").split()
            for elem in meta_parts:
                parts = elem.split("=")
                if parts[0] == "color":
                    metadata["color"] = parts[1]
                elif parts[0] == "max_drones":
                    metadata["max_drones"] = int(parts[1])
                elif parts[0] == "zone":
                    metadata["zone_type"] = parts[1]

        zone: Zone
        if zone_type == "Start_hub":
            zone = Start_hub(
                name=data[0], x=int(data[1]), y=int(data[2]), **metadata
            )
        elif zone_type == "Hub":
            zone = Hub(
                name=data[0], x=int(data[1]), y=int(data[2]), **metadata
            )
        else:
            zone = End_hub(
                name=data[0], x=int(data[1]), y=int(data[2]), **metadata
            )

        return zone

    except ValueError:
        raise SystemExit("ERROR: Expected Integer Value")


def extract_connection(data: str) -> Connection:
    parts = data.strip().split()
    zones = parts[0].split("-")
    metadata = {}

    if len(parts) > 1:
        meta_parts = " ".join(parts[1:]).strip("[]").split()
        for elem in meta_parts:
            key, value = elem.split("=")
            if key == "max_link_capacity":
                metadata["max_link_capacity"] = int(value)

    return Connection(zone1=zones[0], zone2=zones[1], **metadata)


def clean_lines(lines: list[str]) -> list[str]:
    data: list[str] = []
    for line in lines:
        line = line.strip()
        if line.startswith("#") or not line:
            continue
        data.append(line)
    return data


def duplicates_checker(zones: dict[str, Zone]) -> None:
    start_hubs = [z for z in zones.values() if isinstance(z, Start_hub)]
    end_hubs = [z for z in zones.values() if isinstance(z, End_hub)]

    if len(start_hubs) != 1:
        raise SystemExit(
            f"ERROR: there must be exactly one 'start_hub',"
            f" found {len(start_hubs)}"
        )

    if len(end_hubs) != 1:
        raise SystemExit(
            f"ERROR: there must be exactly one 'end_hub',"
            f" found {len(end_hubs)}"
        )


def validate_connections(
    zones: dict[str, Zone], connections: list[Connection]
) -> None:
    for conn in connections:
        if conn.zone1 not in zones:
            raise SystemExit(
                f"ERROR: zone '{conn.zone1}' in connection does not exist"
            )
        if conn.zone2 not in zones:
            raise SystemExit(
                f"ERROR: zone '{conn.zone2}' in connection does not exist"
            )

    seen: set[tuple[str, ...]] = set()
    for conn in connections:
        pair = tuple(sorted([conn.zone1, conn.zone2]))
        if pair in seen:
            raise SystemExit(
                f"ERROR: duplicate connection '{conn.zone1}-{conn.zone2}'"
            )
        seen.add(pair)


def parse_file(
    filename: str,
) -> tuple[int, dict[str, Zone], list[Connection]]:
    data = clean_lines(read_file(filename))
    temp = data[0].split(":")
    zones: dict[str, Zone] = {}
    connections: list[Connection] = []
    nb_drones = 0

    if temp[0] != "nb_drones":
        raise SystemExit(
            f"ERROR line 1: expected 'nb_drones: <number>',"
            f" got '{temp[0]}'"
        )
    try:
        nb_drones = int(temp[1])
        if nb_drones <= 0:
            raise ValueError
    except ValueError:
        raise SystemExit(
            f"ERROR line 1: 'nb_drones' value must be a positive integer,"
            f" got '{temp[1].strip()}'"
        )

    for elem in data[1:]:
        parts = elem.split(":")
        if parts[0] == "start_hub":
            zone = extract_zone(parts[1], "Start_hub")
            if zone.name in zones:
                raise SystemExit(f"ERROR: zone '{zone.name}' already exists")
            zones[zone.name] = zone

        elif parts[0] == "hub":
            zone = extract_zone(parts[1], "Hub")
            if zone.name in zones:
                raise SystemExit(f"ERROR: zone '{zone.name}' already exists")
            zones[zone.name] = zone

        elif parts[0] == "end_hub":
            zone = extract_zone(parts[1], "End_hub")
            if zone.name in zones:
                raise SystemExit(f"ERROR: zone '{zone.name}' already exists")
            zones[zone.name] = zone

        elif parts[0] == "connection":
            connections.append(extract_connection(parts[1]))

        else:
            raise SystemExit(f"ERROR: unknown line type '{parts[0]}'")

    duplicates_checker(zones)
    validate_connections(zones, connections)

    return nb_drones, zones, connections


if __name__ == "__main__":
    print(parse_file("config.txt"))
