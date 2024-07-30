import os
import re
from typing import TextIO

import matplotlib.pyplot as plt
from version_parser import Version

from foundryMapExportParser.MapParser import parse_map
from foundryMapExportParser.Wall import *


class VIMapConverterWallStyle:
    def __init__(self, linewidth: float = 0.4, color: str = "black", linestyle: tuple[int, tuple] = (0, ())):
        self.linewidth = linewidth
        self.color = color
        self.linestyle = linestyle


class VIMapConverterTileSymbol(Enum):
    ARROW = 0


class VIMapConverterTileStyle:
    def __init__(self, symbol: VIMapConverterTileSymbol = VIMapConverterTileSymbol.ARROW, rotation: int = 0):
        self.symbol = symbol
        self.rotation: int = rotation

    def draw_symbol(self, coordinates: tuple[int, int], size: int, rotation: float):
        if self.symbol == VIMapConverterTileSymbol.ARROW:
            direction = round((rotation + self.rotation) % 360 / 90)
            if direction == 0:
                arrow_from: tuple[float, float] = (coordinates[0] + size / 2, - coordinates[1] - size + (size / 10))
                plt.arrow(arrow_from[0], arrow_from[1], 0, size - 3 * (size / 10), length_includes_head=True,
                          head_width=size / 3,
                          color="black")
            if direction == 2:
                arrow_from: tuple[float, float] = (coordinates[0] + size / 2, - coordinates[1] - (size / 10))
                plt.arrow(arrow_from[0], arrow_from[1], 0, - size + 3 * (size / 10), length_includes_head=True,
                          head_width=size / 3,
                          color="black")


class VIMapConverterWallConfig:
    def __init__(self, direction: Direction, doorconfig: Door, lightconfig: LightRestriction,
                 movementconfig: MovementRestriction, sightconfig: SightRestriction, soundconfig: SoundRestiction):
        self.direction = direction
        self.doorconfig = doorconfig
        self.lightconfig = lightconfig
        self.movementconfig = movementconfig
        self.sightconfig = sightconfig
        self.soundconfig = soundconfig

    def __eq__(self, other):
        return self.direction == other.direction and \
            self.doorconfig == other.doorconfig and \
            self.lightconfig == other.lightconfig and \
            self.movementconfig == other.movementconfig and \
            self.sightconfig == other.sightconfig and \
            self.soundconfig == other.soundconfig

    def __hash__(self):
        return hash((self.direction, self.doorconfig, self.lightconfig, self.movementconfig, self.sightconfig,
                     self.soundconfig))


class VIMapConverterTileConfig:
    def __init__(self, texture_regex: str):
        self.texture_regex = texture_regex

    def check_texture_regex(self, texture_path: str) -> bool:
        return re.search(self.texture_regex, texture_path) is not None

    def __eq__(self, other):
        return self.texture_regex == other.texture_regex

    def __hash__(self):
        return hash(self.texture_regex)


class VIMapConverter:
    def __init__(self, path_to_exported_json: TextIO, version: Version):
        self.map = parse_map(path_to_exported_json, version)
        self.wallconfigs = {}
        self.tileconfigs: dict[VIMapConverterTileConfig: VIMapConverterTileStyle] = {}

    def load_empty_style_config(self):
        for directionconfig in Direction:
            for doorconfig in Door:
                for lightconfig in LightRestriction:
                    for movementconfig in MovementRestriction:
                        for sightconfig in SightRestriction:
                            for soundconfig in SoundRestiction:
                                self.wallconfigs[VIMapConverterWallConfig(
                                    directionconfig,
                                    doorconfig,
                                    lightconfig,
                                    movementconfig,
                                    sightconfig,
                                    soundconfig
                                )] = None

    def load_default_style_config(self):
        self.load_empty_style_config()

        for directionconfig in Direction:
            for lightconfig in LightRestriction:
                for movementconfig in [MovementRestriction.Normal]:
                    for soundconfig in SoundRestiction:
                        for sightconfig in SightRestriction:
                            for doorconfig in [Door.No, Door.SecretDoorClosed, Door.SecretDoorOpened,
                                               Door.SecretDoorLocked]:
                                self.wallconfigs[VIMapConverterWallConfig(
                                    directionconfig,
                                    doorconfig,
                                    lightconfig,
                                    movementconfig,
                                    sightconfig,
                                    soundconfig
                                )] = VIMapConverterWallStyle()

        for directionconfig in Direction:
            for lightconfig in LightRestriction:
                for movementconfig in [MovementRestriction.Normal]:
                    for soundconfig in SoundRestiction:
                        for sightconfig in SightRestriction:
                            for doorconfig in [Door.Opened, Door.Closed]:
                                self.wallconfigs[VIMapConverterWallConfig(
                                    directionconfig,
                                    doorconfig,
                                    lightconfig,
                                    movementconfig,
                                    sightconfig,
                                    soundconfig
                                )] = VIMapConverterWallStyle(linewidth=0.3, linestyle=(0, (1, 1)))

    def set_wall_style(self, configurations: list[VIMapConverterWallConfig], style: VIMapConverterWallStyle):
        for configuration in configurations:
            self.wallconfigs[configuration] = style

    def set_tile(self, configurations: list[VIMapConverterTileConfig], style: VIMapConverterTileStyle):
        for configuration in configurations:
            self.tileconfigs[configuration] = style

    def save_map(self, path: os.path):
        plt.figure(figsize=(self.map.dimensions[0] / 1000, self.map.dimensions[1] / 1000), dpi=1000)
        plt.axis('off')

        for wall in self.map.walls:
            wallstyle: VIMapConverterWallStyle = self.wallconfigs[VIMapConverterWallConfig(
                wall.direction,
                wall.door,
                wall.light_restriction,
                wall.movement_restrictions,
                wall.sight_restriction,
                wall.sound_restriciton
            )]

            if wallstyle is not None:
                plt.plot((self.map.real_coord_x(wall.position_from[0]),
                          self.map.real_coord_x(wall.position_to[0])),
                         (-self.map.real_coord_y(wall.position_from[1]),
                          -self.map.real_coord_y(wall.position_to[1])),
                         linewidth=wallstyle.linewidth,
                         color=wallstyle.color,
                         linestyle=wallstyle.linestyle)

        for tile in self.map.tiles:
            for tileconfig in self.tileconfigs:
                if tileconfig.check_texture_regex(tile.texture_path):
                    self.tileconfigs[tileconfig].draw_symbol(
                        (
                            self.map.real_coord_x(tile.position[0]),
                            self.map.real_coord_y(tile.position[1])
                        ),
                        size=tile.dimensions[0],
                        rotation=tile.rotation
                    )

        plt.savefig(path, pad_inches=0, dpi=1000)
