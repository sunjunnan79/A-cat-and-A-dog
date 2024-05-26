import os
import random
import threading

import pygame
import sys
import time

from mod.map import create_map, screen
from threading import Timer
cat_x = 120
cat_y = 400
dog_x = 120
dog_y = 850
defenceTime = 2
y_max = 900
y_min = 0
x_max = 1000
x_min = 50
times = 60
def play_sound_effect(file_path, start_time, duration):
    sound = pygame.mixer.Sound(file_path)
    sound.play(loops=0, maxtime=duration, fade_ms=0)

def Cat_sound():
    play_sound_effect(file_path='./music/cat.mp3', start_time=0, duration=1000)

def Dog_sound():
    play_sound_effect(file_path='./music/dog.mp3', start_time=0, duration=2000)
class Cat(object):
    def __init__(self):
        self.hurtStatus = False
        self.catStatus = [pygame.transform.scale(pygame.image.load('.\\images\\cat1.png'), (100, 100)),  # 正常向右移动
                          pygame.transform.scale(pygame.image.load('.\\images\\cat2.png'), (115, 90)),  # 跳跃向右移动
                          pygame.transform.scale(pygame.image.load('.\\images\\cat3.png'), (115, 90)),  # 下滑向右移动
                          pygame.transform.scale(pygame.image.load('.\\images\\cat4.png'), (100, 100)),  # 正常向左移动
                          pygame.transform.scale(pygame.image.load('.\\images\\cat5.png'), (115, 90)),  # 跳跃向左移动
                          pygame.transform.scale(pygame.image.load('.\\images\\cat6.png'), (115, 90)),  # 下滑向左移动
                          ]
        self.statues = 0
        self.catX = cat_x
        self.catY = cat_y
        self.jumpStatues = False
        self.defendStatus = False  # 默认为非防御状态
        self.health = 5  # 血条
        self.healthStatus = [
            pygame.transform.scale(pygame.image.load('.\\images\\heart1.png'), (300, 50)),
            pygame.transform.scale(pygame.image.load('.\\images\\heart2.png'), (300, 50)),
            pygame.transform.scale(pygame.image.load('.\\images\\heart3.png'), (300, 50)),
            pygame.transform.scale(pygame.image.load('.\\images\\heart4.png'), (300, 50)),
            pygame.transform.scale(pygame.image.load('.\\images\\heart5.png'), (300, 50)),
        ]
        self.beatS = False
        self.now_x = 0
        self.now_y = 0
        self.angle = 0
        self.size = 50
        self.energy = 5  # 能量
        self.energyStatus = [
            pygame.transform.scale(pygame.image.load('.\\images\\energy0.png'), (300, 50)),
            pygame.transform.scale(pygame.image.load('.\\images\\energy1.png'), (300, 50)),
            pygame.transform.scale(pygame.image.load('.\\images\\energy2.png'), (300, 50)),
            pygame.transform.scale(pygame.image.load('.\\images\\energy3.png'), (300, 50)),
            pygame.transform.scale(pygame.image.load('.\\images\\energy4.png'), (300, 50)),
            pygame.transform.scale(pygame.image.load('.\\images\\energy5.png'), (300, 50)),
        ]

    def up(self):
        if self.jumpStatues == False and self.statues == 0:
            self.jumpStatues = True
            self.statues = 1
            for i in range(10):  # 上升
                time.sleep(0.02)
                self.catY = self.catY - 10
            # 停留
            time.sleep(0.5)
            for i in range(10):  # 下降
                time.sleep(0.02)
                self.catY = self.catY + 10
            self.statues = 0
            self.jumpStatues = False
        elif self.jumpStatues == False and self.statues == 3:
            self.jumpStatues = True
            self.statues = 4
            for i in range(10):  # 上升
                time.sleep(0.02)
                self.catY = self.catY - 10
            # 停留
            time.sleep(0.5)
            for i in range(10):  # 下降
                time.sleep(0.02)
                self.catY = self.catY + 10
            self.statues = 3
            self.jumpStatues = False

    def down(self):
        if self.statues == 0:
            self.statues = 2
            time.sleep(0.9)
            self.statues = 0
        elif self.statues == 3:
            self.statues = 5
            time.sleep(0.9)
            self.statues = 3

    def left(self):
        if self.jumpStatues:
            self.statues = 4
        else:
            self.statues = 3
        if self.catX > x_min:
            self.catX = self.catX - 5

    def right(self):
        if self.jumpStatues:
            self.statues = 1
        else:
            self.statues = 0
        if self.catX < x_max:
            self.catX = self.catX + 5

    def beat(self, dog):
        if self.energy == 5:
            self.beatS = True
            self.useenergy()
            self.angle = 0
            rotation_speed = 360 / times

            target_y = dog.dogY
            target_x = dog.dogX

            move_x_speed = (target_x - self.catX) // times
            move_y_speed = (target_y - self.catY) // times
            self.now_y = self.catY
            self.now_x = self.catX
            while self.now_y < target_y:
                self.now_x += move_x_speed
                self.now_y += move_y_speed
                self.angle += rotation_speed
                self.size *= 1.02
                time.sleep(0.02)
            self.beatS = False



    def defend(self):
        if not self.defendStatus and self.energy == 5:
            self.defendStatus = True
            self.useenergy()
            time.sleep(defenceTime)
            self.defendStatus = False

    def getenergy(self):  # 获得能量
        if not self.defendStatus and self.energy < 5:
            self.energy += 1

    def useenergy(self):
        if self.energy >= 5:
            self.energy -= 5

    def cutlive(self):  # 扣除生命
        if not self.defendStatus:
            self.health -= 1
            Cat_sound()
    def hurt(self):
        if not self.hurtStatus:
            self.hurtStatus = True
            self.cutlive()
            time.sleep(defenceTime)
            self.hurtStatus = False


class Dog(object):
    def __init__(self):
        self.hurtStatus = False
        self.size = 50
        self.dogStatus = [
            pygame.transform.scale(pygame.image.load('.\\images\\dog1.png'), (100, 100)),  # 正常向右移动
            pygame.transform.scale(pygame.image.load('.\\images\\dog2.png'), (115, 90)),  # 跳跃向右移动
            pygame.transform.scale(pygame.image.load('.\\images\\dog3.png'), (115, 90)),  # 下滑向右移动
            pygame.transform.scale(pygame.image.load('.\\images\\dog4.png'), (100, 100)),  # 正常向左移动
            pygame.transform.scale(pygame.image.load('.\\images\\dog5.png'), (115, 90)),  # 跳跃向左移动
            pygame.transform.scale(pygame.image.load('.\\images\\dog6.png'), (115, 90)),  # 下滑向左移动
        ]
        self.statues = 0
        self.dogX = dog_x
        self.dogY = dog_y
        self.jumpStatues = False
        self.defendStatus = False  # 默认为非防御状态
        self.health = 5  # 血条
        self.healthStatues = [
            pygame.transform.scale(pygame.image.load('.\\images\\heart1.png'), (300, 50)),
            pygame.transform.scale(pygame.image.load('.\\images\\heart2.png'), (300, 50)),
            pygame.transform.scale(pygame.image.load('.\\images\\heart3.png'), (300, 50)),
            pygame.transform.scale(pygame.image.load('.\\images\\heart4.png'), (300, 50)),
            pygame.transform.scale(pygame.image.load('.\\images\\heart5.png'), (300, 50)),
        ]
        self.beatS = False
        self.now_x = 0
        self.now_y = 0
        self.angle = 0
        self.energy = 5  # 能量
        self.energyStatus = [
            pygame.transform.scale(pygame.image.load('.\\images\\energy0.png'), (300, 50)),
            pygame.transform.scale(pygame.image.load('.\\images\\energy1.png'), (300, 50)),
            pygame.transform.scale(pygame.image.load('.\\images\\energy2.png'), (300, 50)),
            pygame.transform.scale(pygame.image.load('.\\images\\energy3.png'), (300, 50)),
            pygame.transform.scale(pygame.image.load('.\\images\\energy4.png'), (300, 50)),
            pygame.transform.scale(pygame.image.load('.\\images\\energy5.png'), (300, 50)),
        ]

    def up(self):
        if self.jumpStatues == False and self.statues == 0:
            self.jumpStatues = True
            self.statues = 1
            for i in range(10):  # 上升
                time.sleep(0.02)
                self.dogY = self.dogY - 10
            # 停留
            time.sleep(0.5)
            for i in range(10):  # 下降
                time.sleep(0.02)
                self.dogY = self.dogY + 10
            self.statues = 0
            self.jumpStatues = False
        elif self.jumpStatues == False and self.statues == 3:
            self.jumpStatues = True
            self.statues = 4
            for i in range(10):  # 上升
                time.sleep(0.02)
                self.dogY = self.dogY - 10
            # 停留
            time.sleep(0.5)
            for i in range(10):  # 下降
                time.sleep(0.02)
                self.dogY = self.dogY + 10
            self.statues = 3
            self.jumpStatues = False

    def down(self):
        if self.statues == 0:
            self.statues = 2
            time.sleep(0.9)
            self.statues = 0
        elif self.statues == 3:
            self.statues = 5
            time.sleep(0.9)
            self.statues = 3

    def left(self):
        if self.jumpStatues:
            self.statues = 4
        else:
            self.statues = 3
        if self.dogX > x_min:
            self.dogX = self.dogX - 5

    def right(self):
        if self.jumpStatues:
            self.statues = 1
        else:
            self.statues = 0
        if self.dogX < x_max:
            self.dogX = self.dogX + 5

    def beat(self, cat):
        if self.energy == 5:
            self.beatS = True
            self.useenergy()
            self.angle = 0
            rotation_speed = 360 / times

            target_y = cat.catY


            target_x = cat.catX

            move_x_speed = (target_x - self.dogX) // times
            move_y_speed = (target_y - self.dogY) // times
            self.now_y = self.dogY
            self.now_x = self.dogX
            while self.now_y > target_y:
                self.now_x += move_x_speed
                self.now_y += move_y_speed
                self.angle += rotation_speed
                self.size *= 1.01
                time.sleep(0.02)
            self.beatS = False


    def getDefend(self):
        while self.defendStatus:
            finalImage = pygame.transform.scale(pygame.image.load('.\\images\\obstacle1.png'), (50, 50))
            finalRect = finalImage.get_rect()
            finalRect.bottomleft = (self.dogX, self.dogY)
            screen.blit(finalImage, finalRect)

    def defend(self):
        if not self.defendStatus and self.energy == 5:
            self.defendStatus = True
            self.useenergy()
            time.sleep(defenceTime)
            self.defendStatus = False

    def getenergy(self):  # 获得能量
        if not self.defendStatus and self.energy < 5:
            self.energy += 1

    def useenergy(self):
        if self.energy >= 5:
            self.energy -= 5

    def cutlive(self):  # 扣除生命
        if not self.defendStatus:
            self.health -= 1
            Dog_sound()

    def hurt(self):
        if not self.hurtStatus:
            self.hurtStatus = True
            self.cutlive()
            time.sleep(defenceTime)
            self.hurtStatus = False
