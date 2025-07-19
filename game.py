import pgzrun
from pgzero.rect import Rect

WIDTH = 800
HEIGHT = 600
TITLE = "Plataformer Game"

GRAVITY = 0.5
PLAYER_SPEED = 4
JUMP_STRENGTH = -12
ANIMATION_SPEED = 0.1
sounds_enabled = True

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

##########
# Objects
##########
player = Player((50, HEIGHT - 100))
platforms = [
    Platform((0, HEIGHT - 40), (WIDTH, 40)) # floor
]

def draw():
    """ Desenha tudo na tela. """
    screen.fill((20, 20, 80)) # dark background
    for p in platforms:
        p.draw()
    player.draw()

def update():
    player.update(platforms)

pgzrun.go()