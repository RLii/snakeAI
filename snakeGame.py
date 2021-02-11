import pygame
import random
import NeuralNetwork
import numpy as np

def show_score(length, DISPLAY, font_style):
    DISPLAY.blit(font_style.render("Score: " + str(length-1), True, (255, 255, 255)), [0, 0])

def show_generation(generation, DISPLAY, font_style):
    DISPLAY.blit(font_style.render("Generation: " + str(generation), True, (255, 255, 255)), [600, 545])

def show_specieNum(specieNum, DISPLAY, font_style):
    DISPLAY.blit(font_style.render("SpeciesNum: " + str(specieNum), True, (255, 255, 255)), [600, 575])

def check_collision(x, y, list):
    for i in list:
        if x==i[0] and y == i[1]:
            return True
    return False

def draw_snake(length, list, DISPLAY, white):
    for x in list:
        pygame.draw.rect(DISPLAY, white, [x[0], x[1], length, length], 2)


def message(msg, color, DISPLAY, font_style):
    mesg = font_style.render(msg, True, color)
    DISPLAY.blit(mesg, [200, 150])


#NEURAL NETWORK Helpers
def getAppleQuadrant(foodX, foodY, x1, y1):
    list = [0] * 4
    if x1 <= foodX and y1 <= foodY:
        list[0] = 1
    elif x1 > foodX and y1 <= foodY:
        list[1] = 1
    elif x1 <= foodX and y1 > foodY:
        list[2] = 1
    elif x1 > foodX and y1 > foodY:
        list[3] = 1
    return list

def getHeadDirection(x1_change, y1_change):
    list = [0] * 4
    if x1_change > 0:
        list[0] = 1
    elif x1_change < 0:
        list[1] = 1
    elif y1_change > 0:
        list[2] = 1
    elif y1_change < 0:
        list[3] = 1
    return list

def getTailDirection(snake_list):
    list = [0] * 4
    if snake_list[0][0] - snake_list[1][0] > 0:
        list[0] = 1
    elif snake_list[0][0] - snake_list[1][0] < 0:
        list[1] = 1
    elif snake_list[0][1] - snake_list[1][1] > 0:
        list[2] = 1
    elif snake_list[0][1] - snake_list[1][1] < 0:
        list[3] = 1
    return list


def getSnakeVisuals(x1, y1, snake_list, DISPLAY_width, DISPLAY_height):
    xVision = [-1] * 2
    yVision = [-1] * 2
    for i in range(len(snake_list)):
        if snake_list[len(snake_list) - 1 - i][0] == x1 and xVision[0] == -1 or xVision[1] == -1:
            if snake_list[len(snake_list) - 1 - i][1] <= y1 and yVision[0] == -1:
                yVision[0] = (y1 - snake_list[len(snake_list) - 1 - i][1]) / 20 - 1
            elif snake_list[len(snake_list) - 1 - i][1] > y1 and yVision[1] == -1:
                yVision[1] = (snake_list[len(snake_list) - 1 - i][1] - y1) / 20 - 1

        if snake_list[len(snake_list) - 1 - i][1] == y1 and yVision[0] == -1 or yVision[1] == -1:
            if snake_list[len(snake_list) - 1 - i][0] <= x1 and xVision[0] == -1:
                xVision[0] = (x1 - snake_list[len(snake_list) - 1 - i][0]) / 20 - 1
            elif snake_list[len(snake_list) - 1 - i][0] > x1 and xVision[1] == -1:
                xVision[1] = (snake_list[len(snake_list) - 1 - i][0] - x1) / 20 - 1
    if xVision[0] == -1:
        xVision[0] = x1/20
    if xVision[1] == -1:
        xVision[1] = (DISPLAY_width - x1) / 20 - 1
    if yVision[0] == -1:
        yVision[0] = y1/20
    if yVision[1] == -1:
        yVision[1] = (DISPLAY_height - y1) / 20 - 1
    return xVision + yVision


def getFitness(time_alive, apples):
    return time_alive + (np.power(1.6, apples) + np.power(apples, 1.9) * 30) - (np.power(apples, 1.2) * np.power(time_alive*.25, 1.3))


def gameLoop(NeuralNets, generationNumber = "NA"):
    pygame.init()
    DISPLAY = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Snake!')

    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)

    clock = pygame.time.Clock()
    speed = 75

    DISPLAY_width = 800
    DISPLAY_height = 600
    font_style = pygame.font.SysFont(None, 30)

    evolution_results = []
    for i in range(len(NeuralNets)):
        x1 = 400
        y1 = 300

        x1_change = 20
        y1_change = 0

        block_movement = 20

        alive = True
        game_close = False

        snake_list = [[320, 300], [340, 300], [360, 300], [380, 300], [400, 300]]
        snake_length = 5

        foodX = random.randrange(0, DISPLAY_width - block_movement, block_movement)
        foodY = random.randrange(0, DISPLAY_height - block_movement, block_movement)

        alive_multiplier = 1
        alive = True
        nn = NeuralNets[i]

        while alive:
            # Human Controls
            #while not alive:
            #    DISPLAY.fill(black)
            #    message("Game Over, Press q to quit, r to restart", white, DISPLAY, font_style)
            #    pygame.display.update()
            #    for event in pygame.event.get():
            #        if event.type == pygame.KEYDOWN:
            #            if event.key == pygame.K_q:
            #                game_close = True
            #                alive = True
            #            if event.key == pygame.K_r:
            #                gameLoop()


            #Controls
            #for event in pygame.event.get():
            #    if event.type == pygame.QUIT:
            #        alive = False
            #    if event.type == pygame.KEYDOWN:
            #        if event.key == pygame.K_LEFT:
            #           x1_change = -block_movement
            #           y1_change = 0
            #       elif event.key == pygame.K_RIGHT:
            #           x1_change = block_movement
            #           y1_change = 0
            #       elif event.key == pygame.K_DOWN:
            #           x1_change = 0
            #           y1_change = block_movement
            #       elif event.key == pygame.K_UP:
            #           x1_change = 0
            #           y1_change = -block_movement

            # NeuralNet Controls
            params = getSnakeVisuals(x1, y1, snake_list, DISPLAY_width, DISPLAY_height) + getAppleQuadrant(foodX, foodY, x1, y1) + getHeadDirection(x1_change, y1_change) + getTailDirection(snake_list)
            nn.forward_propagate(params)
            movement = nn.getOutput()
            if movement[0] == 1:
                x1_change = -block_movement
                y1_change = 0
            elif movement[1] == 1:
                x1_change = block_movement
                y1_change = 0
            elif movement[2] == 1:
                x1_change = 0
                y1_change = block_movement
            elif movement[3] == 1:
                x1_change = 0
                y1_change = -block_movement

            x1 += x1_change
            y1 += y1_change

            if check_collision(x1, y1, snake_list):
                alive = False
                list = []
                list.append(getFitness(alive_multiplier, snake_length-5))
                list.append(nn)
                evolution_results.append(list)

            if x1 >= DISPLAY_width or y1 >= DISPLAY_height or x1 < 0 or y1 < 0:
                alive = False
                list = []
                list.append(getFitness(alive_multiplier, snake_length-5))
                list.append(nn)
                evolution_results.append(list)

            DISPLAY.fill(black)

            snake_head = [x1, y1]
            snake_list.append(snake_head)
            if len(snake_list) > snake_length:
                del snake_list[0]

            show_generation(generationNumber, DISPLAY, font_style)
            show_score(snake_length, DISPLAY, font_style)
            show_specieNum(i+1, DISPLAY, font_style)
            pygame.draw.rect(DISPLAY, red, [foodX, foodY, block_movement, block_movement])

            draw_snake(block_movement, snake_list, DISPLAY, white)

            pygame.display.update()
            if x1 == foodX and y1 == foodY:
                foodX = random.randrange(0, DISPLAY_width - block_movement, block_movement)
                foodY = random.randrange(0, DISPLAY_height - block_movement, block_movement)
                snake_length += 1
            alive_multiplier = alive_multiplier + 1

            if alive_multiplier > 15000:
                alive = False

            clock.tick(speed)


    pygame.quit()
    return evolution_results


