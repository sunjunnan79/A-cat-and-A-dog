import threading

import pygame
import sys
import os
import random
import time
from mod.obstacle import obstaclelist, createdogObstacle, creatcatObstacle
import mod.animal
from mod.map import screen
from mod.map import start


class DogJumpThread(threading.Thread):
    def __init__(self, dog):
        super().__init__()
        self.dog = dog

    def run(self):
        self.dog.up()


class CatJumpThread(threading.Thread):
    def __init__(self, cat):
        super().__init__()
        self.cat = cat

    def run(self):
        self.cat.up()


class DogDownThread(threading.Thread):
    def __init__(self, dog):
        super().__init__()
        self.dog = dog

    def run(self):
        self.dog.down()


class CatDownThread(threading.Thread):
    def __init__(self, cat):
        super().__init__()
        self.cat = cat

    def run(self):
        self.cat.down()


class DogDefendThread(threading.Thread):
    def __init__(self, dog):
        super().__init__()
        self.dog = dog

    def run(self):
        self.dog.defend()


class CatDefendThread(threading.Thread):
    def __init__(self, cat):
        super().__init__()
        self.cat = cat

    def run(self):
        self.cat.defend()


class CatBeatThread(threading.Thread):
    def __init__(self, cat, dog):
        super().__init__()
        self.dog = dog
        self.cat = cat

    def run(self):
        self.cat.beat(self.dog)


class DogBeatThread(threading.Thread):
    def __init__(self, cat, dog):
        super().__init__()
        self.dog = dog
        self.cat = cat

    def run(self):
        self.dog.beat(self.cat)


class DogHurtThread(threading.Thread):
    def __init__(self, dog):
        super().__init__()
        self.dog = dog

    def run(self):
        self.dog.hurt()


class CatHurtThread(threading.Thread):
    def __init__(self, cat):
        super().__init__()
        self.cat = cat

    def run(self):
        self.cat.hurt()


def music_play():
    pygame.mixer.music.load(os.path.join("music", "music.mp3"))
    pygame.mixer.music.play(-1)  # 循环播放音乐
def Play():
    cat = mod.animal.Cat()
    dog = mod.animal.Dog()
    count = 0
    q = 400

    while cat.health and dog.health:
        count += 1
        if count == 5:
            count = 0
            q = max(50, q - 1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        key = pygame.key.get_pressed()

        # 猫的控制
        if key[pygame.K_w]:
            CatJumpThread(cat).start()
        elif key[pygame.K_s]:
            CatDownThread(cat).start()
        elif key[pygame.K_a]:
            cat.left()
        elif key[pygame.K_d]:
            cat.right()
        elif key[pygame.K_j]:
            CatBeatThread(cat, dog).start()
        elif key[pygame.K_k]:
            # CatgetDefendThread(cat).start()
            CatDefendThread(cat).start()

        # 狗的控制
        if key[pygame.K_UP]:
            DogJumpThread(dog).start()
        elif key[pygame.K_DOWN]:
            DogDownThread(dog).start()
        elif key[pygame.K_LEFT]:
            dog.left()
        elif key[pygame.K_RIGHT]:
            dog.right()
        elif key[pygame.K_KP1]:
            DogBeatThread(cat, dog).start()
        elif key[pygame.K_KP2]:
            DogDefendThread(dog).start()

        mod.map.create_map()  # 每帧重新绘制背景

        cat_image = cat.catStatus[cat.statues]
        cat_image_rect = cat_image.get_rect()
        cat_image_rect.bottomleft = (cat.catX, cat.catY)

        dog_image = dog.dogStatus[dog.statues]
        dog_image_rect = dog_image.get_rect()
        dog_image_rect.bottomleft = (dog.dogX, dog.dogY)

        dog_heart = dog.healthStatues[dog.health - 1]
        dog_heart_rect = dog_heart.get_rect()
        dog_heart_rect.bottomleft = (830, 70)

        cat_heart = cat.healthStatus[cat.health - 1]
        cat_heart_rect = cat_heart.get_rect()
        cat_heart_rect.bottomleft = (70, 70)

        cat_energy = cat.energyStatus[cat.energy]
        cat_energy_rect = cat_energy.get_rect()
        cat_energy_rect.bottomleft = (70, 140)

        dog_energy = dog.energyStatus[dog.energy]
        dog_energy_rect = dog_energy.get_rect()
        dog_energy_rect.bottomleft = (830, 140)

        if cat.beatS:
            cat_beatImage = pygame.transform.scale(pygame.image.load('.\\images\\fish.png'), (cat.size, cat.size))
            cat_beatImage = pygame.transform.rotate(cat_beatImage, cat.angle)
            beatRect = cat_beatImage.get_rect()
            beatRect.bottomleft = (cat.now_x, cat.now_y)
            screen.blit(cat_beatImage, beatRect)
            if dog_image_rect.colliderect(beatRect):
                DogHurtThread(dog).start()
                cat.beatS = False

        if dog.beatS:
            dog_beatImage = pygame.transform.scale(pygame.image.load('.\\images\\bone.png'), (dog.size, dog.size))
            dog_beatImage = pygame.transform.rotate(dog_beatImage, dog.angle)
            beatRect = dog_beatImage.get_rect()
            beatRect.bottomleft = (dog.now_x, dog.now_y)
            screen.blit(dog_beatImage, beatRect)
            if cat_image_rect.colliderect(beatRect):
                CatHurtThread(cat).start()
                dog.beatS = False

        if cat.defendStatus:
            cat_defendImage = pygame.transform.scale(pygame.image.load('.\\images\\denfendcat.png'), (200, 150))
            cat_defendRect = cat_defendImage.get_rect()
            cat_defendRect.bottomleft = (cat.catX - 35, cat.catY - 15)
            screen.blit(cat_defendImage, cat_defendRect)

        if dog.defendStatus:
            dog_defendImage = pygame.transform.scale(pygame.image.load('.\\images\\denfendcat.png'), (200, 150))
            dog_defendRect = dog_defendImage.get_rect()
            dog_defendRect.bottomleft = (dog.dogX - 35, dog.dogY - 15)
            screen.blit(dog_defendImage, dog_defendRect)

        if cat.hurtStatus:
            cat_hurtImage = pygame.transform.scale(pygame.image.load('.\\images\\hurt.png'), (100, 75))
            cat_hurtRect = cat_hurtImage.get_rect()
            cat_hurtRect.bottomleft = (cat.catX + 15, cat.catY - 80)
            screen.blit(cat_hurtImage, cat_hurtRect)

        if dog.hurtStatus:
            finalImage = pygame.transform.scale(pygame.image.load('.\\images\\hurt.png'), (100, 75))
            finalRect = finalImage.get_rect()
            finalRect.bottomleft = (dog.dogX + 15, dog.dogY - 80)
            screen.blit(finalImage, finalRect)

        # 创建新障碍物
        if random.randint(1, q) == 1:
            createdogObstacle()
            creatcatObstacle()

        # 移动障碍物
        # 复制当前的障碍物的副本并游历
        for obstacle in obstaclelist[:]:
            obstacle.move()
            # 碰撞检测
            if dog_image_rect.colliderect(obstacle.obstacleRect):
                if obstacle.type == 'dog_sky':
                    dog.getenergy()
                else:
                    DogHurtThread(dog).start()
                obstacle.destroy()
            if cat_image_rect.colliderect(obstacle.obstacleRect):
                if obstacle.type == 'cat_sky':
                    cat.getenergy()
                else:
                    CatHurtThread(cat).start()
                obstacle.destroy()
            obstacle.remove()

        screen.blit(cat_image, cat_image_rect)
        screen.blit(dog_image, dog_image_rect)
        screen.blit(cat_heart, cat_heart_rect)
        screen.blit(dog_heart, dog_heart_rect)
        screen.blit(cat_energy, cat_energy_rect)
        screen.blit(dog_energy, dog_energy_rect)

        for obstacle in obstaclelist:
            screen.blit(obstacle.obstacleStatus, obstacle.obstacleRect)

        pygame.display.flip()
        clock.tick(100)  # 控制帧率

    if dog.health:
        finalImage = pygame.transform.scale(pygame.image.load('.\\images\\dogwin.png'), (500, 500))
        finalRect = finalImage.get_rect()
        finalRect.bottomleft = (350, 600)
        cat_heart = pygame.transform.scale(pygame.image.load('.\\images\\heart0.png'), (300, 50))
        cat_heart_rect = cat_heart.get_rect()
        cat_heart_rect.bottomleft = (70, 70)
        mod.map.screen.blit(finalImage, finalRect)
        mod.map.screen.blit(cat_heart, cat_heart_rect)
    else:
        finalImage = pygame.transform.scale(pygame.image.load('.\\images\\catwin.png'), (500, 500))
        finalRect = finalImage.get_rect()
        finalRect.bottomleft = (350, 600)
        dog_heart = pygame.transform.scale(pygame.image.load('.\\images\\heart0.png'), (300, 50))
        dog_heart_rect = dog_heart.get_rect()
        dog_heart_rect.bottomleft = (830, 70)
        mod.map.screen.blit(finalImage, finalRect)
        mod.map.screen.blit(dog_heart, dog_heart_rect)
    # 清空障碍物列表
    obstaclelist.clear()
    pygame.display.flip()
    time.sleep(5)



if __name__ == "__main__":
    # 初始化
    pygame.init()
    pygame.mixer.init()
    pygame.display.set_caption("猫狗大战")
    clock = pygame.time.Clock()
    music_play()

    while start():
        Play()

