import pygame
import random
from pygame.locals import *

pygame.init()
pygame.mixer.init()

width, height = 1200,600
screen = pygame.display.set_mode((width,height))    

background = pygame.image.load("D:/Python/Alien Invasion/resources/image/background.png")
background = pygame.transform.scale(background,(width,height))
pygame.mixer.music.load("D:/Python/Alien Invasion/resources/audio/background.wav")
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.17)
explose = pygame.mixer.Sound("D:/Python/Alien Invasion/resources/audio/explosion.wav")
explose.set_volume(0.2)
laser = pygame.mixer.Sound("D:/Python/Alien Invasion/resources/audio/laser.wav")
laser.set_volume(0.2)

white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
black = (0,0,0)

total_enemies = 0
enemies_left = 0
next_row = 60
enemy_each_row = 17
class stop_watch:
    def __init__(self):
        self.init_time = pygame.time.get_ticks()
    def get(self):
        return pygame.time.get_ticks()-self.init_time
    def reset(self):
        self.init_time = pygame.time.get_ticks()
timer = stop_watch()
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player,self).__init__()
        self.surf = pygame.image.load("D:/Python/Alien Invasion/resources/image/player.png")
        self.surf.set_colorkey(white,RLEACCEL)
        self.rect = self.surf.get_rect(topleft=(width/2,height-100))
        self.speed = 4
    def update(self,press):
        if press[K_UP] or press[K_w]:
            self.rect.move_ip(0, -self.speed)
        if press[K_DOWN] or press[K_s]:
            self.rect.move_ip(0, self.speed)
        if press[K_LEFT] or press[K_a]:
            self.rect.move_ip(-self.speed, 0)
        if press[K_RIGHT] or press[K_d]:
            self.rect.move_ip(self.speed, 0)
        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, width)
        self.rect.top = max(self.rect.top,height-200)
        self.rect.bottom = min(self.rect.bottom, height)
player = Player()
class Enemy(pygame.sprite.Sprite):    
    def __init__(self,cnt):
        super(Enemy,self).__init__()
        if cnt%2==0:
            self.surf = pygame.image.load("D:/Python/Alien Invasion/resources/image/enemy.png")
        else:
            self.surf = pygame.image.load("D:/Python/Alien Invasion/resources/image/ufo.png")
            self.surf = pygame.transform.scale(self.surf,(64,64))
        self.surf.set_colorkey((white),RLEACCEL)
        self.rect = self.surf.get_rect()
        self.rect.left = (cnt%enemy_each_row) * (self.rect.width+5)
        self.rect.top = (cnt//enemy_each_row) * next_row
        self.speed = 2
        if (cnt//enemy_each_row) % 2 == 0:
            self.speed = -self.speed
    def update(self):
        self.rect.move_ip(self.speed,0)
        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, width)
        self.rect.top = max(self.rect.top,0)
        self.rect.bottom = min(self.rect.bottom, height)
        if self.rect.right == width or self.rect.left == 0:
            self.rect.move_ip(0,next_row)
            self.speed = -self.speed
class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super(Bullet,self).__init__()
        self.surf = pygame.image.load("D:/Python/Alien Invasion/resources/image/bullet.png")
        self.surf.set_colorkey((white),RLEACCEL)
        self.rect = self.surf.get_rect()
        self.rect.topleft = (player.rect.centerx-17,player.rect.centery)
        self.speed = 5
    def update(self):
        self.rect.move_ip(0,-self.speed)
        if self.rect.top <= 0:
            self.kill()

enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

reload_time = 1000
reload_until = 0
def shoot():
    global shot, reload_time, reload_until
    if timer.get() < reload_until:
        return
    reload_until = timer.get() + reload_time
    shot += 1
    new_bullet = Bullet()
    bullets.add(new_bullet)
    all_sprites.add(new_bullet)
    laser.play()
def print_reload():
    reloading_font = pygame.font.Font(None, 60)
    reload_word = reloading_font.render("RELOADING...",True,black)
    textRect = reload_word.get_rect(bottomleft = (0,height))
    screen.blit(reload_word,textRect)

shot = 0
state = 0

def ask_ene():
    global total_enemies
    while 1:
        screen.blit(background,(0,0))
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                exit(0)
            if event.type==pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    exit(0)
                if event.key == K_BACKSPACE:
                    total_enemies //= 10
                if event.key == K_RETURN:
                    return
                x = pygame.key.name(event.key)
                if x >= '0' and x <= '9':
                    total_enemies = total_enemies*10+int(x)        
        font_style = pygame.font.SysFont("bahnschrift", 50)
        mesg = font_style.render("SELECT TOTAL ENEMY: "+str(total_enemies), True, white)
        screen.blit(mesg,mesg.get_rect(center=(width/2,height/2-30)))
        pygame.display.flip()
def ask_user():
    global total_enemies, enemies_left
    ask_ene()
    enemies_left = total_enemies
    for e in range(total_enemies):
        new_enemy = Enemy(e)
        enemies.add(new_enemy)
        all_sprites.add(new_enemy)
def end_screen():
    global alr_ask, state
    font = pygame.font.Font(None, 100)
    statement = ["HUMAN VICTORY",green]
    if state == 0:
        statement = ["ALIEN VICTORY",red]
    word = font.render(statement[0],True,statement[1])
    textRect = word.get_rect(center=(width/2,height/2))
    screen.blit(word,textRect)
    font_style = pygame.font.SysFont("bahnschrift", 60)
    restart = font_style.render("Press R To Restart",True,black)
    restart_rect = restart.get_rect(center=(width/2,height/2+50))
    screen.blit(restart,restart_rect)
    wait = 1
    while wait:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == K_r:
                    wait = 0
                    alr_ask = 0
                    state = 0
        pygame.display.flip()
    for i in enemies:
        i.kill()
    for i in all_sprites:
        i.kill()
    for i in bullets:
        i.kill()
def take_input():
    global shot
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            exit(0)
        if event.type==pygame.KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                exit(0) 
            if event.key == K_SPACE:
                shoot()
def reload_bar():
    rb_height = 25
    rect = pygame.Rect(0,0,200,rb_height)
    rect.bottomleft = (10,height-10)
    pygame.draw.rect(screen,black,rect)
    percent = 1 - max(reload_until-timer.get(),0) / reload_time
    rect1 = pygame.Rect(0,0,percent*200,rb_height)
    rect1.bottomleft = rect.bottomleft
    pygame.draw.rect(screen,green,rect1)
def update():
    press = pygame.key.get_pressed()
    player.update(press)
    enemies.update()
    bullets.update()
    for entity in all_sprites:
        screen.blit(entity.surf,entity.rect)
def collide():
    global enemies_left
    for e in enemies:
        for b in bullets:
            if e.rect.colliderect(b.rect):
                enemies_left -= 1
                e.kill()
                b.kill()
                explose.play()
def game_state():
    global state, running, enemies_left
    if enemies_left == 0:
        state = 1
        running = 0
    if pygame.sprite.spritecollideany(player,enemies):
        running = 0
def restart():
    global running, total_enemies, state, player, enemies_left, reload_until
    for i in enemies:
        i.kill()
    for i in bullets:
        i.kill()
    for i in all_sprites:
        i.kill()
    reload_until = 0
    running = 1
    total_enemies = 0
    enemies_left = 0
    timer.reset()
    state = 0
    player = Player()
    all_sprites.add(player)
def draw_info():
    global total_enemies, enemies_left
    font = pygame.font.SysFont("Corbel",45)
    left = font.render("Spaceship: "+str(enemies_left)+"/"+str(total_enemies),True,white)
    screen.blit(left,left.get_rect(bottomright=(width,height)))
running = 1
while 1:
    restart()
    ask_user()
    while running:
        take_input()
        reload_bar()
        update()
        collide()
        draw_info()
        game_state()
        pygame.display.flip()
    end_screen()
