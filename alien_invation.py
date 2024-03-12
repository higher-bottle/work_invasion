#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 29 19:03:54 2024

@author: bingtinghuangfu
"""

import pygame as pg
import os
from time import sleep
from Setting import Setting
from GameStats import GameStats
from Music import Music
from Objects import Ship,Bullet,Alien,Alien_2,Boss
from NumberShow import Button,Point,ScroreBoard,Level,SoundSign,Instruction


class AlienInvasion:
    
    def __init__(self):
        pg.init()
        self.setting=Setting()
        self.stats=GameStats(self)
        self.music=Music(self)
        
        
        self.screen=pg.display.set_mode(self.setting.screen_size,pg.RESIZABLE)
        self.screen_width=self.screen.get_width()
        self.screen_change=False
        pg.display.set_caption("Alien Invation")
        self.ship=Ship(self)
        self.bullet=pg.sprite.Group()#新建一个空“子弹”精灵组
        self.boss=pg.sprite.Group()
        
        self._create_boss()
        
        self.aliens=pg.sprite.Group()
        self.aliens_2=pg.sprite.Group()
        
        self.last_drop_time = pg.time.get_ticks()
        self.last_drop_time_2 = pg.time.get_ticks()

        
        self.play_button=Button(self, "Start")
        self.sound_button=SoundSign(self)
        self.instruction=Instruction(self,'Instruction','Left Ctrl\nSpace\nLeft/Right Key\nQ\nShoot a Table Work\nShoot a Slide Work\nMiss a Table Work\nMiss a Slide Work\nBeated',
                                     'Shoot\nSpeed Up\nMove\nQuit\n+10\n+20\n-20\n-10\nLose a Heart')
        # self.instruction=Instruction(self,'Shoot\nSpeed Up\nMove')
        
        self.scoreboard=ScroreBoard(self)
        self.pointboard=Point(self)
        self.level=Level(self)
    
    
    def _ship_hit(self):
        '''check if the ship has beated 3 times'''
        # print(self.stats.ships_left)
        if self.stats.ships_left > 0:
            self.stats.ships_left-=1
            
            self.scoreboard._prep_heart()
            self.aliens.empty()
            self.aliens_2.empty()
            self.bullet.empty()
            
            sleep(0.5)
        else:
            self.setting.level=0
            self.stats.game_active=False
            pg.mouse.set_visible(True)


    def _check_aliens_bottom(self):
        screen_rect=self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom>=screen_rect.bottom:
                self.music._music_wrong()
                if self.stats.collisions_count > -5:
                    self.stats.collisions_count -= 2
                    self.stats.point = -20
                    self.stats.collision_x = alien.rect.x
                    self.stats.collision_y = screen_rect.height - 40
                    self.time_show = pg.time.get_ticks() + 500
                    self.aliens.empty()
                    self.bullet.empty()
                    self._update_score()
                    self.pointboard._prep_point()
                    self.scoreboard._prep_score()
                    self.scoreboard._check_high_score()
                    self.scoreboard._prep_high_score()
                    
                else:
                    self.setting.level = 0
                    self.stats.game_active = False
                    pg.mouse.set_visible(True)
            
        for alien in self.aliens_2.sprites():
            
            if alien.rect.bottom>=screen_rect.bottom:
                self.music._music_wrong()
                if self.stats.collisions_count > -5:
                    self.stats.collisions_count-=1
                    self.stats.point = -10
                    
                    self.stats.collision_x = alien.rect.x
                    self.stats.collision_y = screen_rect.height - 40
                    self.time_show = pg.time.get_ticks() + 500
                    self.aliens_2.empty()
                    self.bullet.empty()
                    self._update_score()
                    self.pointboard._prep_point()
                    self.scoreboard._prep_score()
                    self.scoreboard._check_high_score()
                    self.scoreboard._prep_high_score()
                else:
                    self.setting.level=0
                    self.stats.game_active=False
                    pg.mouse.set_visible(True)

        

    
        
    def _fire_bullet(self):
        if len(self.bullet)<self.setting.bullet_allowed:
            new_bullet=Bullet(self)#新建一个“子弹”元素
            self.bullet.add(new_bullet)#把新建的元素加入精灵组
            
    def _add_alien(self):
        if self.stats.alien_count<self.setting.alien_num:
            new_alien=Alien(self)
            self.aliens.add(new_alien)
            self.stats.alien_count+=1
            
    def _add_alien_2(self):
        if self.stats.alien_count_2<self.setting.alien_num_2:
            new_alien_2=Alien_2(self)
            self.aliens_2.add(new_alien_2)
            self.stats.alien_count_2+=1

    
    
    def _create_boss(self):
        new_boss=Boss(self)
        self.boss.add(new_boss)
        
    
    
    def _check_test_keydown(self,event):
        if event.key==pg.K_RIGHT:   
            self.ship.moving_right=True
        elif event.key==pg.K_LEFT:
            self.ship.moving_left=True
        elif event.key==pg.K_SPACE:
            self.ship.speed=2
        elif event.key==pg.K_q:
            pg.quit()
            os._exit(0)
        elif event.key==pg.K_LCTRL:
            self._fire_bullet()
        # elif event.key==pg.K_a:
        #     self._drop_alien()
     
        
    def _check_test_keyup(self,event):
        if event.key==pg.K_RIGHT:
            self.ship.moving_right=False
        elif event.key==pg.K_LEFT:
            self.ship.moving_left=False
        elif event.key==pg.K_SPACE:
            self.ship.speed=1
    
    def _check_sound_button(self,mouse_pos):
        self.mouse_pos=mouse_pos
        sound_button_click=self.sound_button.rect.collidepoint(self.mouse_pos)
        if sound_button_click:
            if self.stats.sound_play:
                self.stats.sound_play = False
                pg.mixer.music.pause()
                # self.stats.sound_play_sign = False
            elif not self.stats.sound_play:
                self.stats.sound_play = True
                pg.mixer.music.unpause()
                # self.stats.sound_play_sign = True
            self.sound_button._prep_sign()
    
    
    def  _check_play_button(self,mouse_pos):
        self.mouse_pos=mouse_pos
        button_click=self.play_button.rect.collidepoint(self.mouse_pos)
        if (button_click) and (not self.stats.game_active):
            self.stats.reset_status()
            self.stats.if_level_up=True
            
            self.setting.initialize_dynamic_settings()
            self.stats.game_active=True
            self.scoreboard._prep_score()
            self.level._prep_level()
            self.scoreboard._prep_heart()
            pg.mouse.set_visible(False)
            self.aliens.empty()
            self.bullet.empty()
            self.ship.center_ship()
            self._drop_alien()
            self._drop_alien_2()
    
    def _check_test(self):
        self.screen_change=False
        for event in pg.event.get():
            if event.type==pg.QUIT:
                pg.quit()
                os._exit(0)
            elif event.type==pg.KEYDOWN:#按下
                self._check_test_keydown(event)
            elif event.type==pg.KEYUP:
                self._check_test_keyup(event)
            elif event.type==pg.VIDEORESIZE:
                self.screen=pg.display.set_mode((event.w, event.h), pg.RESIZABLE)
                self.screen_width=event.w
                self.screen_change=True
            elif event.type==pg.MOUSEBUTTONDOWN:
                mouse_pos=pg.mouse.get_pos()
                self._check_play_button(mouse_pos)
                self._check_sound_button(mouse_pos)
            
   
    def _drop_alien(self):
        if self.stats.game_active:
            current_time = pg.time.get_ticks()
            if current_time - self.last_drop_time >= self.setting.alien_interval:
                self._add_alien()
                self.last_drop_time = current_time

    def _drop_alien_2(self):
        '''drop the powerpoint alien when level 3'''
        if self.stats.game_active and self.setting.level > 1:
             current_time_2 = pg.time.get_ticks()
             if current_time_2 - self.last_drop_time_2 >= self.setting.alien_interval_2:
                 self._add_alien_2()
                 self.last_drop_time_2 = current_time_2



    def _update_screen(self):
        self.screen.fill((230,230,230))
        self.ship.blitme()
        self.scoreboard._show_score()
        self.level._show_level()
        self.pointboard._show_point()
        self.pointboard._show_arrow()
        
        for bullet in self.bullet.sprites():
            bullet.draw_bullet()
            
        self.boss.draw(self.screen)#Draws all of the member sprites onto the given surface.
        
        
        for alien in self.aliens.sprites():
            alien.draw_alien(self)
        self._drop_alien()
            
        for alien in self.aliens_2.sprites():
            alien.draw_alien(self)
        self._drop_alien_2()
        

        if not self.stats.game_active:
            self.play_button._draw_button()
            self.instruction._draw_button()
        
        self.sound_button._show_sign()
        
        pg.display.flip()
    
    
    def _update_bullet(self):
            
        '''delete the bullets which have disapeared'''
        for bullet in self.bullet.copy():
            if bullet.rect.bottom<=0:
                self.bullet.remove(bullet)
                
    
        
    def _check_bullet_alien_collisions(self):
        
        collisions=pg.sprite.groupcollide(self.bullet, self.aliens, 1, 1)
        
        
        collisions_2=pg.sprite.groupcollide(self.bullet, self.aliens_2, 1, 1)
        
        if collisions:
            for collision in collisions:
                self.stats.collision_x=collision.rect.x
                self.stats.collision_y=collision.rect.y
            self.stats.collisions_count += 1
            self.stats.point = 10
            self.time_show = pg.time.get_ticks() + 500
            self.music._music_money()
            self.pointboard._prep_point()
            self._update_score()
            self.scoreboard._prep_score()
            self.scoreboard._check_high_score()
            self.scoreboard._prep_high_score()
        
        if collisions_2:
            for collision in collisions_2:
                self.stats.collision_x=collision.rect.x
                self.stats.collision_y=collision.rect.y
            self.stats.collisions_count+=2
            self.stats.point = 20
            self.time_show = pg.time.get_ticks() + 500
            self.music._music_money()
            self.pointboard._prep_point()
            self._update_score()
            self.scoreboard._prep_score()
            self.scoreboard._check_high_score()
            self.scoreboard._prep_high_score()
            
        


        
        if pg.sprite.spritecollideany(self.ship, self.aliens) or pg.sprite.spritecollideany(self.ship, self.aliens_2):#alien和船只相撞
            self.music._music_wrong()
            self._ship_hit()
    
    def _update_score(self):
            self.stats.score=self.stats.collisions_count*self.setting.alien_point
    
    
    def _level_up(self):
        ''' a Level up system'''
        if self.stats.alien_count==self.setting.alien_num:
            self.setting.level += 1
            self.stats.if_level_up=True
            self.time_show_level = pg.time.get_ticks() + 500
            self.pointboard._prep_arrow()
            self.bullet.empty()
            self.aliens.empty()
            self.stats.reset_status()#重置血条和小怪刷新个数
            self.level._prep_level()#刷新等级
            self.scoreboard._prep_heart()#刷新血条
            self.setting.increase_speed()#增速
            
            
        self.scoreboard._show_score()
       
        
    
    
    def run_game(self):   
        self.music._music_bg()
        while True:
            # self.music._music_bg()
            self._check_test()
            if self.screen_change:
                self.ship.screen_change(self)
                
            if self.stats.game_active:
                # print(self.stats.game_active)
                self.ship.update()
                self.bullet.update()
                self._update_bullet()
                self._check_bullet_alien_collisions()
                self.pointboard._update_arrow()
                self._level_up()
                self.boss.update()
                self.aliens.update()
                self.aliens_2.update()
                self._check_aliens_bottom()
                
            self._update_screen()
            
    