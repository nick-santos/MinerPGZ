import pgzrun
from platformer import *

from config import *
from objects import Player, Enemy, BigGem

def load_scene(scene_name):
    global background, platforms
    scene = scenes[scene_name]
    background = scene.get("background", [])
    platforms = scene["platforms"]
    update_platforms(platforms)
    
def load_objects(scene_name):
    global player, enemies, gems
    scene = scenes[scene_name]
    player = Player(*scene["player_start"])
    enemies = [Enemy(x, y) for x, y in scene.get("enemies", [])]
    gems = [BigGem(x, y) for x, y in scene.get("gems", [])]

def change_scene(new_scene):
    global current_scene
    current_scene = new_scene
    load_scene(current_scene)
    load_objects(current_scene)

def player_reached_goal():
    # Exemplo: verifica se o player alcançou o lado direito da tela
    return player.x > WIDTH

current_scene = "level1scene1"  # Começo do level 1
load_scene(current_scene) # Carrega a cena inicial
load_objects(current_scene)



def draw():

    while check_state() == 'pause': ## novo
        return ## novo

    screen.clear()
   
    if background:
        for tile in background:
            tile.draw()

    for platform in platforms:
        platform.draw()

    if player.alive:
        player.draw() 
        
    for gem in gems:
        gem.draw()    

    for enemy in enemies:
        enemy.draw()

    

    

    # for collectable in collectables:
    #     collectable.draw()
    
    # for obstacle in obstacles:
    #     obstacle.draw()

    # game messages
    # if over:
    #     screen.draw.text("Game Over", center=(WIDTH/2, HEIGHT/2))

    # if win:
    #     screen.draw.text("You won!", center=(WIDTH/2, HEIGHT/2))


def update():

    while check_state() == 'pause': ## novo
        return ## novo
    
    player.update(gems)
    
    for enemy in enemies:
        enemy.update(player, gems)

    for gem in gems:
        gem.update(player)

    # Verificar troca de cena
    if player_reached_goal():
        change_scene("level1scene1")


pgzrun.go()