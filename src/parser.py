
from pydantic import BaseModel,Field
from typing import Optional, List, Literal


class Start_hub(BaseModel):
    name: str = Field(...)
    x: int = Field(...)
    y: int = Field(...)
    color: Optional[str] = None
    max_drones: int = Field(default=1, gt=0)
    zone_type: Literal["normal", "blocked", "restricted", "priority"] = "normal"


def read_file(filename: str) -> list[str]:
    try:
        with open(filename, "r") as f:
            return f.readlines()
    except FileNotFoundError:
        print("ERROR: File Not Found.")
        return []


def extract_start_hub(data: list[str]) -> Start_hub:
    try:
        metadata = {}
        data = data.split()

        if len(data) == 4:
            meta_parts = data[3].strip("[]").split()
            for elem in meta_parts:
                elem = elem.split("=")
                if elem[0] == "color":
                    metadata["color"] = elem[1]
                elif elem[0] == "max_drones":
                    metadata["max_drones"] = int(elem[1])
                elif elem[0] == "zone":
                    metadata["zone_type"] = elem[1]
        zone = Start_hub(
                name=data[0],
                x=int(data[1]),
                y=int(data[2]),
                **metadata
            )
        print(zone)

    except ValueError:
        raise SystemExit("ERROR : Expected Integer Value")


def clean_lines(lines: list[str]) -> list[str]:
    data: list[str] = []
    for line in lines:
        line = line.strip()
        if line.startswith("#") or not line:
            continue 
        data.append(line)
    return data

def parse_file(filename: str) -> None:
    data = clean_lines(read_file(filename))
    temp = data[0].split(":")
    if temp[0] != "nb_drones":
        raise SystemExit(
            f"ERROR line 1: expected 'nb_drones: <number>', got '{temp[0]}'"
            )
    try:
        nb_drones = int(temp[1])
        if nb_drones <= 0:
            raise ValueError
    except ValueError as e:
        raise SystemExit(
            f"ERROR line 1: 'nb_drones' value must be a positive integer,"
            f" got '{temp[1].strip()}'"
        )
    
    for elem in data[1:]:
        elem = elem.split(":")
        if elem[0] == "start_hub":
            extract_start_hub(elem[1])
        elif elem[0] == "hub":
            pass
        elif elem[0] == "end_hub":
            pass
        elif elem[0] == "connection":
            pass


if __name__ == "__main__":
    parse_file("souwa")
