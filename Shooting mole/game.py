import pygame
from pygame.locals import *
import math
import random

pygame.init()
pygame.mixer.init()

width, height = 1218, 630
screen=pygame.display.set_mode((width, height))
black = (0,0,0)
white = (255,255,255)
green = (0,255,0)
red = (255,0,0)

# 3 - Load images
grass = pygame.image.load("D:/Python/shooting mole/resources/images/grass.png")
castle = pygame.image.load("D:/Python/shooting mole/resources/images/castle.png")
healthbar = pygame.image.load("D:/Python/shooting mole/resources/images/healthbar.png")
health = pygame.image.load("D:/Python/shooting mole/resources/images/health.png")
lose_screen = pygame.image.load("D:/Python/shooting mole/resources/images/gameover.png")
lose_screen = pygame.transform.scale(lose_screen,(width,height))
win_screen = pygame.image.load("D:/Python/shooting mole/resources/images/youwin.png")
win_screen = pygame.transform.scale(win_screen,(width,height))

# 3.1 - Load audio
hit = pygame.mixer.Sound("D:/Python/shooting mole/resources/audio/explode.wav")
enemy = pygame.mixer.Sound("D:/Python/shooting mole/resources/audio/enemy.wav")
shoot = pygame.mixer.Sound("D:/Python/shooting mole/resources/audio/shoot.wav")
hit.set_volume(0.1)
enemy.set_volume(0.1)
shoot.set_volume(0.1)
pygame.mixer.music.load('D:/Python/shooting mole/resources/audio/moonlight.wav')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.5)

# 4 - keep looping through
running = 0
state = 0
acc = [0,0]

def to_deg(x):
    return x*57.29
class stop_watch:
    def __init__(self):
        self.init_time = pygame.time.get_ticks()
    def get(self):
        return pygame.time.get_ticks()-self.init_time
    def reset(self):
        self.init_time = pygame.time.get_ticks()
timer = stop_watch()
player_avatar = pygame.image.load("D:/Python/shooting mole/resources/images/dude.png")
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player,self).__init__()
        self.surf = player_avatar
        self.rect = self.surf.get_rect(center=(100,100))
        self.speed = 10
        self.angle = 0
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
        self.rect.top = max(self.rect.top,0)
        self.rect.bottom = min(self.rect.bottom, height)
        position = pygame.mouse.get_pos()
        playerpos = self.rect.center
        self.angle = math.atan2(position[1]-playerpos[1],position[0]-playerpos[0])
        self.surf = pygame.transform.rotate(player_avatar,360-to_deg(self.angle)) # change angle from rad to deg
arrow = pygame.image.load("D:/Python/shooting mole/resources/images/bullet.png")
class Arrow(pygame.sprite.Sprite):
    def __init__(self):
        super(Arrow,self).__init__()
        self.angle = p.angle
        self.surf = pygame.transform.rotate(arrow,360-to_deg(self.angle))
        self.rect = self.surf.get_rect(center=p.rect.center)
        self.speed = 15
    def update(self):
        x = math.cos(self.angle)*self.speed
        y = math.sin(self.angle)*self.speed
        self.rect.move_ip(x,y)
        if self.rect.top < 0 or self.rect.bottom > height or self.rect.left < 0 or self.rect.right > width:
            self.kill()
badguyimg = pygame.image.load("D:/Python/shooting mole/resources/images/badguy.png")
class Badguy(pygame.sprite.Sprite):
    def __init__(self):
        super(Badguy,self).__init__()
        self.surf = badguyimg
        self.rect = self.surf.get_rect()
        self.rect.left = width+100
        self.rect.top = random.randint(50,height-100)
        self.speed = random.randint(5,8)
    def update(self):
        self.rect.move_ip(-self.speed,0)
        if self.rect.right < 0:
            self.kill()
def background():
    screen.fill(0)
    for x in range(width//grass.get_width()+1):
        for y in range(height//grass.get_height()+1):
            screen.blit(grass,(x*100,y*100))
def draw_screen():
    background()
    castle_height = castle.get_height()
    for x in range((height-50)//castle_height):
        screen.blit(castle,(0,50+x*castle_height))    
def draw_hp():
    hp_rect = pygame.Rect(5,5,200,28)
    pygame.draw.rect(screen,black,hp_rect)
    percent = cur_hp/max_hp[diff]
    cur_hp_rect = pygame.Rect(5,5,200*percent,28)
    pygame.draw.rect(screen,green,cur_hp_rect)
    font = pygame.font.SysFont("comicsansms",23)
    hp_text = font.render(str(cur_hp),True,white)
    hp_rect = hp_text.get_rect(center=(30,19))
    screen.blit(hp_text,hp_rect)
def draw_info():
    font = pygame.font.SysFont("comicsansms",35)
    kill_text = font.render("Total mole: "+str(acc[1])+"/"+str(mole_tar[diff]),True,black)
    kill_rect = kill_text.get_rect(bottomleft=(0,height))
    if acc[0] != 0:     
        accuracy = acc[1]/acc[0]*100
    else:
        accuracy = 0
    screen.blit(kill_text,kill_rect)
    acc_text = font.render("Accuracy: "+str(round(accuracy,1))+"%",True,black)
    acc_rect = acc_text.get_rect(bottomleft=(325,height))
    screen.blit(acc_text,acc_rect)
    time_text = font.render("Time: "+str(timer.get()//1000)+"/"+str(time_tar[diff]),True,black)
    time_rect = time_text.get_rect(bottomleft=(650,height))
    screen.blit(time_text, time_rect)

    rb_height = 25
    rect = pygame.Rect(0,0,200,rb_height)
    rect.bottomright = (width-10,height-10)
    pygame.draw.rect(screen,black,rect)
    percent = 1-max(reload_until-timer.get(),0) / reload_time
    rect1 = pygame.Rect(0,0,percent*200,rb_height)
    rect1.bottomleft = rect.bottomleft
    pygame.draw.rect(screen,green,rect1)

max_hp = [200,180,1100,50,10]
cur_hp = max_hp[0]
badtimer = 500
add_enemy = pygame.USEREVENT + 1
pygame.time.set_timer(add_enemy, badtimer)

p = Player()
arrows = pygame.sprite.Group() 
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

reload_until = 0
reload_time = 350
total_diff = 5
diff = 0
mole_tar = [10,15,25,40,60]
time_tar = [20,25,310,38,46]
diff_text = ["Easy","Normal","Hard","Extreme","Impossible"]
diff_text_pos = [(1/4,1/2),(1/2,1/2),(3/4,1/2),(1/3,3/4),(2/3,3/4)]
diff_text_rect = [None]*total_diff
def draw_border(x,color,thickness):
    pygame.draw.line(screen,color,x.topleft,x.topright,thickness)
    pygame.draw.line(screen,color,x.bottomleft,x.bottomright,thickness)
    pygame.draw.line(screen,color,x.topleft,x.bottomleft,thickness)
    pygame.draw.line(screen,color,x.topright,x.bottomright,thickness)
def select_difficulty():
    global diff
    background()
    font = pygame.font.SysFont("Corbel",45)
    d_text = font.render("Select difficulty ",True,black)
    d_rect = d_text.get_rect(center=(width/2,height/2-100))
    screen.blit(d_text,d_rect)
    for i in range(total_diff):
        cur_text = font.render(diff_text[i],True,black)
        diff_text_rect[i] = cur_text.get_rect(center=(width*diff_text_pos[i][0],height*diff_text_pos[i][1]))
    pygame.display.flip()
    while 1:      
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i in range(total_diff):
                    if diff_text_rect[i].collidepoint(pygame.mouse.get_pos()):
                        diff = i
                        return
        for i in range(total_diff):
            if diff_text_rect[i].collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen,green,diff_text_rect[i])
            else:
                pygame.draw.rect(screen,white,diff_text_rect[i])
        for i in range(total_diff):
            cur_text = font.render(diff_text[i],True,black)
            screen.blit(cur_text,diff_text_rect[i])
            pygame.display.update(diff_text_rect[i])
def take_input():
    global reload_until, reload_time
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() 
            exit(0)
        if event.type == add_enemy:
            new_badguy = Badguy()
            enemies.add(new_badguy)
            all_sprites.add(new_badguy)      
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # left click
            if timer.get() < reload_until:
                continue
            reload_until = timer.get() + reload_time
            new_arrow = Arrow()
            arrows.add(new_arrow)  
            all_sprites.add(new_arrow)
            acc[0]+=1
            shoot.play()
        if event.type == pygame.KEYDOWN:    
            if event.key == K_ESCAPE:
                pygame.quit()
                exit(0)
def restart():
    global running, badtimer, p, acc, state, cur_hp, reload_until
    for i in all_sprites:
        i.kill()
    for i in arrows:
        i.kill()
    for i in enemies:
        i.kill()
    reload_until = 0
    running = 1
    p = Player()
    all_sprites.add(p)
    timer.reset()
    acc = [0,0]
    state = 0
    cur_hp = max_hp[diff]
def update():
    press = pygame.key.get_pressed()
    p.update(press)
    for i in enemies:
        i.update()
    for i in arrows:
        i.update()
    for i in all_sprites:
        screen.blit(i.surf,i.rect)
def collide():
    global cur_hp
    for i in enemies:
        if i.rect.left <= castle.get_rect().right:
            cur_hp -= 10
            i.kill()
            hit.play()
    for x in arrows:
        for y in enemies:
            if x.rect.colliderect(y.rect):
                x.kill()
                y.kill()
                acc[1]+=1
                enemy.play()
def check_condition():
    global running, state, cur_hp
    if timer.get()>=time_tar[diff]*1000 or acc[1]>=mole_tar[diff]:
        running=0
        state=1
    if cur_hp <= 0:
        running=0
        state=0
def end_screen():
    global acc
    if acc[0] != 0:     
        accuracy = acc[1]/acc[0]*100
    else:
        accuracy = 0
    score_font = pygame.font.SysFont("comicsansms", 35)
    if state==0:
        screen.blit(lose_screen,(0,0))
    else:
        screen.blit(win_screen,(0,0))
    kill_text = score_font.render("Total mole: "+str(acc[1]),True,black)
    screen.blit(kill_text,kill_text.get_rect(center=(width/2,height/2+15)))
    accu = score_font.render("Accuracy: "+str(round(accuracy,1))+"%",True,black)
    screen.blit(accu,accu.get_rect(center=(width/2,height/2+45)))
    res_text = score_font.render("Press R to restart",True,black)
    screen.blit(res_text,res_text.get_rect(center=(width/2,height/2+75)))
    wait = 1
    while wait:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == K_r:
                    wait = 0
        pygame.display.flip()
while 1:
    background()
    pygame.display.flip()
    select_difficulty()
    restart()
    while running:
        draw_screen()
        draw_hp()
        draw_info()
        take_input()
        update()
        collide()
        pygame.display.flip()
        check_condition()  
    end_screen()