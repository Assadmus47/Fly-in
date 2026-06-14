

def read_file(filename: str) -> list[str]:
    try:
        with open(filename, "r") as f:
            return f.readlines()
    except FileNotFoundError:
        print("ERROR: File Not Found.")
        return []


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

if __name__ == "__main__":
    parse_file("souwa")
