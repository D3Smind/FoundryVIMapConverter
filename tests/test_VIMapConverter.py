from VIMapConverter import *


def test_initial_json_loading2():
    vic = VIMapConverter(open("testdata/fvtt-Scene-walltest.json", "r"), Version("11.00.315"))
    vic.load_default_style_config()
    vic.set_tile([VIMapConverterTileConfig("Arrow.png$")],
                 VIMapConverterTileStyle(rotation=90))
    vic.save_map("testdata/out/walltest.jpg")
    assert vic
