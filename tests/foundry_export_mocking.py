import io
import json
from typing import TextIO


def create_mock_foundry_export(changemap: dict, walls=None, tiles=None, drawings=None, tokens=None, notes=None,
                               lights=None, sounds=None, templates=None) -> TextIO:
    if templates is None:
        templates = []
    if sounds is None:
        sounds = []
    if lights is None:
        lights = []
    if notes is None:
        notes = []
    if tokens is None:
        tokens = []
    if drawings is None:
        drawings = []
    if tiles is None:
        tiles = []
    if walls is None:
        walls = []

    foundry_export_dict = {
        "name": "Testname",
        "width": 100,
        "height": 100,
        "padding": 0.5,
        "walls": walls,
        "tiles": tiles,
        "drawings": drawings,
        "tokens": tokens,
        "lights": lights,
        "notes": notes,
        "sounds": sounds,
        "templates": templates,
        "grid": {
            "size": 10,
            "type": 1,
            "color": "#ffffff",
            "alpha": 0,
            "distance": 5,
            "units": "ft"
        }
    }

    for changekey in changemap:
        foundry_export_dict[changekey] = changemap[changekey]

    return io.StringIO(json.dumps(foundry_export_dict))
