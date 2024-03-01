#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 29 18:49:22 2024

@author: bingtinghuangfu
"""

import pygame as pg
from Objects import Heart

class Button:
    def __init__(self,ai_game,msg):
        self.screen=ai_game.screen
        self.screen_rect=self.screen.get_rect()
        self.width,self.height=200,50
        self.button_color=(0,255,0)
        self.text_color=(255,255,255)
        self.font=pg.font.SysFont(None, 48)
        self.msg=msg
        
        self.rect=pg.Rect(0, 0, self.width, self.height)
        self.rect.centerx=self.screen_rect.centerx
        self.rect.bottom=self.screen_rect.bottom - 200
        
        self._prep_msg()
        

    
    def _prep_msg(self):
        self.msg_image=self.font.render(self.msg, True, self.text_color,self.button_color)
        self.msg_image_rect=self.msg_image.get_rect()
        self.msg_image_rect.center=self.rect.center
        
    def _draw_button(self):
        self.screen.fill(self.button_color,self.rect)
        self.screen.blit(self.msg_image,self.msg_image_rect)


class Instruction:
    def __init__(self,ai_game,Heading,msg_left,msg_right):
        self.screen=ai_game.screen
        self.screen_rect=self.screen.get_rect()
        self.width,self.height=300,500
        self.button_color=(255 ,255 ,255)
        self.text_color=(51 ,0 ,0)
        self.font=pg.font.SysFont(None, 30)
        self.heading_font=pg.font.SysFont(None, 50)
        self.msg_left=msg_left
        self.msg_right=msg_right
        self.heading=Heading
        
        # 'Left Ctrl - Shoot\nSpace - Speed Up\nLeft/Right Key - Move'
        self.rect=pg.Rect(0, 0, self.width, self.height)
        self.rect.center=self.screen_rect.center
        self.rect.bottom=self.screen_rect.bottom - 300
        
        self._prep_msg()

    def _prep_msg(self):
        msg_list_left=self.msg_left.split('\n')
        msg_list_right=self.msg_right.split('\n')
        self.msg_image_list_left=[]
        self.msg_image_list_right=[]
        
        for i in msg_list_left:
            msg_image = self.font.render(i, True, self.text_color)
            self.msg_image_list_left.append(msg_image)
            
        for i in msg_list_right:
            msg_image = self.font.render(i, True, self.text_color)
            self.msg_image_list_right.append(msg_image)

        self.heading_image = self.heading_font.render(self.heading, True, (204,0,102))
    
        
    def _draw_button(self):
        self.screen.fill(self.button_color,self.rect)
        for i,x in zip(self.msg_image_list_left,range(len(self.msg_image_list_left))):
            msg_rect = i.get_rect()
            msg_rect.left = self.rect.left + 10
            msg_rect.top = self.rect.top + 150 + (x-1)*40
            self.screen.blit(i,msg_rect)
        
        for i,x in zip(self.msg_image_list_right,range(len(self.msg_image_list_right))):
            msg_rect = i.get_rect()
            msg_rect.right= self.rect.right - 10
            msg_rect.top = self.rect.top + 150 + (x-1)*40
            self.screen.blit(i,msg_rect)
        
        heading_image_rect=self.heading_image.get_rect()
        heading_image_rect.top = self.rect.top + 10
        heading_image_rect.left = self.rect.left + 10
        
        self.screen.blit(self.heading_image,heading_image_rect)


  
class ScroreBoard:
    '''A class to report scoring information'''
    def __init__(self,ai_game):
        '''Initialize scorekeeping attributes.'''
        self.ai_game=ai_game
        self.screen=ai_game.screen
        self.screen_rect=self.screen.get_rect()
        self.setting=ai_game.setting
        self.stats=ai_game.stats
        
        self.text_color=(30,30,30)
        self.font=pg.font.SysFont(None, 36)
        self._prep_score()
        self._prep_high_score()
        self._prep_heart()
        
    def _prep_high_score(self):
        high_score_str=str(self.stats.high_score)
        self.high_score_image=self.font.render(f'Highest Score: {high_score_str}', True, self.text_color,self.setting.bg_color)
        self.high_score_rect=self.high_score_image.get_rect()
        self.high_score_rect.centerx=self.screen_rect.centerx
        self.high_score_rect.top=10

        
    def _prep_score(self):
        '''“Turn the score into a rendered image'''
        score_str=str(self.stats.score)
        self.score_image=self.font.render(f'Score: {score_str}', True, self.text_color,self.setting.bg_color)
        self.score_rect=self.score_image.get_rect()
        self.score_rect.right=self.screen_rect.right-5
        self.score_rect.top=20
    
    
    def _prep_heart(self):
        self.hearts=pg.sprite.Group()
        for heart_number in range(self.stats.ships_left+1):
            heart=Heart(self.ai_game)
            heart.rect.x=self.screen_rect.width-(40+heart_number*heart.rect.width+(heart_number-1)*3)
            heart.rect.y=90
            self.hearts.add(heart)
    
    
    
    def _show_score(self):
        self.screen.blit(self.score_image,self.score_rect)
        self.screen.blit(self.high_score_image,self.high_score_rect)
        self.hearts.draw(self.screen)
       
        
    def _check_high_score(self):
        if self.stats.score>self.stats.high_score:
            self.stats.high_score=self.stats.score
            self._prep_high_score()


class Point:
    def __init__(self,ai_game):
        self.screen=ai_game.screen
        self.screen_rect=self.screen.get_rect()
        self.ai_game=ai_game
        self.stats=ai_game.stats
        self.setting=ai_game.setting
        
        self.text_color_add=(0,204,0)
        self.text_color_deduct=(255,0,0)
        
        self.font=pg.font.SysFont(None, 24)
        self._prep_point()
        self._prep_arrow()
        
    def _prep_arrow(self):
        self.arrow_image=pg.transform.scale(pg.image.load(self.setting.arrow_image), (20,20))
        self.arrow_rect=self.arrow_image.get_rect()
        self.arrow_rect.right=self.screen_rect.right-60
        self.arrow_rect.top = 55


    def _prep_point(self):
        '''Turn the point into a rendered image'''
        point_str=str(self.stats.point)
        if self.stats.point>0:
            self.point_image=self.font.render(f'+{point_str}', True, self.text_color_add,self.setting.bg_color)
        else:
            self.point_image=self.font.render(f'{point_str}', True, self.text_color_deduct,self.setting.bg_color)
        self.point_rect=self.point_image.get_rect()
        self.point_rect.x=self.stats.collision_x
        self.point_rect.y=self.stats.collision_y

    def _show_point(self):
        if self.stats.point != 0 and pg.time.get_ticks() < self.ai_game.time_show:
            self.screen.blit(self.point_image,self.point_rect)

    def _show_arrow(self):
        if not self.stats.if_level_up and self.stats.game_active and pg.time.get_ticks() < self.ai_game.time_show_level:
            self.screen.blit(self.arrow_image, self.arrow_rect)
        
        
    def _update_arrow(self):
        self.arrow_rect.y -= 0.3


class Level:
    def __init__(self,ai_game):
        self.screen=ai_game.screen
        self.screen_rect=self.screen.get_rect()
        self.setting=ai_game.setting
        self.stats=ai_game.stats
        
        self.text_color=(255,0,127)
        self.font=pg.font.SysFont(None, 24)
        self._prep_level()
        
    def _prep_level(self):
        '''“Turn the score into a rendered image'''
        level_str=str(self.setting.level+1)
        self.level_image=self.font.render(f'Level {level_str}', True, self.text_color,self.setting.bg_color)
        self.level_rect=self.level_image.get_rect()
        self.level_rect.right=self.screen_rect.right-5
        self.level_rect.top=60


        
    def _show_level(self):
        self.screen.blit(self.level_image,self.level_rect)
        

class SoundSign:
    def __init__(self,ai_game):
        self.screen=ai_game.screen
        self.screen_rect=self.screen.get_rect()
        self.setting=ai_game.setting
        self.stats=ai_game.stats
        self.rect=pg.Rect(15, 15, 40, 40)

        self._prep_sign()
    
    def _prep_sign(self):
        self.sound_sign=pg.transform.scale(pg.image.load(self.setting.sound_image), (self.rect.width,self.rect.width))
        self.mute_sign=pg.transform.scale(pg.image.load(self.setting.mute_image), (self.rect.width,self.rect.width))
        self.sound_rect=self.rect
        self.mute_rect=self.rect
    
    def _show_sign(self):
        if self.stats.sound_play:
            self.screen.blit(self.sound_sign,self.sound_rect)
        else:
            self.screen.blit(self.mute_sign,self.mute_rect)
    
        
        