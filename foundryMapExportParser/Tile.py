class Tile:
    def __init__(self):
        self.position: tuple[int, int] = None
        self.dimensions: tuple[int, int] = None
        self.rotation: int = None
        self.hidden: bool = None
        self.texture_path: str = None
