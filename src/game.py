import pygame
from sys import exit

pygame.init()
pygame.display.set_caption("Python game")
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

game_active = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    if game_active:
        screen.fill((255, 255, 255))
    else:
        screen.fill((94, 129, 162))
    
    pygame.display.update()
    clock.tick(60)