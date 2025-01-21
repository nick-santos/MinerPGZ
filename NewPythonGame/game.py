
import pgzrun # import da biblioteca pygame zero
from pgzero.actor import Actor, POS_TOPLEFT, ANCHOR_CENTER, transform_anchor
from platformer import *

from config import *
from objects import Player, Enemy

def load_scene(scene_name):
    global background, platforms, gems
    scene = scenes[scene_name]
    background = scene.get("background", [])
    platforms = scene["platforms"]
    gems = scene.get("gems", [])

    update_platforms(scene["platforms"]) # test
    
def load_objects(scene_name):
    global player, enemies
    scene = scenes[scene_name]
    player = Player(*scene["player_start"])
    enemies = [Enemy(x, y) for x, y in scene.get("enemies", [])]

def change_scene(new_scene):
    global current_scene
    current_scene = new_scene
    load_scene(current_scene)
    load_objects(current_scene)

def player_reached_goal():
    # Exemplo: verifica se o player alcançou o lado direito da tela
    return player.x > WIDTH

current_scene = "level1scene0"  # Começo do level 1
load_scene(current_scene)# Carrega a cena inicial4
load_objects(current_scene)


def draw():
    screen.clear()
    
    if background:
        for tile in background:
            tile.draw()

    for platform in platforms:
        platform.draw()

    if gems:
        for gem in gems:
            gem.draw()    

    for enemy in enemies:
        enemy.draw()

    # for collectable in collectables:
    #     collectable.draw()
    
    # for obstacle in obstacles:
    #     obstacle.draw()

    if player.alive:
        player.draw()
    
    # game messages
    if over:
        screen.draw.text("Game Over", center=(WIDTH/2, HEIGHT/2))

    if win:
        screen.draw.text("You won!", center=(WIDTH/2, HEIGHT/2))


def update():
    player.update()
    
    for enemy in enemies:
        enemy.update(player)

    # Verificar troca de cena
    if player_reached_goal():
        change_scene("level1scene1")


pgzrun.go()