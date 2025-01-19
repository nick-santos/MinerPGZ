
import pgzrun # import da biblioteca pygame zero
from pgzero.actor import Actor, POS_TOPLEFT, ANCHOR_CENTER, transform_anchor
from platformer import *

TILE_SIZE = 32
ROWS = 15
COLS = 20

# set up screen dimensios
WIDTH = TILE_SIZE * COLS
HEIGHT = TILE_SIZE * ROWS
TITLE = "Miner Game"

## MAP

#background_1_000 = build("map/1_000_Background.csv", TILE_SIZE)
#platforms = build("map/1_000_Platforms.csv", TILE_SIZE)
#platforms = build("map/Platforms0.csv", TILE_SIZE)
#collectables = build("map/Collectables.csv", TILE_SIZE)
#obstacles = build("map/Obstacles.csv", TILE_SIZE)
#gems = build("map/Gems.csv", TILE_SIZE)

scenes = {
    "level1scene0": {
        "background": build("map/1_000_Background.csv", TILE_SIZE),
        "platforms": build("map/1_000_Platforms.csv", TILE_SIZE),
        "player_start": (TILE_SIZE * 10, HEIGHT - (TILE_SIZE * 5))
    },
    "level1scene1": {
        "background": build("map/1_001_Background.csv", TILE_SIZE),
        "platforms": build("map/1_001_Platforms.csv", TILE_SIZE),
        "player_start": (TILE_SIZE * 1.5, HEIGHT - (TILE_SIZE * 1)),
        "enemies": [(TILE_SIZE * 12, HEIGHT - (TILE_SIZE * 1))]
    }
}


## Game variables
over = False
win = False
gravity = 1

class Player():

    def __init__(self, x, y):
        self.image = Actor('rectangle')
        self.image.bottomleft = ((x, y))
        self.x = x
        self.y = y
        # player variables
        self.velocity_x = 4
        self.velocity_y = 0
        self.jumping = False
        self.direction = 0
        self.alive = True
        self.jump_velocity = -17

        self.numofgems = 0
        self.health = 10

    def collidelist(self, objects):
        """Delegar collidelist para o Actor interno."""
        return self.image.collidelist(objects)
    
    def colliderect(self, rect):
        """Delegar colliderect para o Actor interno."""
        return self.image.colliderect(rect)

    def draw(self):
        """Delegar o método draw para o Actor interno."""
        self.image.draw()


    def update(self):
        global over, win

        ### PLAYER ###
        # moves
        self.direction = 0

        if keyboard.a:
            self.direction = -1
        if keyboard.d:
            self.direction = 1

        self.x += self.direction * self.velocity_x
        self.image.x = self.x  # Atualizar posição do Actor

        ## X collision with platforms
        if self.collidelist(platforms) != -1 and self.direction != 0:
            object = platforms[self.collidelist(platforms)]
            if self.direction > 0:  # Movendo-se para a direita
                self.image.right = object.left
            elif self.direction < 0:  # Movendo-se para a esquerda
                self.image.left = object.right
        

        # gravity and jump
        if keyboard.w and self.jumping == False:
            self.velocity_y += self.jump_velocity
            self.jumping = True

        self.y += self.velocity_y 
        self.image.y = self.y  # Atualizar posição do Actor
        
        ## Y collision with platforms
        if self.collidelist(platforms) != -1:
            object = platforms[self.collidelist(platforms)]
            # check if going down
            if self.velocity_y > 0:
                self.jumping = False
                self.image.bottom = object.top
            # check if going up
            elif self.velocity_y < 0:
                self.image.top = object.bottom
            
            self.velocity_y = 0

        self.velocity_y += gravity

        # ## Collision with obstacles
        # if self.collidelist(obstacles) != -1:
        #     self.alive = False
        #     over = True

        # ## Collision with collectables
        # for collectable in collectables:
        #     if self.colliderect(collectable):
        #         collectables.remove(collectable)

        ## Collision with gem blocks
        for gem in gems:
            if self.colliderect(gem):
                if keyboard.e:
                    gems.remove(gem)
                    self.numofgems += 1
                    print(self.numofgems)


        self.y = self.image.y  # Atualizar posição
        self.x = self.image.x  # Atualizar posição


class Enemy():

    def __init__(self, x, y):
        self.image = Actor('rectenemy')
        self.image.bottomleft = ((x, y))
        self.x = x
        self.start_x = x  # Posição inicial no eixo X
        self.patrol_range = 90  # Alcance do movimento de patrulha
        self.speed = 2  # Velocidade de movimento
        self.direction = 1  # Direção inicial (1 = direita, -1 = esquerda)
        self.wait_time = 1  # Tempo de espera entre as direções
        self.waiting = False  # Status de espera
        self.last_wait_time = 0  # Tempo da última espera
        self.detection_radius = 150  # Raio de detecção do jogador
        self.chasing = False  # Estado atual: False para patrulha, True para perseguição
        self.patrolling = True
        self.forcedwaiting = False


        self.locked = True
        self.totalgems = 3
        self.currentgems = 0


    def draw(self):
        """Delegar o método draw para o Actor interno."""
        self.image.draw()


    def update(self, player):
        """Atualiza o comportamento do inimigo."""
        # Calcular a distância do jogador
        distance_to_player = abs(self.image.x - player.image.x)

        if self.currentgems == self.totalgems:
            # ir dormir ou ficar em idle, algo que simbolize que ele abriu o caminho
            return

        # forced waiting state after interacting with player
        if self.forcedwaiting == True: 
            if time.time() - self.last_wait_time >= self.wait_time:
                self.forcedwaiting = False  # Sai do estado de espera
                self.direction *= -1  # Inverte a direção 
            return  # Durante a espera, não se move

        # Alternar para o estado de perseguição se o jogador estiver perto
        if distance_to_player <= self.detection_radius and (player.y >= self.image.top and player.y <= self.image.bottom) and self.forcedwaiting == False:
            self.chasing = True
            self.patrolling = False
        else: # go back to his patrol area before starting to patrol again
            self.chasing = False
            if self.image.x >= self.start_x + self.patrol_range:
                self.image.x += -1 * self.speed
            elif self.image.x <= self.start_x:
                self.image.x += 1 * self.speed
            else:
                self.patrolling = True
                

        if self.chasing:
            # Perseguir o jogador
            if self.image.x < player.image.x:
                self.image.x += self.speed
            elif self.image.x > player.image.x:
                self.image.x -= self.speed
            
            # if the player is close enough the enemy will interact with them. Attack or gem collecting
            if self.image.left <= player.image.right + 10 and self.image.right >= player.image.left - 10:
                if player.numofgems > 0:
                    player.numofgems -= 1
                    self.currentgems += 1
                    print("peguei a gema kkkkk")
                    print(player.numofgems)
                else:
                    print("ATTACK")
                
                # setting the enemy to forced waiting after interation
                self.chasing = False
                self.patrolling = True
                self.forcedwaiting = True
                self.last_wait_time = time.time()  # Marca o tempo da espera

        elif self.patrolling:
            # Patrulha normal
            if self.waiting:
                # Verifica se o tempo de espera acabou
                if time.time() - self.last_wait_time >= self.wait_time:
                    self.waiting = False  # Sai do estado de espera
                    self.direction *= -1  # Inverte a direção
                return  # Durante a espera, não se move
            

            # Movimento de patrulha
            self.image.x += self.direction * self.speed

            # Verifica os limites da patrulha
            if self.image.x >= self.start_x + self.patrol_range or self.image.x <= self.start_x:
                self.waiting = True  # Entra no estado de espera
                self.last_wait_time = time.time()  # Marca o tempo da espera
        

def load_scene(scene_name):
    global background, platforms, gems, player, enemies
    scene = scenes[scene_name]
    background = scene.get("background", [])
    platforms = scene["platforms"]
    gems = scene.get("gems", [])
    player = Player(*scene["player_start"])
    enemies = [Enemy(x, y) for x, y in scene.get("enemies", [])]

def change_scene(new_scene):
    global current_scene
    current_scene = new_scene
    load_scene(current_scene)

def player_reached_goal():
    # Exemplo: verifica se o player alcançou o lado direito da tela
    return player.x > WIDTH

current_scene = "level1scene0"  # Começo do level 1
load_scene(current_scene)# Carrega a cena inicial



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