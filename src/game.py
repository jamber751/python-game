import pygame
from sys import exit
from random import randint

from bucket import Bucket
from obstacle import Obstacle
from inputbox import InputBox


def is_collision(score):
    if pygame.sprite.spritecollide(bucket.sprite, obstacle_group, True):
        return score + 1
    return score


def life_lost():
    global LIFE_COUNT
    global GAME_STATE
    LIFE_COUNT -= 1
    if LIFE_COUNT == 0:
        GAME_STATE = 3


pygame.init()
pygame.display.set_caption("Python game")
SCREEN = pygame.display.set_mode((800, 600))
CLOCK = pygame.time.Clock()

game_active = False

bucket = pygame.sprite.GroupSingle()
bucket.add(Bucket())
obstacle_group = pygame.sprite.Group()

obstacle_timer = pygame.USEREVENT + 1

font = pygame.font.Font('fonts/Pixeltype.ttf', 50)

# Intro
bucket_image = pygame.image.load('graphics/bucket.png').convert_alpha()
bucket_image = pygame.transform.rotozoom(bucket_image, 0, 2)
bucket_image_rect = bucket_image.get_rect(center=(400, 260))
eter_your_name = font.render('Enter your name', False, "White")
eter_your_name_rect = eter_your_name.get_rect(center=(400, 130))
input_box = InputBox(font, 370, 400, 140, 32)


TIMERS = (1000, 1400)
SPEED = 5
SCORE = 0
LIFE_COUNT = 3
NAME = ""

GAME_STATE = 0

pygame.time.set_timer(obstacle_timer, randint(TIMERS[0], TIMERS[1]))
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if GAME_STATE == 1:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    GAME_STATE = 2
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(SPEED, life_lost))
                pygame.time.set_timer(
                    obstacle_timer, randint(TIMERS[0], TIMERS[1]))
        elif GAME_STATE == 0:
            NAME = input_box.handle_event(event)
            if NAME[1]:
                GAME_STATE = 1
                obstacle_group.empty()
        elif GAME_STATE == 2:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    GAME_STATE = 1
        elif GAME_STATE == 3:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    GAME_STATE = 0
                    LIFE_COUNT = 3
                    SCORE = 0
                    SPEED = 5
                    pygame.time.set_timer(
                        obstacle_timer, randint(TIMERS[0], TIMERS[1]))

    if GAME_STATE == 1:
        SCREEN.fill((255, 255, 255))

        obstacle_group.draw(SCREEN)
        obstacle_group.update()

        bucket.draw(SCREEN)
        bucket.update()

        SCORE = is_collision(SCORE)

        score_info = font.render(f'{SCORE}', False, (0, 0, 0))
        score_info_rect = score_info.get_rect(center=(400, 80))
        SCREEN.blit(score_info, score_info_rect)

        life_info = font.render(f'{LIFE_COUNT}', False, (0, 0, 0))
        life_info_rect = life_info.get_rect(center=(600, 80))
        SCREEN.blit(life_info, life_info_rect)
    elif GAME_STATE == 0:

        SCREEN.fill((94, 129, 162))
        input_box.update()
        input_box.draw(SCREEN)
        SCREEN.blit(bucket_image, bucket_image_rect)
        SCREEN.blit(eter_your_name, eter_your_name_rect)

    elif GAME_STATE == 2:
        SCREEN.fill((255, 255, 255))
    elif GAME_STATE == 3:
        SCREEN.fill((0, 0, 0))

    pygame.display.update()
    CLOCK.tick(60)
