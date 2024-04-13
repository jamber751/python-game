import pygame
from sys import exit

from bucket import Bucket

pygame.init()
pygame.display.set_caption("Python game")
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

game_active = False

bucket = pygame.sprite.GroupSingle()
bucket.add(Bucket())

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_active = False
        else:
            if event.type == pygame.KEYDOWN:
                game_active = True

    if game_active:
        screen.fill((255, 255, 255))

        bucket.draw(screen)
        bucket.update()

    else:
        screen.fill((94, 129, 162))

    pygame.display.update()
    clock.tick(60)