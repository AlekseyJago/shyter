from pygame import *
from random import randint
from time import time as timer

mixer.init()
font.init()
window=display.set_mode((0, 0), FULLSCREEN)
background=transform.scale(image.load('galaxy.jpg'), (1760,980))
fontt=font.SysFont('Arial', 40)
font1=font.SysFont('Arial', 210)
winer=font1.render("YOU WIN", True, (0,255,0))
loser=font1.render("YOU LOSE", True, (255,0,0))
display.set_caption('Maze')
mixer.music.load('space.ogg')
#mixer.music.play(-1)
fireogg=mixer.Sound('vyistrel.ogg')

class  GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image=transform.scale(image.load(player_image), (size_x, size_y))
        self.speed=player_speed
        self.rect=self.image.get_rect()
        self.rect.x=player_x
        self.rect.y=player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Bullet(GameSprite):
    def update(self):
        self.rect.y -=self.speed
        if self.rect.y<=-30:
            self.kill()
    

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x>215:
            self.rect.x -=self.speed
        if keys[K_d] and self.rect.x<1615:
            self.rect.x +=self.speed
    def fire(self):
        bullet=Bullet('bullet.png', self.rect.centerx-8, self.rect.top,18,36,15)
        bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y +=self.speed
        if self.rect.y>=980:
            self.rect.y=-100
            self.rect.x=randint(310,1610)
            lost+=1
class Asteroid(GameSprite):
    def update(self):
        
        self.rect.y+=self.speed
        if self.rect.y>=980:
            self.rect.y=-100
            self.rect.x=randint(310,1610)
            
#bullet=Bullet('bullet.png', 800, 800,20,40,8)
iam=Player('rocket.png',900,855,80,110,9)
monsters=sprite.Group()
asteroids=sprite.Group()
bullets=sprite.Group()
for i in range(5):
    monster= Enemy('ufo.png',randint(310,1610), -50,100,65,randint(1,5))
    monsters.add(monster)
for i in range(3):
    asteroid= Asteroid('asteroid.png',randint(310,1610), -50,100,80,randint(15,25))
    asteroids.add(asteroid)
lost=0
score=0
finish=False
num_fire=0
num_bullets=6
rel_time=False
while True:
    for e in event.get():
        if e.type == QUIT:
            exit()
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                exit()
        if e.type==MOUSEBUTTONDOWN and e.button==1:

            if num_fire<6:
                num_fire+=1
                num_bullets-=1
                iam.fire()
                fireogg.play()
            if num_fire>=6 and rel_time==False:
                last_time=timer()
                rel_time=True
            
    if not finish:
        window.blit(background, (0,0))
        text=fontt.render("Пропущено: "+str(lost), True,(250,250,250))
        window.blit(text, (200,140))
        text_lose=fontt.render("Счёт: "+str(score), True,(250,250,250))
        window.blit(text_lose,(200,105))
        fire_num=fontt.render("Осталось выстрелов: "+str(num_bullets), True,(250,250,250))
        window.blit(fire_num,(200,180))
        if rel_time==True:
                now_time=timer()
                if now_time-last_time<3:
                    reload=fontt.render('Wait, reload...',True,(170,0,0))
                    window.blit(reload, (840,900))
                else:
                    num_fire=0
                    num_bullets=6
                    rel_time=False
        
        iam.reset()
        iam.update()
        bullets.update()
        bullets.draw(window)
        monsters.draw(window)
        monsters.update()
        asteroids.draw(window)
        asteroids.update()
        sprite_list=sprite.groupcollide(monsters, bullets, True, True)
        
        for c in sprite_list:
            score+=1
            monster= Enemy('ufo.png',randint(310,1610), -50,100,65,randint(1,5))
            monsters.add(monster)
        if sprite.spritecollide(iam, asteroids, False) or lost>3:
            finish=True
            window.blit(loser, (545,410))
        if score>9:
            finish=True
            window.blit(winer, (545,410))
    else:
        finish=False
        lost=0
        score=0
        num_fire=0
        num_bullets=6
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()
        time.delay(3000)
        for i in range(5):
            monster= Enemy('ufo.png',randint(310,1610), -50,100,65,randint(1,5))
            monsters.add(monster)
        for i in range(3):
            asteroid= Asteroid('asteroid.png',randint(310,1610), -50,100,80,randint(15,25))
            asteroids.add(asteroid)
        
    display.update()
    time.delay(5)
