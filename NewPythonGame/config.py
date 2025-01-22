from platformer import *

TILE_SIZE = 32
ROWS = 15
COLS = 20

# set up screen dimensios
WIDTH = TILE_SIZE * COLS
HEIGHT = TILE_SIZE * ROWS
TITLE = "Miner Game"

scenes = {
    "level1scene0": {
        "background": build("map/1_000_Background.csv", TILE_SIZE),
        "platforms": build("map/1_000_Platforms.csv", TILE_SIZE),
        "player_start": (TILE_SIZE * 10, HEIGHT - (TILE_SIZE * 5))
    },
    "level1scene1": {
        "background": build("map/1_001_Background.csv", TILE_SIZE),
        "platforms": build("map/1_001_Platforms.csv", TILE_SIZE),
        "gems": build("map/1_001_Gems.csv", TILE_SIZE),
        "player_start": (TILE_SIZE * 1.5, HEIGHT - (TILE_SIZE * 1)),
        "enemies": [(TILE_SIZE * 12, HEIGHT - (TILE_SIZE * 1))]
    }
}



## Game variables
over = False
win = False
gravity = 1
platforms = []
gems = []

# config_data = {}

def update_platforms(new_platforms, new_gems):
    global platforms, gems
    platforms = new_platforms
    gems = new_gems

def get_platforms():
    global platforms
    return platforms

def get_gems():
    global gems
    return gems

# def update_config(cofig="", data=[]):
#     config_data.