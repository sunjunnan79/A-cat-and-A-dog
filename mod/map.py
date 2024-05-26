import os
import sys
import pygame
import time

background = pygame.transform.scale(pygame.image.load(os.path.join("images", "background1.jpg")),(1200,900))
size = screen_width, screen_height = 1200, 900
screen = pygame.display.set_mode(size, pygame.DOUBLEBUF)  # 使用双缓冲


pygame.font.init()
# 设置字体
font = pygame.font.Font(None, 74)

# 创建按钮
button_color = (128, 217, 89)
button_hover_color = (107, 186, 71)
button_rect = pygame.Rect(screen_width // 2 - 100, screen_height // 2 - 50, 170, 90)
button_text = font.render("Start", True, (0, 0, 0))
button_rect2 = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 80, 170, 90)
button_text2 = font.render("Quit", True, (0, 0, 0))
def create_map():
    screen.fill((255, 255, 255))
    screen.blit(background, (0, 0))


def temp(i):
    screen.fill((255, 255, 255))
    screen.blit(background, (0, 0))
    button_text3 = font.render("    "+str(i), True, (0, 0, 0))
    pygame.draw.rect(screen, button_color, button_rect)
    screen.blit(button_text3, (button_rect.x + 20, button_rect.y + 20))
    pygame.display.flip()
    time.sleep(1)

def start():
    running = True
    while running:
        screen.fill((255, 255, 255))
        screen.blit(background, (0, 0))

        # 检测鼠标位置，改变按钮颜色
        mouse_pos = pygame.mouse.get_pos()
        if button_rect.collidepoint(mouse_pos):
            color = button_hover_color
        else:
            color = button_color
        # 绘制按钮
        pygame.draw.rect(screen, color, button_rect)
        screen.blit(button_text, (button_rect.x + 20, button_rect.y + 20))

        # 检测鼠标位置，改变按钮颜色
        if button_rect2.collidepoint(mouse_pos):
            color = button_hover_color
        else:
            color = button_color
        # 绘制按钮
        pygame.draw.rect(screen, color, button_rect2)
        screen.blit(button_text2, (button_rect2.x + 20, button_rect2.y + 20))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    for i in range(3,0,-1):
                        temp(i)
                    create_map()
                    return True# 跳出循环，开始游戏
                if button_rect2.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()