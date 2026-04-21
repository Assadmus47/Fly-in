from pydantic import BaseModel, Field
from typing import Optional, List


class Hub(BaseModel):
    name: str
    x: int = Field(..., ge=0)
    y: int = Field(..., ge=0)
    color: Optional[str] = None
    capacity: Optional[int] = Field(None, ge=1)


class Connection(BaseModel):
    from_hub: str
    to_hub: str
    restricted: bool = False


class Config(BaseModel):
    nb_drones: int = Field(..., gt=0)
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
    result = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        result.append(line)
    return result


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


def assert_parts(line: str, parts: list[str], expected: int):
    if len(parts) < expected:
        raise ValueError(f"Invalid line format -> {line}")


def error(line: str, msg: str):
    raise ValueError(f"[Parsing error] {msg} -> {line}")


def main() -> None:
    lines = read_file("config.txt")
    lines = clean_lines(lines)

    nb_drones = 0
    start = None
    end = None
    hubs = []
    connections = []
    hub_names = set()

    for line in lines:
        parts = line.split()
        key = parts[0].rstrip(":")

        if key == "nb_drones":
            assert_parts(line, parts, 2)
            try:
                nb_drones = int(parts[1])
            except:
                error(line, "Invalid nb_drones value")

        elif key == "start_hub":
            assert_parts(line, parts, 4)
            try:
                start = Hub(
                    name=parts[1],
                    x=int(parts[2]),
                    y=int(parts[3])
                )
                hub_names.add(parts[1])
            except Exception as e:
                error(line, f"Invalid start_hub values: {e}")

        elif key == "end_hub":
            assert_parts(line, parts, 4)
            try:
                end = Hub(
                    name=parts[1],
                    x=int(parts[2]),
                    y=int(parts[3])
                )
                hub_names.add(parts[1])
            except Exception as e:
                error(line, f"Invalid end_hub values: {e}")

        elif key == "hub":
            assert_parts(line, parts, 4)

            if parts[1] in hub_names:
                error(line, "Duplicate hub name")

            hub_names.add(parts[1])

            options = parse_options(line)

            try:
                hubs.append(
                    Hub(
                        name=parts[1],
                        x=int(parts[2]),
                        y=int(parts[3]),
                        color=options.get("color"),
                        capacity=int(options["max_drones"]) if "max_drones" in options else None
                    )
                )
            except Exception as e:
                error(line, f"Invalid hub values: {e}")

        elif key == "connection":
            assert_parts(line, parts, 2)

            try:
                zone1, zone2 = parts[1].split("-")
            except ValueError:
                error(line, "Invalid connection format")

            if zone1 not in hub_names or zone2 not in hub_names:
                error(line, "Connection uses unknown hub")

            connections.append(
                Connection(
                    from_hub=zone1,
                    to_hub=zone2,
                    restricted="restricted" in line
                )
            )

        else:
            error(line, "Unknown directive")

    if start is None:
        error("FINAL", "Missing start hub")

    if end is None:
        error("FINAL", "Missing end hub")

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
