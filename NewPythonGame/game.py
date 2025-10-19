import pgzrun
from platformer import *

from config import *
from objects import Player, Enemy, LittleEnemy, BigGem

is_going_back = False

def load_scene(scene_name):
    global background, platforms, east_scene, west_scene
    scene = scenes[scene_name]
    background = scene.get("background", [])
    platforms = scene["platforms"]
    update_platforms(platforms)
    east_scene = scene.get("east_scene")
    west_scene = scene.get("west_scene")
    
def load_objects(scene_name):
    global player, enemies, little_enemies, gems, is_going_back
    scene = scenes[scene_name]
    if is_going_back:
        player = Player(*scene["player_start_back"])
    else:
        player = Player(*scene["player_start"])
    enemies = [Enemy(x, y, range) for x, y, range in scene.get("enemies", [])]
    little_enemies = [LittleEnemy(x, y, range) for x, y, range in scene.get("little_enemies", [])]
    gems = [BigGem(x, y) for x, y in scene.get("gems", [])]

def change_scene(new_scene):
    global current_scene
    current_scene = new_scene
    load_scene(current_scene)
    load_objects(current_scene)

def player_reached_east():
    # Exemplo: verifica se o player alcançou o lado direito da tela
    global is_going_back
    if player.x > WIDTH:
        is_going_back = False
        return True

def player_reached_west():
    # Exemplo: verifica se o player alcançou o lado direito da tela
    global is_going_back
    if player.x < 0:
        is_going_back = True
        return True

current_scene = "level1scene0"  # Começo do level 1
load_scene(current_scene) # Carrega a cena inicial
load_objects(current_scene)



def draw():

    while check_state() == 'pause': ## novo
        return ## novo

    #screen.clear()
   
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

    for little_enemy in little_enemies:
        little_enemy.draw()

    

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

    for little_enemy in little_enemies:
        little_enemy.update(player, gems)

    for gem in gems:
        gem.update(player)

    # Verificar troca de cena
    if player_reached_east():
        change_scene(east_scene)

    if player_reached_west():
        change_scene(west_scene)


pgzrun.go()