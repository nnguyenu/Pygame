import pygame
import time
import random
from pygame.locals import *
from collections import deque

pygame.init()
pygame.mixer.init()

white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
 
width, height = 1218, 630
 
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Xenia')
background = pygame.image.load("D:/Python/Snake Xenia/Resources/image/grass.jpg")
snake = pygame.image.load("D:/Python/Snake Xenia/Resources/image/Snake sprite sheet.png")
pygame.mixer.music.load("D:/Python/Snake Xenia/Resources/audio/Snake Hissing - Sound Effect-[AudioTrimmer.com].mp3")
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.17)
eat = pygame.mixer.Sound("D:/Python/Snake Xenia/Resources/audio/EatSound_CC0_by_EugeneLoza.ogg")
eat.set_volume(0.5)

s_w = snake.get_width()
s_h = snake.get_height()
block = 42
# 0-2: diff types of snake_head
# 3: snake body, 4: snake tail, 5: snake turn
snake_turn = [] 
snake_parts = []
for i in range(3):
    snake_parts.append(snake.subsurface((0,s_h/3*i,s_w/3,s_h/3)))
snake_parts.append(snake.subsurface((s_w/3*2,s_h/3*2,s_w/3,s_h/3)))
snake_parts.append(snake.subsurface((s_w/3,s_h/3*2,s_w/3,s_h/3)))

snake_turn.append(snake.subsurface((s_w/3,s_h/3,s_w/3,s_h/3)))
snake_turn.append(snake.subsurface((s_w/3*2,s_h/3,s_w/3,s_h/3)))
snake_turn.append(snake.subsurface((s_w/3*2,0,s_w/3,s_h/3)))
snake_turn.append(snake.subsurface((s_w/3,0,s_w/3,s_h/3)))

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)
 
# direction ?
# 0 : down, 1 : right, 2: up, 3: left
def rotate(image,angle):
    rimage = pygame.transform.rotate(image,angle)
    return rimage
def turn_img(x,y):
    if (x+1)%4 == y:
        return snake_turn[x]
    else:
        return snake_turn[(x+1)%4]

running = 1

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player,self).__init__()
        self.snake = deque([(0,0,0)])
        self.speed = block
        self.len = 1  
    def update(self,press):
        global running, high_score
        head = self.snake[-1]
        if head[2] != 0 and (press[K_UP] or press[K_w]):
            head = (head[0],head[1]-self.speed,2) 
        elif head[2] != 2 and (press[K_DOWN] or press[K_s]):
            head = (head[0],head[1]+self.speed,0)   
        elif head[2] != 1 and (press[K_LEFT] or press[K_a]):
            head = (head[0]-self.speed,head[1],3)
        elif head[2] != 3 and (press[K_RIGHT] or press[K_d]):
            head = (head[0]+self.speed,head[1],1)   
        if head[0] < 0 or head[0] >= width or head[1] < 0 or head[1] >= height:
            high_score=max(high_score,len(player.snake))
            self.kill()
            running = 0
        if head == self.snake[-1]:
            return
        self.snake.append(head)
        if len(self.snake) > self.len:
            self.snake.popleft()
    def grow(self):
        self.len += 1
    def display(self,type):
        for i in range(len(self.snake)-1,-1,-1):
            topleft = (self.snake[i][0],self.snake[i][1])
            direction = self.snake[i][2]
            if i == len(self.snake)-1:
                img = rotate(snake_parts[type%3],direction*90)  
            elif i == 0:
                direction = self.snake[i+1][2]
                img = rotate(snake_parts[4],direction*90+180)  
            else:
                if self.snake[i+1][2] != direction:
                    img = turn_img(direction,self.snake[i+1][2])   
                else:
                    img = rotate(snake_parts[3],direction*90)
            screen.blit(img,topleft)

class Egg(pygame.sprite.Sprite):
    def __init__(self):
        super(Egg,self).__init__()
        self.surf = pygame.image.load("D:/Python/Snake Xenia/Resources/image/egg.png")
        self.surf.set_colorkey((white),RLEACCEL)
        ok = 1
        while ok:
            ok = 0
            randx = (random.randint(0,width)//block)*block
            randy = (random.randint(0,height)//block)*block
            w = self.surf.get_width()
            h = self.surf.get_height()
            if randx + w > width or randy + h > height:
                ok = 1
        self.rect = self.surf.get_rect(topleft=(randx,randy))

high_score = 0
def end_screen():
    global high_score, running
    print(high_score)
    font_style = pygame.font.SysFont("bahnschrift", 40)
    replay_text = font_style.render("Type R to replay",True,yellow)
    screen.blit(replay_text,replay_text.get_rect(center=(width/2,height/2)))
    hs_text = font_style.render("Highscore: "+str(high_score),True,yellow)
    screen.blit(hs_text,hs_text.get_rect(center=(width/2,height/2+50)))
    wait = 1
    while wait:
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
    
player = Player()

def draw_info(t):
    ct = score_font.render("Time: "+str(t//1000),True,white)
    screen.blit(ct,ct.get_rect(topright=(width,0)))
    global player
    cp = score_font.render("Score: "+str(len(player.snake)),True,white)
    screen.blit(cp,cp.get_rect(topright=(width,50)))
def take_input():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                exit(0)
    press = pygame.key.get_pressed()
    player.update(press)
clock = pygame.time.Clock()
def draw_background():
    bg_width = background.get_width()
    bg_height = background.get_height()
    for x in range(width//bg_width+1):
        for y in range(height//bg_height+1):
            screen.blit(background,(x*bg_width,y*bg_height))
def collider():
    global egg, running, high_score, player
    snake_head = player.snake[-1]
    head_rect = pygame.Rect(snake_head[0],snake_head[1],snake_parts[0].get_width(),snake_parts[0].get_height())
    if head_rect.colliderect(egg):
        egg.kill()
        egg = Egg()
        player.grow()
        eat.play()
    for i in range(len(player.snake)-1):
        curx = player.snake[i][0]
        cury = player.snake[i][1]
        body_rect = pygame.Rect(curx,cury,snake_parts[0].get_width(),snake_parts[0].get_height())
        if head_rect.colliderect(body_rect):
            high_score=max(high_score,len(player.snake))
            player.kill()
            running = 0
while 1:
    egg = Egg()
    player = Player()
    begin_time = pygame.time.get_ticks()
    while running:
        current = pygame.time.get_ticks()
        draw_background()
        screen.blit(egg.surf,egg.rect)
        draw_info(current-begin_time)
        take_input()
        collider()
        player.display(current)
        pygame.display.flip()
        clock.tick(10)
    end_screen()