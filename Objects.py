#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 29 18:47:17 2024

@author: bingtinghuangfu
"""

import pygame as pg
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self,ai_game):
        super().__init__()
        
        self.setting=ai_game.setting
        
        self.screen=ai_game.screen
        self.screen_rect=ai_game.screen.get_rect()
        
        self.image=pg.transform.scale(pg.image.load(self.setting.ship_image), (self.setting.ship_width,self.setting.ship_height))
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom
        self.moving_right=False
        self.moving_left=False
        self.speed=1
        self.screen_width=ai_game.screen_width

    def screen_change(self,ai_game):
        # print(ai_game.screen_change)
        # if ai_game.screen_change:
        self.screen_width=ai_game.screen_width
        self.screen=ai_game.screen
        self.screen_rect=ai_game.screen.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom
        
    def center_ship(self):
        self.rect.midbottom=self.screen_rect.midbottom
        self.x=float(self.rect.x)
        
        
    def blitme(self):
        self.screen.blit(self.image, self.rect)
    
    
    def update(self):
        if (self.moving_right)&(self.rect.right<self.screen_rect.right):
            self.rect.x+=1*self.speed
        if (self.moving_left)&(self.rect.left>0):
            self.rect.x-=1*self.speed


class Bullet(Sprite):
    def __init__(self,ai_game):
        super().__init__()
        self.setting=ai_game.setting
        self.screen=ai_game.screen
        self.color=self.setting.bullet_color
        self.rect = pg.Rect(0, 0, 8,15)
        self.rect.midtop=ai_game.ship.rect.midtop
        self.y = float(self.rect.y)

    def update(self):
        self.y-=self.setting.bullet_speed
        self.rect.y=self.y
    
    def draw_bullet(self):
        pg.draw.rect(self.screen, ((60,60,60)), self.rect)
        
        
class Boss(Sprite):
    
    def __init__(self, ai_game):
        super().__init__()
        self.screen=ai_game.screen
        self.setting=ai_game.setting
        self.screen_rect=ai_game.screen.get_rect()
        self.image=pg.transform.scale(pg.image.load(self.setting.Boss_image),(self.setting.boss_width,self.setting.boss_width))
        self.rect=self.image.get_rect()
        self.rect.x=self.rect.width
        self.rect.y = 40
        self.x = float(self.rect.x)
        self.boss_direction=0
        
    def update(self):
        if (self.boss_direction==0) & (self.rect.right<self.screen_rect.right):
            self.x+=0.2
            self.rect.x=self.x
        elif (self.boss_direction==0) & (self.rect.right>=self.screen_rect.right):
            self.boss_direction=1
    
        if (self.boss_direction==1) & (self.rect.left>0):
            self.x-=0.2
            self.rect.x=self.x
        elif (self.boss_direction==1) & (self.rect.left<=0):
            self.boss_direction=0


class Alien(Sprite):
    
    def __init__(self, ai_game):
        super().__init__()
        self.setting=ai_game.setting
        self.screen=ai_game.screen
        self.screen_rect=ai_game.screen.get_rect()
        self.image=pg.transform.scale(pg.image.load(self.setting.alien_image_1),
                                      (self.setting.alien_width,self.setting.alien_width))
        self.rect=self.image.get_rect()
        self.rect.x=self.rect.width
        self.rect.y=self.rect.height
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.rect.midtop=ai_game.boss.sprites()[0].rect.midbottom
        
               
    def update(self):
        self.y += self.setting.alien_speed
        self.rect.y=self.y

    
    def draw_alien(self,ai_game):
        self.screen.blit(self.image, self.rect)




class Alien_2(Alien):
    def __init__(self,ai_game):
        super().__init__(ai_game)
        self.image=pg.transform.scale(pg.image.load(self.setting.alien_image_2), 
                                      (self.setting.alien_width,self.setting.alien_width))
        self.rect=self.image.get_rect()
        self.rect.x=self.rect.width
        self.rect.y=self.rect.height
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.rect.midtop=ai_game.boss.sprites()[0].rect.midbottom

    def update(self):
        self.y += self.setting.alien_speed_2
        self.rect.y=self.y


class Heart(Sprite):
    def __init__(self,ai_game):
        super().__init__()
        self.setting=ai_game.setting
        self.image=pg.transform.scale(pg.image.load(self.setting.heart_image), (self.setting.heart_width,self.setting.heart_width))
        self.rect = self.image.get_rect()


