import pgzrun
from pgzero.rect import Rect
import random

WIDTH = 800
HEIGHT = 600
TITLE = "Plataformer Game"

GRAVITY = 0.5
PLAYER_SPEED = 4
JUMP_STRENGTH = -12
ANIMATION_SPEED = 0.1
sounds_enabled = True
game_state = 'playing'  # 'menu' / 'playing' / 'game_over' / 'win'

##########
# Classes
##########
class Player:
    def __init__(self, pos):
        self.rect = Rect(pos, (30, 50))
        self.actor = Actor('alien_idle', anchor=('center', 'bottom'))
        self.actor.pos = self.rect.centerx, self.rect.bottom
        
        self.velocity_y = 0
        self.on_ground = False
        self.direction = 1
        
        self.walk_frames = ['alien_walk_a', 'alien_walk_b']
        self.current_frame = 0
        self.animation_timer = 0
        self.is_walking = False

    def move(self, platforms):
        self.is_walking = False
        if keyboard.left:
            self.rect.x -= PLAYER_SPEED
            self.direction = -1
            self.is_walking = True
        elif keyboard.right:
            self.rect.x += PLAYER_SPEED
            self.direction = 1
            self.is_walking = True

        if keyboard.up and self.on_ground:
            self.velocity_y = JUMP_STRENGTH
            self.on_ground = False
            if sounds_enabled:
                sounds.jump.play()

        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y
        self.on_ground = False
        
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                # player is falling
                if self.velocity_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.on_ground = True
                    self.velocity_y = 0
                # player is rising
                elif self.velocity_y < 0:
                    self.rect.top = platform.rect.bottom
                    self.velocity_y = 0 

    def animate(self):
        if not self.on_ground:
            self.actor.image = 'alien_jump'
        elif self.is_walking:
            self.animation_timer += 1 / 60
            if self.animation_timer > ANIMATION_SPEED:
                self.animation_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames)
                self.actor.image = self.walk_frames[self.current_frame]
        else:
            self.actor.image = 'alien_idle'

    def update(self, platforms):
        self.move(platforms)
        self.animate()
        self.actor.pos = self.rect.centerx, self.rect.bottom
    
    def reset(self, pos):
        self.rect.topleft = pos
        self.velocity_y = 0
        self.on_ground = True
    
    def draw(self):
        self.actor.draw()

class Platform:
    def __init__(self, pos, size):
        self.rect = Rect(pos, size)
        self.tiles = []
        
        tile_actor_temp = Actor('platform')
        tile_size = tile_actor_temp.width
        num_tiles = int(size[0] / tile_size)
       
        for i in range(num_tiles):
            tile_pos = (pos[0] + i * tile_size, pos[1])
            tile = Actor('platform', topleft=tile_pos)
            self.tiles.append(tile)

    def draw(self):
        for tile in self.tiles:
            tile.draw()

class Enemy:
    def __init__(self, pos, patrol_range):
        self.rect = Rect(pos, (30, 50)) 
        self.actor = Actor('enemy_attack_a', anchor=('center', 'bottom'))
        self.actor.pos = self.rect.centerx, self.rect.bottom

        self.start_x = self.rect.x
        self.end_x = self.rect.x + patrol_range
        self.speed = random.uniform(1.0, 2.0)
        
        self.animation_frames = ['enemy_attack_a', 'enemy_attack_b']
        self.current_frame = 0
        self.animation_timer = 0
        
    def update(self):
        self.rect.x += self.speed
        if self.rect.right > self.end_x or self.rect.left < self.start_x:
            self.speed *= -1
        self.actor.pos = self.rect.centerx, self.rect.bottom
        
        # Enemy animation
        self.animation_timer += 1/60
        if self.animation_timer > ANIMATION_SPEED * 2:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.animation_frames)
            self.actor.image = self.animation_frames[self.current_frame]

    def draw(self):
        self.actor.draw()

##########
# Objects
##########
platforms = []
enemies = []
player = Player((50, HEIGHT - 100))
goal = Actor('flag', pos=(WIDTH - 50, 60))


############
# Functions
############
def setup_level():
    global platforms, enemies
    platforms.clear()
    enemies.clear()

    ground_platform = Platform((0, HEIGHT - 40), (WIDTH, 40))
    p1 = Platform((175, HEIGHT - 150), (150, 20))
    p2 = Platform((375, HEIGHT - 250), (200, 20))
    p3 = Platform((150, HEIGHT - 350), (150, 20))
    p4 = Platform((400, HEIGHT - 450), (175, 20))
    goal_platform = Platform((WIDTH - 150, 100), (150, 20))
    platforms = [ground_platform, p1, p2, p3, p4, goal_platform]

    # Position the player
    player.rect.x = 50
    player.rect.bottom = ground_platform.rect.top
    player.on_ground = True
    player.velocity_y = 0

    # Position the enemies
    enemy1 = Enemy(pos=(p2.rect.x + 10, p2.rect.top - 50), patrol_range=160)
    enemies.append(enemy1)
    enemy2 = Enemy(pos=(p3.rect.x + 10, p3.rect.top - 50), patrol_range=110)
    enemies.append(enemy2)

    # Position the goal flag
    goal.bottom = goal_platform.rect.top
    goal.centerx = goal_platform.rect.centerx

def draw():
    screen.fill((20, 20, 80))
    goal.draw()
    for p in platforms:
        p.draw()
    for e in enemies:
        e.draw()
    player.draw()

def update():
    player.update(platforms)
    for e in enemies:
        e.update() 

setup_level()
pgzrun.go()