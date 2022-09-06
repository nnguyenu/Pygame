import pygame
import time
import random

from pygame.locals import *

from os import path
def getFile(fileName):
    #Returns the absolute path of a file.
    return path.join(path.dirname(__file__), fileName)

pygame.init()
pygame.mixer.init()

width, height = 1218, 630
blue = (50, 153, 213)
red = (255,0,0)
white = (255,255,255)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Escape Labyrinth')

walkRight = [pygame.image.load(getFile('Resources/R1.png')), pygame.image.load(getFile('Resources/R2.png')), pygame.image.load(getFile('Resources/R3.png')), pygame.image.load(getFile('Resources/R4.png')), pygame.image.load(getFile('Resources/R5.png')), pygame.image.load(getFile('Resources/R6.png')), pygame.image.load(getFile('Resources/R7.png')), pygame.image.load(getFile('Resources/R8.png')), pygame.image.load(getFile('Resources/R9.png'))]
walkLeft = [pygame.image.load(getFile('Resources/L1.png')), pygame.image.load(getFile('Resources/L2.png')), pygame.image.load(getFile('Resources/L3.png')), pygame.image.load(getFile('Resources/L4.png')), pygame.image.load(getFile('Resources/L5.png')), pygame.image.load(getFile('Resources/L6.png')), pygame.image.load(getFile('Resources/L7.png')), pygame.image.load(getFile('Resources/L8.png')), pygame.image.load(getFile('Resources/L9.png'))]
bg = pygame.image.load(getFile('Resources/bg.jpg'))
bg = pygame.transform.scale(bg,(width,height))
char = pygame.image.load(getFile('Resources/standing.png'))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player,self).__init__()
        self.rect = pygame.Surface((64,64)).get_rect(bottomleft=(0,height))
        self.speed = 7
        self.jump = False
        self.jump_frame = 10
        self.left = False
        self.right = False
        self.step = 0
    def update(self,press):
        if press[K_LEFT] or press[K_a]:
            self.rect.move_ip(-self.speed, 0)
            self.left = True
            self.right = False
        if press[K_RIGHT] or press[K_d]:
            self.rect.move_ip(self.speed, 0)
            self.left = False
            self.right = True
        if not self.jump:
            if press[K_UP] or press[K_w]:
                self.jump = True
                self.left = False
                self.right = False
                self.step = 0
        else:
            if self.jump_frame >= -10:
                direct = 1 if self.jump_frame < 0 else -1
                self.rect.move_ip(0,(self.jump_frame**2)*0.3*direct)
                self.jump_frame -= 1
            else:
                self.jump = False
                self.jump_frame = 10   
        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, width)
        self.rect.top = max(self.rect.top,0)
        self.rect.bottom = min(self.rect.bottom, height)    
    def display(self):
        self.step %= 27
        if self.left:
            screen.blit(walkLeft[self.step//3],(self.rect))
            self.step += 1
        elif self.right:
            screen.blit(walkRight[self.step//3],(self.rect))
            self.step += 1
        else:
            screen.blit(char,(self.rect))

player = Player()

def typing():
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            exit(0) 
        if event.type==pygame.KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                exit(0)
    press = pygame.key.get_pressed()
    player.update(press)
def draw():
    screen.blit(bg,(0,0))
    player.display()
    pygame.display.update() # same as pygame.display.flip()

clock = pygame.time.Clock()
running = 1
while running:
    clock.tick(27)
    typing()
    draw()
    
