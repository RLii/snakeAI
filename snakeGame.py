import pygame
import random

pygame.init()
DISPLAY = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Snake!')

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)


clock = pygame.time.Clock()
speed = 15

DISPLAY_width = 800
DISPLAY_height = 600
font_style = pygame.font.SysFont(None, 30)


def show_score(length):
    DISPLAY.blit(font_style.render("Score: " + str(length-1), True, (255, 255, 255)), [0, 0])


def check_collision(x, y, list):
    for i in list:
        if x==i[0] and y == i[1]:
            return True
    return False

def draw_snake(length, list):
    for x in list:
        pygame.draw.rect(DISPLAY, white, [x[0], x[1], length, length], 2)


def message(msg, color):
    mesg = font_style.render(msg, True, color)
    DISPLAY.blit(mesg, [200, 150])


def gameLoop():
    x1 = 400
    y1 = 300

    x1_change = 20
    y1_change = 0

    block_movement = 20

    alive = True
    game_close = False

    snake_list = []
    snake_length = 1

    foodX = random.randrange(0, DISPLAY_width - block_movement, block_movement)
    foodY = random.randrange(0, DISPLAY_height - block_movement, block_movement)

    while not game_close:
        while not alive:
            DISPLAY.fill(black)
            message("Game Over, Press q to quit, r to restart", white)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_close = True
                        alive = True
                    if event.key == pygame.K_r:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                alive = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -block_movement
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = block_movement
                    y1_change = 0
                elif event.key == pygame.K_DOWN:
                    x1_change = 0
                    y1_change = block_movement
                elif event.key == pygame.K_UP:
                    x1_change = 0
                    y1_change = -block_movement
        x1 += x1_change
        y1 += y1_change

        if check_collision(x1, y1, snake_list):
            alive = False

        if x1 > DISPLAY_width or y1 > DISPLAY_height or x1 < 0 or y1 < 0:
            alive = False

        DISPLAY.fill(black)

        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        show_score(snake_length)
        pygame.draw.rect(DISPLAY, red, [foodX, foodY, block_movement, block_movement])

        draw_snake(block_movement,snake_list)

        pygame.display.update()

        if x1 == foodX and y1 == foodY:
            foodX = random.randrange(0, DISPLAY_width - block_movement, block_movement)
            foodY = random.randrange(0, DISPLAY_height - block_movement, block_movement)
            snake_length += 1
        clock.tick(speed)

    pygame.quit()
    quit()


gameLoop()
