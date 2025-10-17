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
        "player_start": (TILE_SIZE * 10, HEIGHT - (TILE_SIZE * 5)),
        "next_scene": "level1scene1"
    },
    "level1scene1": {
        "background": build("map/1_001_1_Background.csv", TILE_SIZE),
        "platforms": build("map/1_001_1_Platforms.csv", TILE_SIZE),
        "player_start": (TILE_SIZE * 1, HEIGHT - (TILE_SIZE * 2)),
        "next_scene": "level1scene2"
    },
    "level1scene2": {
        "background": build("map/1_002_Background.csv", TILE_SIZE),
        "platforms": build("map/1_002_Platforms.csv", TILE_SIZE),
        "player_start": (TILE_SIZE * 1, HEIGHT - (TILE_SIZE * 11)),
        "next_scene": "level1scene2"
    }
    # "level1scene1": {
    #     "background": build("map/1_001_Background.csv", TILE_SIZE),
    #     "platforms": build("map/1_001_Platforms.csv", TILE_SIZE),
    #     "gems": [(TILE_SIZE * 10, HEIGHT - (TILE_SIZE * 10)), (TILE_SIZE * 2, HEIGHT - (TILE_SIZE * 7)), (TILE_SIZE * 7, HEIGHT - (TILE_SIZE * 4)), (TILE_SIZE * 7, HEIGHT - (TILE_SIZE * 1)), (TILE_SIZE * 6, HEIGHT - (TILE_SIZE * 1)), (TILE_SIZE * 5, HEIGHT - (TILE_SIZE * 1))],
    #     "player_start": (TILE_SIZE * 1.5, HEIGHT - (TILE_SIZE * 1)),
    #     "enemies": [(TILE_SIZE * 12, HEIGHT - (TILE_SIZE * 1))]
    # }
}

## Game variables
state = ''
over = False
win = False
gravity = 1
platforms = []

# config_data = {}

def update_platforms(new_platforms):
    global platforms
    platforms = new_platforms

def get_platforms():
    global platforms
    return platforms

def check_state():
    global state
    return state

def set_state(new_state):
    global state
    state = new_state

# def update_config(cofig="", data=[]):
#     config_data.