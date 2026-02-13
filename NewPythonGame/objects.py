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
        """Returns the rectangle as a Rect object."""
        return Rect(self.x, self.y, self.image.width, self.image.height)

    def collidelist(self, objects):
        """Delegates collidelist to the intern Actor."""
        return self.image.collidelist(objects)
    
    def colliderect(self, rect):
        """Delegates colliderect to the intern Actor."""
        return self.image.colliderect(rect)

    def draw(self):
        """Delegates draw method to the intern Actor."""
        self.image.draw()

    def stop_holding(self, gems, trigger):
        if not self.holding: 
            return

        if trigger == "enemy":  
            self.holding.delete(gems)
            #gems.remove(self.holding)
            print("Gem removed by the enemy!")

        #print("released gem!")
        
        self.holding.being_held = False 
        self.holding = None  

    def stop_velocity_y(self, gem, object):
        print("COLLIDED above")
        gem.image.top = object.bottom
        self.image.top = gem.image.bottom
        self.velocity_y = 0
        

    def stop_velocity_x(self, object):
        print("COLLIDED side")
        #self.image.x = thing.image.x
        if self.direction > 0:  # Moving to the right
            self.image.right = object.left
        elif self.direction < 0:  # Moving to the left
            self.image.left = object.right


    def update(self, gems):
        #global over, win

        # moves
        self.direction = 0

        if keyboard.a:
            self.direction = -1
        if keyboard.d:
            self.direction = 1

        platforms = get_platforms() 

        if self.holding:
        
            self.image.x += self.direction * self.velocity_x

            self.holding.image.x = self.image.x
            self.holding.image.bottom = self.image.top
            self.holding.direction = self.direction

            ## X GEM 
            if self.holding.collidelist(platforms) != -1:
                # set_state('pause')
                object = platforms[self.holding.collidelist(platforms)]
                if self.holding.direction > 0:  # Moving to the right
                    #print("Side: G Right")
                    self.holding.image.right = object.left
                    self.image.right = object.left
                    #self.holding.direction = 0
                elif self.holding.direction < 0:  # Moving to the left
                    #print("Side: G Left")
                    self.holding.image.left = object.right
                    self.image.left = object.right
                    #self.holding.direction = 0
                    
            ## X collision with platforms
            if self.collidelist(platforms) != -1 and self.direction != 0:
                object = platforms[self.collidelist(platforms)]
                if self.direction > 0:  # Moving to the right
                    # print("Side: P Right")
                    self.image.right = object.left
                elif self.direction < 0:  # Moving to the left
                    # print("Side: P Left")
                    self.image.left = object.right
     
            # gravity and jump
            if keyboard.w and self.jumping == False:
                self.velocity_y += self.jump_velocity
                self.jumping = True

            self.y += self.velocity_y 
            self.image.y = self.y  # Update Actor position
            self.holding.image.bottom = self.image.top

            ## Y collision with platforms
            if self.collidelist(platforms) != -1:
                object = platforms[self.collidelist(platforms)]
                # check if going down
                if self.velocity_y > 0:
                    #print("L: P Chão")
                    self.jumping = False
                    self.image.bottom = object.top
                
                self.velocity_y = 0

            ## Y GEM
            if self.holding.collidelist(platforms) != -1:
                object = platforms[self.holding.collidelist(platforms)]
                # check if going up
                if self.velocity_y < 0:
                    print("L: G Above")
                    self.holding.image.top = object.bottom
                    self.image.top = self.holding.image.bottom
    
                self.velocity_y = 0

            self.velocity_y += gravity

            self.holding.direction = self.direction
            self.holding.x = self.holding.image.x
            self.holding.y = self.holding.image.y
            
        else:

            self.image.x += self.direction * self.velocity_x

            ## X collision with platforms
            if self.collidelist(platforms) != -1 and self.direction != 0:
                object = platforms[self.collidelist(platforms)]
                if self.direction > 0:  # Moving to the right
                    self.image.right = object.left
                elif self.direction < 0:  # Moving to the left
                    self.image.left = object.right
            
            # gravity and jump
            if keyboard.w and self.jumping == False:
                self.velocity_y += self.jump_velocity
                self.jumping = True

            self.y += self.velocity_y 
            self.image.y = self.y  # Update Actor position

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


#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#

class Enemy():

    def __init__(self, x, y, range):
        self.image = Actor('rectenemy')
        self.image.bottomleft = ((x, y))
        self.x = x
        self.y = y
        self.start_x = x  # Inicial position in axe X
        self.patrol_range = range  # Patrol movement range
        self.speed = 1.5  # Movement speed
        self.direction = 1  # Inicial direction (1 = right, -1 = left)
        self.wait_time = 1  # Waiting time before changing direction
        self.waiting = False  # Waiting status
        self.last_wait_time = 0  # Time since last wainted
        self.detection_radius = 120  # Detection radius to detect the player
        self.chasing = False  # Checks if it is in chasing state
        self.patrolling = True # Checks if it is in patrolling state
        self.forcedwaiting = False


        self.locked = True
        self.totalgems = 3
        self.currentgems = 0

    def rect(self):
        """Returns the rectangle as a Rect object."""
        return Rect(self.x, self.y, self.image.width, self.image.height)

    def draw(self):
        """Delegates draw method to the intern Actor."""
        self.image.draw()


    def update(self, player, gems):
        """Updates Enemy Behavior"""

        self.x = self.image.x
        self.y = self.image.y

        # Calculates the distance to the player
        distance_to_player = abs(self.image.x - player.image.x)

        if self.currentgems == self.totalgems:
            # go to sleep, open the path to the player
            return

        # forced waiting state after interacting with player
        if self.forcedwaiting == True: 
            if time.time() - self.last_wait_time >= self.wait_time:
                self.forcedwaiting = False  # Stop waiting
                self.direction *= -1  # Invert direction 
            return  # While waiting, don't move
        
        for gem in gems: # if the enemy collides with the gem in his path
            if self.rect().colliderect(gem.rect()):
                gem.delete(gems)
                self.currentgems += 1
                print("Enemy caught the gem")
                print(self.currentgems)

        # Switches to chasing state if the player is near
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
            # Chases player
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
                    print("Enemy caught the gem")
                    print(self.currentgems)
                else:
                    print("ATTACK")
                
                # setting the enemy to forced waiting after interation
                self.chasing = False
                self.patrolling = True
                self.forcedwaiting = True
                self.last_wait_time = time.time() 

        elif self.patrolling:
            # Patrolling
            if self.waiting:
                # Verifies if waiting time is over
                if time.time() - self.last_wait_time >= self.wait_time:
                    self.waiting = False  # Stop waiting
                    self.direction *= -1  # Invert direction
                return  # While waiting, don't move
            

            # Patrol Movement
            self.image.x += self.direction * self.speed

            # Verify patrol limits
            if self.image.x >= self.start_x + self.patrol_range or self.image.x <= self.start_x:
                self.waiting = True  # Enter waiting state
                self.last_wait_time = time.time() 


#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#


class LittleEnemy():

    def __init__(self, x, y, range):
        self.image = Actor('rectenemy_little')
        self.image.bottomleft = ((x, y))
        self.x = x
        self.y = y
        self.start_x = x  # Inicial position in axe X
        self.patrol_range = range  # Patrol movement range
        self.speed = 2  # Movement speed
        self.direction = 1 # Inicial direction (1 = right, -1 = left)
        self.wait_time = 0.3  # Waiting time before changing direction
        self.waiting = False  # Waiting status
        self.last_wait_time = 0  # Time since last wainted
        self.detection_radius = 70  # Detection radius to detect the player
        self.chasing = False  # Checks if it is in chasing state
        self.patrolling = True # Checks if it is in patrolling state
        self.forcedwaiting = False


        self.locked = True
        self.totalgems = 1
        self.currentgems = 0

    def rect(self):
        """Returns the rectangle as a Rect object."""
        return Rect(self.x, self.y, self.image.width, self.image.height)

    def draw(self):
        """Delegates draw method to the intern Actor."""
        self.image.draw()


    def update(self, player, gems):
        """Updates Enemy Behavior"""

        self.x = self.image.x
        self.y = self.image.y

        # Calculates the distance to the player
        distance_to_player = abs(self.image.x - player.image.x)

        if self.currentgems == self.totalgems:
            # go to sleep, open the path to the player
            return

        # forced waiting state after interacting with player
        if self.forcedwaiting == True: 
            if time.time() - self.last_wait_time >= self.wait_time:
                self.forcedwaiting = False  # Stop waiting
                self.direction *= -1  # Invert direction  
            return  # While waiting, don't move
        
        for gem in gems: # if the enemy collides with the gem in his path
            if self.rect().colliderect(gem.rect()):
                gem.delete(gems)
                self.currentgems += 1
                print("Little Enemy caught the gem")
                print(self.currentgems)

        # Switches to chasing state if the player is near
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
            # Chases player
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
                    print("Little Enemy caught the gem")
                    print(self.currentgems)
                else:
                    print("ATTACK")
                
                # setting the enemy to forced waiting after interation
                self.chasing = False
                self.patrolling = True
                self.forcedwaiting = True
                self.last_wait_time = time.time() 

        elif self.patrolling:
            # Patrolling
            if self.waiting:
                # Verifies if waiting time is over
                if time.time() - self.last_wait_time >= self.wait_time:
                    self.waiting = False  # Stop waiting
                    self.direction *= -1  # Invert direction
                return  # While waiting, don't move
            

            # Patrol Movement
            self.image.x += self.direction * self.speed

            # Verify patrol limits
            if self.image.x >= self.start_x + self.patrol_range or self.image.x <= self.start_x:
                self.waiting = True  # Enter waiting state
                self.last_wait_time = time.time() 


#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#

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
        """Returns the rectangle as a Rect object."""
        return Rect(self.x, self.y, self.image.width, self.image.height)
 
    def collidelist(self, objects):
        """Delegates collidelist to the intern Actor."""
        return self.image.collidelist(objects)
    
    def colliderect(self, rect):
        """Delegates colliderect to the intern Actor."""
        return self.image.colliderect(rect)

    def delete(self, gems):
        """Remove this gem from gems list."""
        if self in gems:
            gems.remove(self)
            print("Gema deletada!")

    def draw(self):
        """Delegates draw method to the intern Actor."""
        self.image.draw()

    def update(self, player):
        
        platforms = get_platforms() 

        if self.being_held:
            
            self.velocity_y = 0

        else:
            
            if self.collidelist(platforms) != -1: 
                object = platforms[self.collidelist(platforms)]
                if self.direction > 0:  # Moving to the right
                    self.image.right = object.left
                elif self.direction < 0:  # Moving to the left
                    self.image.left = object.right


            self.y += self.velocity_y 
            self.image.y = self.y  # Update Actor position
            
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
            self.y = self.image.y  # Update Y position
            self.x = self.image.x  # Update X position
