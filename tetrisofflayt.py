import pygame
from copy import deepcopy
from random import choice, randrange

pygame.init()

w = 10
h = 20

tile = 45

game_resolution = tile * w, tile * h
res = 750, 940

screen_x = 300
screen_y = 600
fps = 60


on = pygame.display.set_mode(res)
game_on = pygame.Surface(game_resolution)
clock = pygame.time.Clock()
pygame.display.set_caption("Tetris by offlayt")


grid = [pygame.Rect(x * tile, y * tile, tile, tile) for x in range(w) for y in range(h)]

details = [
    [[-1, 0], [-2, 0], [0, 0], [1, 0]],
    [[0, -1], [-1, -1], [-1, 0], [0, 0]],
    [[-1, 0], [-1, 1], [0, 0], [0, -1]],
    [[0, 0], [-1, 0], [0, 1], [-1, -1]],
    [[0, 0], [0, -1], [0, 1], [-1, -1]],
    [[0, 0], [0, -1], [0, 1], [1, -1]],
    [[0, 0], [0, -1], [0, 1], [-1, 0]]
    ]


details = [[pygame.Rect(x + w // 2, y + 1, 1, 1) for x, y in DET_pos] for DET_pos in details]

detail_rect = pygame.Rect(0, 0, tile - 2, tile - 2)
field = [[0 for i in range(w)] for j in range(h)]

anim_count, anim_speed, anim_limit = 0, 60, 2000


# фоны
background = pygame.image.load('img/bg1.png').convert()
game_background = pygame.image.load('img/bg3.png').convert()



#шрифты

main_font = pygame.font.Font('font/font.ttf', 60)
font = pygame.font.Font('font/font.ttf', 40)
font_offlayt = pygame.font.Font('font/font.ttf', 25)

title_tetris = main_font.render('TETRIS', True, pygame.Color('black'))
title_score = font.render('ОЧКИ:', True, pygame.Color('yellow'))
title_record = font.render('РЕКОРД:', True, pygame.Color('purple'))
title_offlayt = font_offlayt.render('by offlayt', True, pygame.Color('black'))






get_color = lambda : (randrange(30, 256), randrange(30, 256), randrange(30, 256))

detail, next_detail = deepcopy(choice(details)), deepcopy(choice(details))
color, next_color = get_color(), get_color()

score, lines = 0, 0
scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}


def check_borders():
    if detail[i].x < 0 or detail[i].x > w - 1:
        return False
    elif detail[i].y > h - 1 or field[detail[i].y][detail[i].x]:
        return False
    return True
def get_record():
    try:
        with open('record') as f:
            return f.readline()
    except FileNotFoundError:
        with open('record', 'w') as f:
            f.write('0')
def set_record(record, score):
    rec = max(int(record), score)
    with open('record', 'w') as f:
        f.write(str(rec))
while True:
    record = get_record()
    dx, rotate = 0, False
    on.blit(background, (0, 0))
    on.blit(game_on, (20, 20))
    game_on.blit(game_background, (0, 0))


    # delay for full lines
    for i in range(lines):
        pygame.time.wait(200)





    # кнопки
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dx = -1
            elif event.key == pygame.K_RIGHT:
                dx = 1
            elif event.key == pygame.K_DOWN:  #can 'K_z' and more
                anim_limit = 100
            elif event.key == pygame.K_SPACE:
                anim_limit = 100

            elif event.key == pygame.K_UP:
                rotate = True






    # x
    detail_old = deepcopy(detail)
    for i in range(4):
        detail[i].x += dx
        if not check_borders():
            detail = deepcopy(detail_old)
            break
    # y
    anim_count += anim_speed
    if anim_count > anim_limit:
        anim_count = 0
        detail_old = deepcopy(detail)
        for i in range(4):
            detail[i].y += 1
            if not check_borders():
                for i in range(4):
                    field[detail_old[i].y][detail_old[i].x] = color
                detail, color = next_detail, next_color
                next_detail, next_color = deepcopy(choice(details)), get_color()
                anim_limit = 2000
                break


    # поворачивать фигуру
    center = detail[0]
    detail_old = deepcopy(detail)
    if rotate:
        for i in range(4):
            x = detail[i].y - center.y
            y = detail[i].x - center.x
            detail[i].x = center.x - x
            detail[i].y = center.y + y
            if not check_borders():
                detail = deepcopy(detail_old)
                break

    # проверка линий
    line, lines = h - 1, 0
    for row in range(h - 1, -1, -1):
        count = 0
        for i in range(w):
            if field[row][i]:
                count += 1
            field[line][i] = field[row][i]
        if count < w:
            line -= 1
        else:
            anim_speed += 3
            lines += 1

    # подсчет очков
    score += scores[lines]

    # нарисовать клетку
    [pygame.draw.rect(game_on, (40, 40, 40), i_rect, 1) for i_rect in grid]

    # отрисовка детали
    for i in range(4):
        detail_rect.x = detail[i].x * tile
        detail_rect.y = detail[i].y * tile
        pygame.draw.rect(game_on, color, detail_rect)

    # отрисовка поля
    for y, raw in enumerate(field):
        for x, col in enumerate(raw):
            if col:
                detail_rect.x, detail_rect.y = x * tile, y * tile
                pygame.draw.rect(game_on, col, detail_rect)

    # отрисовка следующей детали
    for i in range(4):
        detail_rect.x = next_detail[i].x * tile + 380
        detail_rect.y = next_detail[i].y * tile + 185
        pygame.draw.rect(on, next_color, detail_rect)

    # draw titles
    on.blit(title_tetris, (485, 10))
    on.blit(title_score, (535, 780))
    on.blit(font.render(str(score), True, pygame.Color('orange')), (550, 840))
    on.blit(title_record, (525, 650))
    on.blit(font.render(record, True, pygame.Color('pink')), (550, 710))
    #on.blit(title_offlayt, (600, 903))



    # гейм овер
    for i in range(w):
        if field[0][i]:
            set_record(record, score)
            field = [[0 for i in range(w)] for i in range(h)]
            anim_count, anim_speed, anim_limit = 0, 60, 15000
            score = 0
            for i_rect in grid:
                pygame.draw.rect(game_on, get_color(), i_rect)
                on.blit(game_on, (20, 20))
                pygame.display.flip()
                clock.tick(200)

    pygame.display.flip()
    clock.tick(fps)



