import pygame
import random
from pygame.locals import *

pygame.init()
pygame.mixer.init()
width, height = 1100, 600
screen = pygame.display.set_mode((width,height))
running = 1
high_score = 0
last_time = 0
white = (255,255,255)
black = (0,0,0)
green = (0,255,0)
yellow = (255, 255, 102)
red = (255,0,0)

pygame.mixer.music.load("D:/Python/Avoid obstacles/resources/audio/pygame-a-primer_Apoxode_-_Electric_1.mp3")
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.25)
move_up_sound = pygame.mixer.Sound("D:/Python/Avoid obstacles/resources/audio/pygame-a-primer_Rising_putter.ogg")
move_up_sound.set_volume(0.1)
move_down_sound = pygame.mixer.Sound("D:/Python/Avoid obstacles/resources/audio/pygame-a-primer_Falling_putter.ogg")
move_down_sound.set_volume(0.1)
collision_sound = pygame.mixer.Sound("D:/Python/Avoid obstacles/resources/audio/pygame-a-primer_Collision.ogg")
collision_sound.set_volume(0.3)

# Define a Player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("D:/Python/Avoid obstacles/resources/image/jet1.png").convert() # convert to optimize ?  
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)     # render selected color as transparent, use RLEACCEL to optimize
        self.rect = self.surf.get_rect()
        self.rect.topleft = (width/2,height/2)
        self.speed = 9
        self.max_hp = 70
        self.hp = self.max_hp
    # Move the sprite based on user keypresses
    def update(self, pressed_keys):
        if pressed_keys[K_UP] or pressed_keys[K_w]:
            self.rect.move_ip(0, -self.speed)
            move_up_sound.play()
        if pressed_keys[K_DOWN] or pressed_keys[K_s]:
            self.rect.move_ip(0, self.speed)
            move_down_sound.play()
        if pressed_keys[K_LEFT] or pressed_keys[K_a]:
            self.rect.move_ip(-self.speed, 0)
        if pressed_keys[K_RIGHT] or pressed_keys[K_d]:
            self.rect.move_ip(self.speed, 0)
        # Keep player on the screen
        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, width)
        self.rect.top = max(self.rect.top,0)
        self.rect.bottom = min(self.rect.bottom, height)

# Define the enemy object by extending pygame.sprite.Sprite
# The surface you draw on the screen is now an attribute of 'enemy'
class Enemy(pygame.sprite.Sprite):  
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("D:/Python/Avoid obstacles/resources/image/missile.png")
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        randx = random.randint(width + 20, width + 100)
        randy = random.randint(0, height)
        self.rect = self.surf.get_rect(center=(randx,randy))
        self.speed = random.randint(5,8)

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud,self).__init__()
        self.surf = pygame.image.load("D:/Python/Avoid obstacles/resources/image/cloud.png").convert()
        self.surf.set_colorkey((0,0,0),RLEACCEL)
        randx = random.randint(width +20, width + 100)
        randy = random.randint(0,height)
        self.rect = self.surf.get_rect(center=(randx,randy))
        self.speed = 8
    def update(self):
        self.rect.move_ip(-self.speed,0)
        if self.rect.right < 0:
            self.kill()

# Create groups to hold enemy sprites and all sprites
# - enemies is used for collision detection and position updates
# - all_sprites is used for rendering
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

# Create a custom event for adding a new enemy
# This event acts as QUIT or KEYDOWN event 
add_enemy = pygame.USEREVENT + 1
pygame.time.set_timer(add_enemy, 160)   # it will occur every ??? miliseconds
add_cloud = pygame.USEREVENT + 2
pygame.time.set_timer(add_cloud, 350)

def end_screen():
    global high_score
    str_len = [55,25,36]
    font_style = pygame.font.SysFont("bahnschrift", str_len[0])
    mesg = font_style.render("SCORE: "+str(current_time//1000), True, black)
    trect = mesg.get_rect(center=(width/2,height/2-30))
    screen.blit(mesg,trect)
    font_style = pygame.font.SysFont("bahnschrift", str_len[1])
    high_score = max(high_score,current_time//1000)
    hs = pygame.font.SysFont("bahnschrift", 20).render("HIGHSCORE: "+str(high_score),True,black)
    hs_rect = hs.get_rect(center=(width/2,height/2+10))
    screen.blit(hs,hs_rect)
    font_style = pygame.font.SysFont("bahnschrift", str_len[2])
    restart = font_style.render("Press R To Restart",True,black)
    restart_rect = restart.get_rect(center=(width/2,height/2-30+str_len[0]+str_len[1]))
    screen.blit(restart,restart_rect)
def restart():
    global total_time, running
    wait = 1
    while wait:
        total_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    exit(0)
                if event.key == K_r:
                    running = 1
                    wait = 0
                    break
        pygame.display.flip()
def take_input():
    for event in pygame.event.get():
        if event.type==pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==K_ESCAPE):
            running = 0
            pygame.quit()
            exit(0)
        if event.type==add_enemy:
            # Create the new enemy and add it to sprite groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
        if event.type==add_cloud:
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)      
def update():
    # Get the set of keys pressed and check for user input      
    # Return boolean values represent key's state -> cannot identify key order -> use KEYDOWN instead
    pressed_keys = pygame.key.get_pressed() 
    # Update the player sprite based on user keypresses
    player.update(pressed_keys)
    enemies.update()
    clouds.update()
def draw():
    # HP bar 
    pygame.draw.rect(screen,black,(10,10,player.max_hp*3.5,30))
    pygame.draw.rect(screen,green,(10,10,player.hp*3.5,30))

    font_25 = pygame.font.SysFont("comicsansms", 25)
    font_45 = pygame.font.SysFont("comicsansms", 45)
    t_text = font_45.render("Time: "+str(current_time//1000),True,black)
    t_rect = t_text.get_rect(topright=(width,0))
    screen.blit(t_text,t_rect)
    current_life = font_25.render("HP: "+str(player.hp),True,red)
    screen.blit(current_life,(12,8))
def collide():
    global running
    # Check if any enemies have collided with the player
    if pygame.sprite.spritecollideany(player, enemies):
    # If so, then remove the player and stop the loop
        player.hp-=1
        # Stop any moving sounds and play the collision sound
        move_up_sound.stop()
        move_down_sound.stop()
        collision_sound.play()
        if(player.hp==0):
            for entity in all_sprites:
                entity.kill()
            running = False
while 1:
    player = Player()   
    all_sprites.add(player)
    while running:
        total_time = pygame.time.get_ticks()
        current_time = total_time - last_time
        screen.fill((135, 206, 250))
        take_input()
        update()
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)
        collide()
        draw()
        pygame.display.flip()
        clock = pygame.time.Clock()
        clock.tick(100)
    end_screen()
    restart()
    last_time = total_time
# All done! Stop and quit the mixer.
pygame.mixer.music.stop()
pygame.mixer.quit()
