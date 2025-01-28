from pygame import Rect
from pgzero.actor import Actor
from platformer import *
from pgzero.builtins import keyboard

from config import *

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

        self.holding = None

    def rect(self):
        """Retorna o retângulo da gem como um objeto Rect."""
        return Rect(self.x, self.y, self.image.width, self.image.height)

    def collidelist(self, objects):
        """Delegar collidelist para o Actor interno."""
        return self.image.collidelist(objects)
    
    def colliderect(self, rect):
        """Delegar colliderect para o Actor interno."""
        return self.image.colliderect(rect)

    def draw(self):
        """Delegar o método draw para o Actor interno."""
        self.image.draw()

    def stop_holding(self, gems, trigger):
        if not self.holding: 
            return

        if trigger == "enemy":  
            self.holding.delete(gems)
            #gems.remove(self.holding)
            print("Gema removida devido a inimigo!")

        #print("Soltou a gem!")
        
        self.holding.being_held = False 
        self.holding = None  

    def stop_velocity_y(self, gem, object):
        print("COLIDIU cima")
        gem.image.top = object.bottom
        self.image.top = gem.image.bottom
        self.velocity_y = 0
        

    def stop_velocity_x(self, object):
        print("COLIDIU lado")
        #self.image.x = thing.image.x
        if self.direction > 0:  # Movendo-se para a direita
            self.image.right = object.left
        elif self.direction < 0:  # Movendo-se para a esquerda
            self.image.left = object.right


    def update(self, gems):
        global over, win

        # moves
        self.direction = 0

        if keyboard.a:
            self.direction = -1
        if keyboard.d:
            self.direction = 1

        self.image.x += self.direction * self.velocity_x

        platforms = get_platforms() 

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

        if self.holding:
            if self.holding.collidelist(platforms) != -1:
                object = platforms[self.holding.collidelist(platforms)]
                # check if going up
                if self.velocity_y < 0:
                    #player.stop_velocity_y(self, object)
                    self.holding.image.top = object.bottom
                    self.image.top = self.holding.image.bottom
                
                self.velocity_y = 0

            if self.holding.collidelist(platforms) != -1: 
                object = platforms[self.holding.collidelist(platforms)]
                
                if self.direction > 0:  # Movendo para a direita
                    self.image.right = object.left
                    self.holding.image.right = object.left
                    #player.stop_velocity_x(object)
                elif self.direction < 0:  # Movendo para a esquerda
                    self.image.left = object.right
                    self.holding.image.left = object.right

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

        # if self.collidelist(gems):
        #     object = self.collidelist(gems)
        #     # check if going down
        #     if self.velocity_y > 0:
        #         self.jumping = False
        #         self.image.bottom = object.top
        #     # check if going up
        #     elif self.velocity_y < 0:
        #         self.image.top = object.bottom
            
        #     self.velocity_y = 0

        self.velocity_y += gravity 

        ## Collision with gem blocks
        for gem in gems:
            if self.rect().colliderect(gem.rect()):
                if keyboard.e and self.holding is None:
                    self.holding = gem
                    gem.being_held = True
                    #self.numofgems += 1
                    #print(self.numofgems)
                    break

                object = gem.image
                if self.velocity_y > 0 and not gem.being_held:
                    if self.image.bottom < object.bottom:
                        self.jumping = False
                        self.image.bottom = object.top
                    self.velocity_y = 0


        if keyboard.f and self.holding:
            self.stop_holding(gems, None)


        self.y = self.image.y  
        self.x = self.image.x  

class Enemy():

    def __init__(self, x, y):
        self.image = Actor('rectenemy')
        self.image.bottomleft = ((x, y))
        self.x = x
        self.y = y
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

    def rect(self):
        """Retorna o retângulo da gem como um objeto Rect."""
        return Rect(self.x, self.y, self.image.width, self.image.height)

    def draw(self):
        """Delegar o método draw para o Actor interno."""
        self.image.draw()


    def update(self, player, gems):
        """Atualiza o comportamento do inimigo."""
        # Calcular a distância do jogador

        self.x = self.image.x
        self.y = self.image.y

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
        
        for gem in gems: # if the enemy collides with the gem in his path
            if self.rect().colliderect(gem.rect()):
                gem.delete(gems)
                self.currentgems += 1
                print("Inimigo pegou a gema")
                print(self.currentgems)

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
                if player.holding != None:
                    player.stop_holding(gems, "enemy")
                    #player.numofgems -= 1
                    self.currentgems += 1
                    print("Inimigo pegou a gema")
                    print(self.currentgems)
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

class BigGem():
    
    def __init__(self, x, y):
        self.image = Actor('tile_0091')
        self.image.bottomleft = ((x, y))
        self.x = x
        self.y = y
        self.direction = 1
        self.velocity_x = 2
        self.velocity_y = 0
        self.being_held = False

    def rect(self):
        """Retorna o retângulo da gem como um objeto Rect."""
        return Rect(self.x, self.y, self.image.width, self.image.height)
 
    def collidelist(self, objects):
        """Delegar collidelist para o Actor interno."""
        return self.image.collidelist(objects)
    
    def colliderect(self, rect):
        """Delegar colliderect para o Actor interno."""
        return self.image.colliderect(rect)

    def delete(self, gems):
        """Remove esta gem da lista de gems."""
        if self in gems:
            gems.remove(self)
            print("Gema deletada!")

    def draw(self):
        """Delegar o método draw para o Actor interno."""
        self.image.draw()

    def update(self, player):
        
        platforms = get_platforms() 

        if self.being_held:
            
            self.direction = player.direction
            self.velocity_y = 0

            self.image.x = player.x
            #self.image.y = self.y   
            self.image.bottom = player.image.top      

            ## Y collision with platforms
            # if self.collidelist(platforms) != -1:
            #     object = platforms[self.collidelist(platforms)]
            #     # check if going up
            #     if player.velocity_y < 0:
            #         #player.stop_velocity_y(self, object)
            #         self.image.top = object.bottom
            #         player.image.top = self.image.bottom
                
            #         player.velocity_y = 0
                    
                    # print(f'V: gem top: {self.image.top}, object bot: {object.bottom}')
                    # print(f'V: player top: {player.image.top}, gem bot: {self.image.bottom}')

            ## X collision with platforms
            # if self.collidelist(platforms) != -1: 
            #     object = platforms[self.collidelist(platforms)]
                
            #     if self.direction > 0 and self.image.top <= object.bottom:  # Movendo para a direita
            #         player.image.right = object.left
            #         self.image.right = object.left
            #         #player.stop_velocity_x(object)
            #     elif self.direction < 0 and self.image.top <= object.bottom:  # Movendo para a esquerda
            #         player.image.left = object.right
            #         self.image.left = object.right
            #         #player.stop_velocity_x(object)
                
            #     print(f'L: gem x: {self.image.x}, object x: {object.x}')
                

            #self.image.y = self.y
            #self.image.bottom = player.image.top
            #self.image.y = self.y

            # ## Y collision with platforms
            # if self.collidelist(platforms) != -1:
            #     object = platforms[self.collidelist(platforms)]
            #     # check if going up
            #     if player.velocity_y < 0:
            #         self.image.top = object.bottom
            #         player.image.top = self.image.bottom
            #         #self.image.top = object.bottom
            #         #player.image.top = self.image.bottom
                
            #     self.velocity_y = 0
            
            # if self.collidelist(platforms) != -1: 
            #     object = platforms[self.collidelist(platforms)]
            #     if self.direction > 0:  # Movendo para a direita
            #         #self.image.right = object.left
            #         player.stop_velocity_x(object)
            #     elif self.direction < 0:  # Movendo para a esquerda
            #         #self.image.left = object.right
            #         player.stop_velocity_x(object)

            
            # ## Y collision with platforms
            # if self.collidelist(platforms) != -1:
            #     object = platforms[self.collidelist(platforms)]
            #     # check if going up
            #     if player.velocity_y < 0:
            #         player.stop_velocity_y(self, object)
            #         #self.image.top = object.bottom
            #         #player.image.top = self.image.bottom
                
            #     self.velocity_y = 0
            
            #self.image.x = player.x
            
            self.x = self.image.x
            self.y = self.image.y


        else:
            
            if self.collidelist(platforms) != -1: 
                object = platforms[self.collidelist(platforms)]
                if self.direction > 0:  # Movendo para a direita
                    self.image.right = object.left
                elif self.direction < 0:  # Movendo para a esquerda
                    self.image.left = object.right

            # if self.colliderect(player):
            #     object = player
            #     if player.direction > 0:  # Movendo-se para a direita
            #         self.image.left = object.right
            #         self.direction = player.direction
            #     elif player.direction < 0:  # Movendo-se para a esquerda
            #         self.image.right = object.left
            #         self.direction = player.direction


            self.y += self.velocity_y 
            self.image.y = self.y  # Atualizar posição do Actor
            
            ## Y collision with platforms
            if self.collidelist(platforms) != -1:
                object = platforms[self.collidelist(platforms)]
                # check if going down
                if self.velocity_y > 0:
                    self.image.bottom = object.top
                # check if going up
                elif self.velocity_y < 0:
                    self.image.top = object.bottom
                
                self.velocity_y = 0

            self.velocity_y += gravity

            #print(self.image.midtop)
            self.y = self.image.y  # Atualizar posição
            self.x = self.image.x  # Atualizar posição




# ## Collision with obstacles
# if self.collidelist(obstacles) != -1:
#     self.alive = False
#     over = True

# ## Collision with collectables
# for collectable in collectables:
#     if self.colliderect(collectable):
#         collectables.remove(collectable)