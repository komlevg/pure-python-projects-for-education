import pygame
from random import randrange
import pymunk.pygame_util
#создание единой системы координат, нужно из-за различий используемых библиотек
pymunk.pygame_util.positive_y_is_up = False

RES = WIDTH, HEIGHT = 1000, 800
FPS = 60

pygame.init()
surface = pygame.display.set_mode(RES)
clock = pygame.time.Clock()
#возможность отрисовки физобъектов из библиотеки pymunk
draw_options = pymunk.pygame_util.DrawOptions(surface)
#создание пространства с физ законами
space = pymunk.Space()
space.gravity = 0, 3000
ball_mass, ball_radius = 1, 7
segment_thickness = 6

a, b, c, d = 10, 100, 18, 40
x1, x2, x3, x4 = a, WIDTH // 2 - c, WIDTH // 2 + c, WIDTH - a
y1, y2, y3, y4, y5 = b, HEIGHT // 4 - d, HEIGHT // 4, HEIGHT // 2 - 1.5 * b, HEIGHT - 4 * b
L1, L2, L3, L4 = (x1, -100), (x1, y1), (x2, y2), (x2, y3)
R1, R2, R3, R4 = (x4, -100), (x4, y1), (x3, y2), (x3, y3)
B1, B2 = (0, HEIGHT), (WIDTH, HEIGHT)


def create_ball(space):
    # создание динамического объекта шарика и определение его свойств

    # определение момента инерции
    ball_moment = pymunk.moment_for_circle(ball_mass, 0, ball_radius)
    # создание тела объекта
    ball_body = pymunk.Body(ball_mass, ball_moment)
    ball_body.position = randrange(x1, x4), randrange(-y1, y1)
    # создание формы в виде окружности
    ball_shape = pymunk.Circle(ball_body, ball_radius)
    #2добавление упругости нашим шарам
    ball_shape.elasticity = 0.1
    #3добавление силы трения
    ball_shape.friction = 0.1
    #ball_shape.color = [randrange(256) for i in range(4)]
    # создание одного шара
    space.add(ball_body, ball_shape)
    return ball_body

def create_segment(from_, to_, thickness, space, color):
    segment_shape = pymunk.Segment(space.static_body, from_, to_, thickness)
    segment_shape.color = pygame.color.THECOLORS[color]
    space.add(segment_shape)


platforms = (L1, L2), (L2, L3), (L3, L4), (R1, R2), (R2, R3), (R3, R4)
for platforms in platforms:
    create_segment(*platforms, segment_thickness, space, 'green')
create_segment(B1, B2, 20, space, 'green')

def create_peg(x, y, space, color):
    circle_shape = pymunk.Circle(space.static_body, radius=10, offset=(x, y))
    circle_shape.color = pygame.color.THECOLORS[color]
    circle_shape.elasticity = 0.1
    circle_shape.friction = 0.5
    space.add(circle_shape)


# pegs
peg_y, step = y4, 60
for i in range(10):
    peg_x = -1.5 * step if i % 2 else -step
    for j in range(WIDTH // step + 2):
        create_peg(peg_x, peg_y, space, 'darkslateblue')
        if i == 9:
            create_segment((peg_x, peg_y + 50), (peg_x, HEIGHT), segment_thickness, space, 'darkslategray')
        peg_x += step
    peg_y += 0.5 * step


balls = [([randrange(256) for i in range(3)], create_ball(space)) for j in range(600)]


while True:
    surface.fill(pygame.Color('black'))

    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            exit()
        if i.type == pygame.MOUSEBUTTONDOWN:
            if i.button == 1:
                create_ball(space, i.pos)

    #шаг единицы/времени для вычислений в пространстве пайманк в связи количеством кадров
    space.step(1 / FPS)
    #отображение пространства
    space.debug_draw(draw_options)

    pygame.display.flip()
    clock.tick(FPS)