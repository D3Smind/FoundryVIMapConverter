import json

from version_parser import Version

from foundryMapExportParser import MapParser
from foundry_export_mocking import create_mock_foundry_export


def test_initial_json_loading():
    map = MapParser.parse_map(open("testdata/fvtt-Scene-walltest.json", "r"), Version("11.00.315"))
    assert map


def test_v11_paring():
    map = MapParser.parse_map(
        create_mock_foundry_export(changemap={
            "name": "My Map",
            "width": 5000,
            "height": 4000,
            "padding": 0.25
        }),
        Version("11.00.315"))

    assert map.name == "My Map"
    assert map.dimensions[0] == 5000
    assert map.dimensions[1] == 4000
    assert map.padding == 0.25


def test_dimension_scaling():
    map = MapParser.parse_map(
        create_mock_foundry_export(changemap={
            "width": 5000,
            "height": 4000,
            "padding": 0.25
        }),
        Version("11.00.315"))

    assert map.full_dimensions[0] == 6250
    assert map.full_dimensions[1] == 5000

    assert map.offsets[0] == 1250
    assert map.offsets[1] == 1000


def test_walls():
    walls = json.load(open("testdata/fvtt-Scene-walltest.json", "r"))["walls"]

    map = MapParser.parse_map(
        create_mock_foundry_export(changemap={
            "width": 500,
            "height": 500,
            "padding": 0.2,
            "walls": walls
        }),
        Version("11.00.315"))
    assert len(map.walls) == 22
