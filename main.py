from foundyVIExport.VIMapConverter import *

if __name__ == '__main__':
    vic = VIMapConverter(open("foundry-scene.json", "r"), Version("11.00.315"))
    vic.load_default_style_config()
    vic.set_tile([VIMapConverterTileConfig("Arrow.png$")],
                 VIMapConverterTileStyle(rotation=90))
    vic.save_map("walltest.jpg")
    assert vic
