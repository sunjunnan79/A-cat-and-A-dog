import pygame
import random
import sys

# 初始化Pygame
pygame.init()

# 设定屏幕尺寸
screen_width = 800
screen_height = 600
# 初始化屏幕
screen = pygame.display.set_mode((screen_width, screen_height))
# 设置标题
pygame.display.set_caption("躲避障碍物")

# 颜色定义
WHITE = (255, 255, 255)

# 加载图片
player_image = pygame.image.load('player.gif')
# 设置图片大小
player_image = pygame.transform.scale(player_image, (100, 100))
# 加载图形的边距
player_rect = player_image.get_rect()
# 设置左上角位置
player_rect.topleft = (screen_width // 2, screen_height - player_rect.height - 10)
# 加载图片
obstacle_image = pygame.image.load('obstacle.jpg')
# 将障碍物缩放为50x50像素
obstacle_image = pygame.transform.scale(obstacle_image, (50, 50))
# 加载图形边距
obstacle_rect = obstacle_image.get_rect()

# 游戏变量
player_speed = 5
obstacle_speed = 5
obstacles = []

# 时钟
clock = pygame.time.Clock()

# 主游戏循环开始
running = True
while running:
    # 遍历事件逐个处理
    for event in pygame.event.get():
        # 如果获取到退出信号则直接退出
        if event.type == pygame.QUIT:
            running = False

    # 获取按键状态
    keys = pygame.key.get_pressed()
    # 判断按键并执行相应操作
    # pygame.K_LEFT左方向键按下并且玩家的坐标大于左界
    if keys[pygame.K_LEFT] and player_rect.left > 0:
        player_rect.x -= player_speed
    # pygame.K_RIGHT左方向键按下并且玩家的坐标小于右界
    if keys[pygame.K_RIGHT] and player_rect.right < screen_width:
        player_rect.x += player_speed

    # 创建新障碍物
    if random.randint(1, 20) == 1:
        # 复制一个障碍物副本
        new_obstacle = obstacle_rect.copy()
        # 随机创建障碍物的位置
        new_obstacle.topleft = (random.randint(0, screen_width - new_obstacle.width), -new_obstacle.height)
        # 在障碍物列表中添加障碍物
        obstacles.append(new_obstacle)

    # 移动障碍物
    # 复制当前的障碍物的副本并游历
    for obstacle in obstacles[:]:
        # 移动障碍物的位置
        obstacle.y += obstacle_speed
        # 移除超出底部的障碍物
        if obstacle.top > screen_height:
            obstacles.remove(obstacle)
        # 碰撞检测
        if player_rect.colliderect(obstacle):
            running = True  # 玩家碰到障碍物，游戏结束

    # 绘制
    screen.fill(WHITE)
    screen.blit(player_image, player_rect.topleft)
    for obstacle in obstacles:
        screen.blit(obstacle_image, obstacle.topleft)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
