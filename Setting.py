#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 29 18:27:17 2024

@author: bingtinghuangfu
"""

import os
class Setting:
    def __init__(self):
       
        self.bg_color = (230,230,230)
        self.screen_size = (800,900)

        self.level_setting()
        self.music_setting()
        self.boss_setting()
        self.bullet_setting()
        self.alien_setting()
        self.heart_setting()
        self.ship_setting()
        self.arrow_setting()
        
        
        
    def level_setting(self):
        self.level = 0
        
    def music_setting(self):
        self.music_money = os.path.join("Music",'金币.mp3')
        self.music_wrong = os.path.join("Music", 'wrong.mp3')
        self.music_bg = os.path.join("Music", 'bgm.mp3')
        self.sound_image = os.path.join("Image", 'sound.png')
        self.mute_image = os.path.join("Image", 'mute.png')

    def boss_setting(self):
        # self.Boss_image='Image/Boss.png'
        self.Boss_image = os.path.join("Image", 'Boss.png')
        self.boss_width=100
        
    def bullet_setting(self):
        self.bullet_allowed=6
        self.bullet_color=(60,60,60)
        self.bullet_speed=3.0

    def alien_setting(self):
        self.alien_width = 50
        
        # self.alien_image_1 = 'Image/excel.png'
        self.alien_image_1 = os.path.join("Image", 'excel.png')

        self.alien_speed = 0.5
        self.alien_speedup_scale = 1.2#加速系数
        self.alien_num_scale=1.1
        self.alien_interval = 3_000
        self.alien_num = 10#每一轮alien掉落个数
        self.alien_count = 0
        
        # self.alien_image_2 = 'Image/powerpoint.png'
        self.alien_image_2 = os.path.join("Image", 'powerpoint.png')

        self.alien_speed_2 = 0.2
        self.alien_num_2 = 4
        self.alien_count_2 = 0
        self.alien_interval_2 = 5_000
        
        

    def heart_setting(self):
        self.heart_width = 30
        # self.heart_image = 'Image/heart.png'
        self.heart_image = os.path.join("Image", 'heart.png')
        
    def ship_setting(self):
        self.ship_image = os.path.join('Image','Ship.png')
        self.ship_width=130
        self.ship_height=180
        self.ship_limit=2


    def arrow_setting(self):
        self.arrow_image = os.path.join("Image", 'arrow.jpg')



    def initialize_dynamic_settings(self):
        '''Initialize settings that change throughout the game.'''
        self.ship_speed=1.5
        self.bullet_speed=3.0
        self.alien_speed = 0.3
        self.alien_speed_2 = 0.1
        
        self.boss_direction=0
        self.alien_point=10#单位得分

    def increase_speed(self):
        '''increase speed setting'''
        self.ship_speed*=self.alien_speedup_scale
        self.bullet_speed*=self.alien_speedup_scale
        self.alien_speed*=self.alien_speedup_scale    
        self.alien_speed_2*=self.alien_speedup_scale
        self.alien_num*=round(self.alien_num_scale)