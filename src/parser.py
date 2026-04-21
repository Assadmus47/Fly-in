
from pydantic import BaseModel
from typing import Optional, List


class Hub(BaseModel):
    name: str
    x: int
    y: int
    color: Optional[str] = None
    capacity: Optional[int] = None


class Connection(BaseModel):
    from_hub: str
    to_hub: str
    restricted: bool = False


class Config(BaseModel):
    nb_drones: int
    start: Hub
    end: Hub
    hubs: List[Hub]
    connections: List[Connection]


def read_file(filename: str) -> list[str]:
    try:
        with open(filename, "r") as f:
            return f.readlines()
    except FileNotFoundError:
        print("ERROR: File Not Found.")
        return []


def clean_lines(lines: list[str]) -> List[str]:
    clean_lines = []
    for line in lines:
        line = line.strip()

        if line == "":
            continue

        if line.startswith("#"):
            continue        

        clean_lines.append(line)

    return clean_lines


def parse_options(line: str) -> dict:
    if "[" not in line:
        return {}

    inside = line.split("[")[1].split("]")[0]
    options = {}

    for item in inside.split():
        if "=" in item:
            k, v = item.split("=", 1)
            options[k] = v

    return options


def main() -> None:
    lines = read_file("config.txt")
    lines = clean_lines(lines)


    nb_drones = 0
    start = None
    end = None
    hubs = []
    connections = []

    for line in lines:
        parts = line.split()
        key = parts[0].rstrip(":")

        if key == "nb_drones":
            nb_drones = int(parts[1])
        
        elif key == "start_hub":
            start = Hub(
                name=parts[1],
                x=int(parts[2]),
                y=int(parts[3])
            )

        elif key == "end_hub":
            end = Hub(
                name=parts[1],
                x=int(parts[2]),
                y=int(parts[3])
            )

        elif key == "hub":
            options = parse_options(line)

            hubs.append(
                Hub(
                    name=parts[1],
                    x=int(parts[2]),
                    y=int(parts[3]),
                    color=options.get("color"),
                    capacity=int(options["max_drones"]) if "max_drones" in options else None
                )
            )

        elif key == "connection":
            zone1, zone2 = parts[1].split("-")
            options = parse_options(line)

            connections.append(
                Connection(
                    from_hub=zone1,
                    to_hub=zone2,
                    restricted="restricted" in options
                )
            )

    if start is None or end is None:
        raise ValueError("Missing start or end hub")

    config = Config(
        nb_drones=nb_drones,
        start=start,
        end=end,
        hubs=hubs,
        connections=connections
    )
    print(config)


if __name__ == "__main__":
    main()