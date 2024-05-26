import pygame
import random
import sys
import time

from mod.animal import cat_y, dog_y

obstaclelist = []
y_max = 900
y_min = 0
x_max = 1000
x_min = 50
speed = 5

def creatcatObstacle():  # 创建障碍物
    i = random.randint(1, 130)
    if i <= 50:
        obstacle = Obstacle1()
        obstacle.obstacleY = cat_y
    elif 50 < i <= 100:
        obstacle = Obstacle2()
        obstacle.obstacleY = random.randint(y_min + 100, y_min + 200)
    else:
        obstacle = Obstacle3()
        obstacle.obstacleY = 0
        obstacle.obstacleX = random.randint(x_min, x_max)

    obstaclelist.append(obstacle)


def createdogObstacle():
    i = random.randint(1, 130)
    if i <= 50:
        obstacle = Obstacle1()
        obstacle.obstacleY = dog_y
    elif 50 < i <= 100:
        obstacle = Obstacle2()
        obstacle.obstacleY = random.randint(y_max // 2 + 100, y_max//2+ 200)
    else:
        obstacle = Obstacle4()
        obstacle.obstacleY = 0
        obstacle.obstacleX = random.randint(x_min, x_max)

    obstaclelist.append(obstacle)


class Obstacle1(object):  # 地上的障碍物
    def __init__(self):
        self.obstacleStatus = pygame.transform.scale(pygame.image.load('.\\images\\obstacle1.png'), (50, 50))
        self.obstacleRect = self.obstacleStatus.get_rect()
        self.speed = speed
        self.obstacleX = 1200
        self.obstacleY = 0
        self.type = 'sky'

    def move(self):
        self.obstacleX -= self.speed
        self.obstacleRect.bottomleft = (self.obstacleX, self.obstacleY)

    def remove(self):
        if self.obstacleX < 0:
            obstaclelist.remove(self)

    def destroy(self):
        obstaclelist.remove(self)


class Obstacle2(object):  # 空中的障碍物
    def __init__(self):
        self.obstacleStatus = pygame.transform.scale(pygame.image.load('.\\images\\obstacle2.png'), (50, 50))
        self.obstacleRect = self.obstacleStatus.get_rect()
        self.speed = speed
        self.obstacleX = 1200
        self.obstacleY = 0
        self.type = 'sky'

    def move(self):
        self.obstacleX -= self.speed
        self.obstacleRect.bottomleft = (self.obstacleX, self.obstacleY)

    def remove(self):
        if self.obstacleX <= 0:
            obstaclelist.remove(self)

    def destroy(self):
        obstaclelist.remove(self)


class Obstacle3(object):  # 天降的障碍物
    def __init__(self):
        self.obstacleStatus = pygame.transform.scale(pygame.image.load('.\\images\\fish.png'), (50, 50))
        self.obstacleRect = self.obstacleStatus.get_rect()
        self.speed = speed
        self.obstacleX = 0
        self.obstacleY = 0
        self.type = 'cat_sky'

    def move(self):
        self.obstacleY += self.speed
        self.obstacleRect.bottomleft = (self.obstacleX, self.obstacleY)

    def remove(self):
        if self.obstacleY >= 900:
            obstaclelist.remove(self)

    def destroy(self):
        obstaclelist.remove(self)

class Obstacle4(object):  # 天降的障碍物
    def __init__(self):
        self.obstacleStatus = pygame.transform.scale(pygame.image.load('.\\images\\bone.png'), (50, 50))
        self.obstacleRect = self.obstacleStatus.get_rect()
        self.speed = speed
        self.obstacleX = 0
        self.obstacleY = 0
        self.type = 'dog_sky'

    def move(self):
        self.obstacleY += self.speed
        self.obstacleRect.bottomleft = (self.obstacleX, self.obstacleY)

    def remove(self):
        if self.obstacleY >= 900:
            obstaclelist.remove(self)

    def destroy(self):
        obstaclelist.remove(self)