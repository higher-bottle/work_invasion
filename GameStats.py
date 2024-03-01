#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 29 18:39:07 2024

@author: bingtinghuangfu
"""

class GameStats:
    def __init__(self,ai_game):
        self.game_active=False
        self.setting=ai_game.setting
        self.high_score=0
        self.point = 0
        self.collision_x = 0
        self.collision_y = 0
        self.sound_play = True
        # self.sound_play_sign = True
        self.reset_status()
        
        
    def reset_status(self):
        self.ships_left=self.setting.ship_limit#重置ship被击中次数
        self.alien_count=self.setting.alien_count
        self.alien_count_2=self.setting.alien_count_2
        self.if_level_up=False
        
        if  not self.setting.level:
            self.collisions_count=0
            self.score=0