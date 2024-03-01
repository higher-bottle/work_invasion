#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 29 18:46:10 2024

@author: bingtinghuangfu
"""
import pygame as pg

class Music:
    def __init__(self,ai_game):
        pg.mixer.init()
        self.setting=ai_game.setting
        self.stats=ai_game.stats
        # self._music_money()
        # self._music_wrong()
        # self._music_bg()
        
    def _music_money(self):
        if self.stats.game_active:
            sound_money=pg.mixer.Sound(self.setting.music_money)
            # pg.mixer.music.load()
            sound_money.set_volume(0.2)
            sound_money.play()
    
    def _music_bg(self):  
        if self.stats.sound_play:
            pg.mixer.music.load(self.setting.music_bg)
            pg.mixer.music.set_volume(0.2)
            pg.mixer.music.play()
        
        
    def _music_wrong(self):
        if self.stats.game_active:
            sound_wrong=pg.mixer.Sound(self.setting.music_wrong)
            # pg.mixer.music.load()
            sound_wrong.set_volume(0.6)
            sound_wrong.play()
