import Wall
from Tile import Tile


class Map:
    def __init__(self):
        self.name: str = None
        self.dimensions: tuple[int, int] = None
        self.full_dimensions: tuple[int, int] = None
        self.offsets: tuple[int, int] = None
        self.padding: float = None
        self.walls: list[Wall] = []
        self.tiles: list[Tile] = []
        self.grid_size: int = None

    def calculate_real_dimensions(self):
        self.full_dimensions = (
            self.dimensions[0] * (1 + self.padding),
            self.dimensions[1] * (1 + self.padding)
        )
        self.offsets = (
            self.dimensions[0] * self.padding,
            self.dimensions[1] * self.padding
        )

    def real_coord_x(self, coord_x: int) -> int:
        return coord_x - self.offsets[0]

    def real_coord_y(self, coord_y: int) -> int:
        return coord_y - self.offsets[1]
