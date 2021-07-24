import pygame
from random import randrange as rnd

WIDTH, HEIGHT = 1280, 720
fps = 60
#параметры платформы
platform_w = 300
platform_h = 30
platform_speed = 15
platform = pygame.Rect(WIDTH // 2 - platform_w // 2, HEIGHT - platform_h - 10, platform_w, platform_h)
#параметры шара
ball_radius = 20
ball_speed = 6
#вар для расчета стороны квадрата вписанного в шарик для расчета столкновений
ball_rect = int(ball_radius * 2 ** 0.5)
#рандомное размещение шарика
ball = pygame.Rect(rnd(ball_rect, WIDTH - ball_rect), HEIGHT // 2, ball_rect, ball_rect)
dx, dy = 1, -1
#настройки блоков
block_list = [pygame.Rect(10 + 129 * i, 10 + 70 * j, 100, 50) for i in range(10) for j in range(4)]
color_list = [(rnd(30, 256), rnd(30, 256), rnd(30, 256)) for i in range(10) for j in range(4)]

pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
#изменение фон.изобр.
img = pygame.image.load('testimg1280I720.jpg').convert()

def detect_collision(dx, dy, ball, rect):
    if dx > 0:
        delta_x = ball.right - rect.left
    else:
        delta_x = rect.right - ball.left
    if dy > 0:
        delta_y = ball.bottom - rect.top
    else:
        delta_y = rect.bottom - ball.top

    if abs(delta_x - delta_y) < 10:
        dx, dy = -dx, -dy
    elif delta_x > delta_y:
        dy = -dy
    elif delta_y > delta_x:
        dx = -dx
    return dx, dy

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    sc.blit(img, (0, 0))
    #отрисовка объектов в игре
    [pygame.draw.rect(sc, color_list[color], block) for color, block in enumerate(block_list)]
    pygame.draw.rect(sc, pygame.Color('red'), platform)
    pygame.draw.circle(sc, pygame.Color('black'), ball.center, ball_radius)
    #движение шара
    ball.x += ball_speed * dx
    ball.y += ball_speed * dy
    #отражение шара при столкновениях(лево и право)
    if ball.centerx < ball_radius or ball.centerx > WIDTH - ball_radius:
        dx = -dx
    #отражение шара при столкновениях(верх)
    if ball.centery < ball_radius:
        dy = -dy
    #отражение шара при столкновениях(с платформой)
    if ball.colliderect(platform) and dy > 0:
        dx, dy = detect_collision(dx, dy, ball, platform)
    #отражение шара при столкновениях(с блоками)
    hit_index = ball.collidelist(block_list)
    if hit_index != -1:
        hit_rect = block_list.pop(hit_index)
        hit_color = color_list.pop(hit_index)
        dx, dy = detect_collision(dx, dy, ball, hit_rect)
        #DLC
        hit_rect.inflate_ip(ball.width * 4, ball.height * 4)
        pygame.draw.rect(sc, hit_color, hit_rect)
        fps += 2
    #конец игры
    if ball.bottom > HEIGHT:
        exit()
    elif not len(block_list):
        exit()
    #управление
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and platform.left > 0:
        platform.left -= platform_speed
    if key[pygame.K_RIGHT] and platform.right < WIDTH:
        platform.right += platform_speed


    pygame.display.flip()
    clock.tick(fps)