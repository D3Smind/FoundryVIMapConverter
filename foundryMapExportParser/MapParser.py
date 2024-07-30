import json
from typing import TextIO

from version_parser import Version

from foundryMapExportParser.Map import Map
from foundryMapExportParser.Tile import Tile
from foundryMapExportParser.Wall import *


def parse_map(path_to_exported_json: TextIO, version: Version) -> Map:
    _foundry_export_dict = json.load(path_to_exported_json)
    map = Map()

    if version.get_major_version() == 11:
        _parse_map_v11(_foundry_export_dict, map)
    else:
        raise AttributeError("Version not supported")

    map.calculate_real_dimensions()

    return map


def _parse_map_v11(foundry_export_dict: dict, map: Map):
    map.name = foundry_export_dict["name"]
    map.dimensions = (
        foundry_export_dict["width"],
        foundry_export_dict["height"]
    )
    map.grid_size = foundry_export_dict["grid"]["size"]
    map.padding = foundry_export_dict["padding"]

    map.walls = []
    for foundry_wall_export_dict in foundry_export_dict["walls"]:
        map.walls.append(_parse_wall_v11(foundry_wall_export_dict))

    map.tiles = []
    for foundry_tile_export_dict in foundry_export_dict["tiles"]:
        map.tiles.append(_parse_tile_v11(foundry_tile_export_dict))


def _parse_wall_v11(foundry_wall_export_dict: dict) -> Wall:
    wall = Wall()

    wall.position_from = (
        foundry_wall_export_dict["c"][0],
        foundry_wall_export_dict["c"][1]
    )
    wall.position_to = (
        foundry_wall_export_dict["c"][2],
        foundry_wall_export_dict["c"][3]
    )

    match foundry_wall_export_dict["move"]:
        case 20:
            wall.movement_restrictions = MovementRestriction.Normal
        case 0:
            wall.movement_restrictions = MovementRestriction.No
        case _:
            raise AttributeError("Unsupported")

    match foundry_wall_export_dict["light"]:
        case 40:
            wall.light_restriction = LightRestriction.ReverseProximity
        case 30:
            wall.light_restriction = LightRestriction.Proximity
        case 20:
            wall.light_restriction = LightRestriction.Normal
        case 10:
            wall.light_restriction = LightRestriction.Limited
        case 0:
            wall.light_restriction = LightRestriction.No
        case _:
            raise AttributeError("Unsupported")

    match foundry_wall_export_dict["sight"]:
        case 40:
            wall.sight_restriction = SightRestriction.ReverseProximity
        case 30:
            wall.sight_restriction = SightRestriction.Proximity
        case 20:
            wall.sight_restriction = SightRestriction.Normal
        case 10:
            wall.sight_restriction = SightRestriction.Limited
        case 0:
            wall.sight_restriction = SightRestriction.No
        case _:
            raise AttributeError("Unsupported")

    match foundry_wall_export_dict["sound"]:
        case 40:
            wall.sound_restriciton = SoundRestiction.ReverseProximity
        case 30:
            wall.sound_restriciton = SoundRestiction.Proximity
        case 20:
            wall.sound_restriciton = SoundRestiction.Normal
        case 10:
            wall.sound_restriciton = SoundRestiction.Limited
        case 0:
            wall.sound_restriciton = SoundRestiction.No
        case _:
            raise AttributeError("Unsupported")

    match foundry_wall_export_dict["dir"]:
        case 0:
            wall.direction = Direction.Both
        case 1:
            wall.direction = Direction.Left
        case 2:
            wall.direction = Direction.Right
        case _:
            raise AttributeError("Unsupported")

    if foundry_wall_export_dict["door"] == 0:
        wall.door = Door.No

    elif foundry_wall_export_dict["door"] == 1:
        match foundry_wall_export_dict["ds"]:
            case 0:
                wall.door = Door.Closed
            case 1:
                wall.door = Door.Opened
            case 2:
                wall.door = Door.Locked
            case _:
                raise AttributeError("Unsupported")

    elif foundry_wall_export_dict["door"] == 2:
        match foundry_wall_export_dict["ds"]:
            case 0:
                wall.door = Door.SecretDoorClosed
            case 1:
                wall.door = Door.SecretDoorOpened
            case 2:
                wall.door = Door.SecretDoorLocked
            case _:
                raise AttributeError("Unsupported")

    return wall


def _parse_tile_v11(foundry_tile_export_dict: dict) -> Tile:
    tile = Tile()

    tile.position = (foundry_tile_export_dict["x"], foundry_tile_export_dict["y"])
    tile.dimensions = (foundry_tile_export_dict["width"], foundry_tile_export_dict["height"])
    tile.rotation = foundry_tile_export_dict["rotation"]
    tile.hidden = foundry_tile_export_dict["hidden"]
    tile.texture_path = foundry_tile_export_dict["texture"]["src"]

    return tile
