
import pgzrun # import da biblioteca pygame zero
#from pgzero.builtins import Actor,Rect,ZRect,clock,images,keyboard,mouse
from pgzero.actor import Actor, POS_TOPLEFT, ANCHOR_CENTER, transform_anchor
#from pgzhelper import *

TILE_SIZE = 8
ROWS = 30
COLS = 20

# set up screen dimensios
#WIDTH = TILE_SIZE * ROWS
#HEIGHT = TILE_SIZE * COLS
#TITLE = "Miner Game"
WIDTH = 800
HEIGHT = 600

# Background
bg = Actor('background2')

# man
man = Actor('viking1')
man.x = 400
man.y = 450
man.images = ['viking1', 'viking2']

floor = 450

velocity = 0
gravity = 1

# other
other = Actor('viking2')
other.x = 600
other.y = 320


def draw():
    bg.draw()
    man.draw()
    other.draw()


def update():
    global velocity

    ### player ###
    # moves
    if keyboard.left: # type: ignore
        man.x -= 5
    if keyboard.right: # type: ignore
        man.x += 5

    ## JUMP ##
    if keyboard.up and man.y == floor: # type: ignore
        velocity = -18
    man.y += velocity
    velocity += gravity

    if man.y > floor:
        velocity = 0
        man.y = floor

    ## COLLISION ##
    if man.colliderect(other):
        man.x = 100
      


pgzrun.go()