

def read_file(filename: str) -> str:
    try:
        with open(filename, "r") as f:
            data: str = f.read()
        return data
    except FileNotFoundError:
        print("ERROR: File Not Found.")


if __name__ == "__main__":
    data = read_file("config.txt")
    print(data)
    print("apres")
    souwa = data.splitlines()
    print(souwa)