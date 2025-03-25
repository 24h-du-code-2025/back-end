def read_file(path) -> str:
    with open(path, 'r') as file:
        return file.read()
