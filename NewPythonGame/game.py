
import pgzrun # import da biblioteca pygame zero
from pgzero.actor import Actor, POS_TOPLEFT, ANCHOR_CENTER, transform_anchor
from platformer import *

TILE_SIZE = 32
ROWS = 15
COLS = 20

## MAP
platforms = build("map/Platforms.csv", TILE_SIZE)
collectables = build("map/Collectables.csv", TILE_SIZE)
obstacles = build("map/Obstacles.csv", TILE_SIZE)

# set up screen dimensios
WIDTH = TILE_SIZE * COLS
HEIGHT = TILE_SIZE * ROWS
TITLE = "Miner Game"

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
        self.jump_velocity = -15

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

        if keyboard.left:
            self.direction = -1
        if keyboard.right:
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
        if keyboard.up and self.jumping == False:
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

        ## Collision with obstacles
        if self.collidelist(obstacles) != -1:
            self.alive = False
            over = True

        ## Collision with collectables
        for collectable in collectables:
            if self.colliderect(collectable):
                collectables.remove(collectable)
        
        if len(collectables) == 0:
            win = True

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


        self.alive = True
        self.health = 10


    def draw(self):
        """Delegar o método draw para o Actor interno."""
        self.image.draw()


    def patrol(self):
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
        
    def update(self):
        self.patrol()
        
        


## Positions
player = Player(TILE_SIZE * 5, HEIGHT - (TILE_SIZE * 3))
enemy1 = Enemy(TILE_SIZE * 8, HEIGHT - (TILE_SIZE * 3))


def draw():
    screen.clear()
    
    for platform in platforms:
        platform.draw()

    for collectable in collectables:
        collectable.draw()
    
    for obstacle in obstacles:
        obstacle.draw()

    if player.alive:
        player.draw()

    enemy1.draw()
    
    # game messages
    if over:
        screen.draw.text("Game Over", center=(WIDTH/2, HEIGHT/2))

    if win:
        screen.draw.text("You won!", center=(WIDTH/2, HEIGHT/2))



def update():
    player.update()
    enemy1.update()


pgzrun.go()



# # PLAYER
# player = Actor('rectangle')
# #player.scale = 0.3
# player.bottomleft = (TILE_SIZE * 5, HEIGHT - (TILE_SIZE * 3))
# # player variables
# player.velocity_x = 4
# player.velocity_y = 0
# player.jumping = False
# player.direction = 0
# player.alive = True

## GRAVITY
#jump_velocity = -15
#gravity = 1


# def update():
#     global over, win

#     ### PLAYER ###
#     # moves
#     player.direction = 0

#     if keyboard.left:
#         player.direction = -1
#     if keyboard.right:
#         player.direction = 1

#     player.x += player.direction * player.velocity_x

#     ## X collision with platforms
#     if player.collidelist(platforms) != -1 and player.direction != 0:
#         object = platforms[player.collidelist(platforms)]
#         player.x = object.x - player.direction * (object.width / 2 + player.width / 2)

#     # gravity and jump
#     if keyboard.up and player.jumping == False:
#         player.velocity_y += jump_velocity
#         player.jumping = True

#     player.y += player.velocity_y 
    
#     ## Y collision with platforms
#     if player.collidelist(platforms) != -1:
#         object = platforms[player.collidelist(platforms)]
#         # check if going down
#         if player.velocity_y > 0:
#             player.jumping = False
#             player.y = object.y - (object.height / 2 + player.height / 2)
#         # check if going up
#         elif player.velocity_y < 0:
#             player.y = object.y + (object.height / 2 + player.height / 2)
        
#         player.velocity_y = 0

#     player.velocity_y += gravity

#     ## Collision with obstacles
#     #if player.collidelist(obstacles) != -1:
#         #player.alive = False
#         #over = True

#     ## Collision with collectables
#     for collectable in collectables:
#         if player.colliderect(collectable):
#             collectables.remove(collectable)
    
#     if len(collectables) == 0:
#         win = True