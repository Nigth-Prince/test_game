import random
from typing import Any
import pygame as pg
from sql_bd import DateBaseSQL


pg.init()
SQL = DateBaseSQL() # новое
win = pg.display.set_mode((600,600))
FONT_SIZE = 18
font_name = pg.font.match_font('arial')
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GREY = (50,50,50)
WIDTH, HEIGHT = 600,600
dog_surf = pg.image.load('C:/Users/pr1nce/Desktop/Game_MGTU-main/foto.jpeg')
dog_rect = dog_surf.get_rect(bottomright=(600, 300))
class Apple(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load('apple.png')
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0,570)
        self.rect.y = random.randrange(0,570)

    # def update(self):

class Player(pg.sprite.Sprite):
    def __init__(self,x,y):
        pg.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.speed_x = 1
        self.speed_y = 0
        self.image = pg.image.load('C:/Users/pr1nce/Desktop/Game_MGTU-main/hero.png')
        self.rect = self.image.get_rect()
        self.rect. centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 100
    def update(self):
        # for i in range(4): # новое для змейки
            # win.blit(self.image,(self.rect.x-100*i,self.rect.y)) # новое для змейки
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        key = pg.key.get_pressed()
        if key[pg.K_LEFT]:
            if self.speed_x != 1:
                self.speed_x = -1
                self.speed_y = 0
        elif key[pg.K_RIGHT]:
            if self.speed_x != -1:
                self.speed_x = 1
                self.speed_y = 0 
        elif key[pg.K_UP]:
            if self.speed_y != 1:
                self.speed_x = 0
                self.speed_y = -1
        elif key[pg.K_DOWN]:
            if self.speed_y != -1:
                self.speed_x = 0
                self.speed_y = 1
        
        

def draw_text(surf, text, x, y, size=FONT_SIZE, color=WHITE): # выведение
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color) 
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect) 

def user_name(surf, text, x, y, size=FONT_SIZE): 
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect() 
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)



all_sprites = pg.sprite.Group()
player = Player(300,300)
all_sprites.add(player)
apple = Apple()
all_sprites.add(apple)
name = ''
start_game = True
# полностью новый метод
def see_db(name):
    score = random.randrange(500)
    SQL.set(name=name, score=score)
    
    while 1:
        for i in pg.event.get():
            if i.type == pg.QUIT:
                exit()
        win.fill((0,0,0))
        offset = 150
        step = 0
        for u_name, u_score in SQL.get():
            step += 1
            draw_text(win,('='*26), WIDTH // 2, HEIGHT - offset-90*step)    
            draw_text(win, (f'{u_name}                        {u_score}'), WIDTH // 2-10, HEIGHT - 150 - offset*2)
            offset -= 30
        step = 0
        while step < 15:
            step+=1
            draw_text(win,('|'+ ' ' * 28 + '|' + ' ' * 28 + '|'), WIDTH // 2, HEIGHT - 170 - offset- 20*step)
        draw_text(win,('='*26), WIDTH // 2, HEIGHT - 180)
        pg.display.update()

while start_game:
    for i in pg.event.get():
        if i.type == pg.QUIT:
            exit()
        elif i.type == pg.KEYDOWN:
            if i.key in {pg.K_ESCAPE, pg.K_RETURN}:
                start_game = False
                # see_db(name)
            elif i.key == pg.K_BACKSPACE:
                name = name[:-1]
            else:
                name += i.unicode
        win.fill((0,0,0))
        win.blit(dog_surf,dog_rect)
        draw_text(win, 'Введите имя:', WIDTH // 2, HEIGHT // 2) 
        draw_text(win, name, WIDTH // 2 , HEIGHT // 2 + 20)
        pg.display.update()
score = 0
while 1:
    for i in pg.event.get():
        if i.type == pg.QUIT:
            exit()
    
    win.fill((255,255,255))
    draw_text(win, name, 15 , 15, color=(0,0,0))
    draw_text(win, f'Score:{score}', WIDTH // 2 , 15,color=(0,0,0))
    all_sprites.update()
    all_sprites.draw(win)
    pg.display.update()
    pg.time.Clock().tick(40)