import pygame
from sys import exit
from random import randint

from bucket import Bucket
from obstacle import Obstacle
from inputbox import InputBox
from gamestate import GameState


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Python game")
        self.SCREEN = pygame.display.set_mode((800, 600))
        self.CLOCK = pygame.time.Clock()
        self.game_state = GameState.INTRO
        self.bucket = pygame.sprite.GroupSingle()
        self.bucket.add(Bucket())
        self.obstacle_group = pygame.sprite.Group()
        self.obstacle_timer = pygame.USEREVENT + 1
        self.font = pygame.font.Font('fonts/Pixeltype.ttf', 50)
        self.TIMERS = (1000, 1400)
        self.SPEED = 5
        self.SCORE = 0
        self.LIFE_COUNT = 3
        self.NAME = ""
        self.input_box = InputBox(self.font, 370, 400, 140, 32)

        pygame.time.set_timer(self.obstacle_timer, randint(
            self.TIMERS[0], self.TIMERS[1]))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if self.game_state == GameState.PLAYING:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game_state = GameState.PAUSED
                if event.type == self.obstacle_timer:
                    self.obstacle_group.add(
                        Obstacle(self.SPEED, self.life_lost))
                    pygame.time.set_timer(self.obstacle_timer, randint(
                        self.TIMERS[0], self.TIMERS[1]))
            elif self.game_state == GameState.INTRO:
                self.NAME = self.input_box.handle_event(event)
                if self.NAME[1]:
                    self.game_state = GameState.PLAYING
                    self.obstacle_group.empty()
            elif self.game_state == GameState.PAUSED:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game_state = GameState.PLAYING
            elif self.game_state == GameState.GAME_OVER:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.reset_game()

    def reset_game(self):
        self.game_state = GameState.INTRO
        self.LIFE_COUNT = 3
        self.SCORE = 0
        self.SPEED = 5
        pygame.time.set_timer(self.obstacle_timer, randint(
            self.TIMERS[0], self.TIMERS[1]))

    def is_collision(self):
        if pygame.sprite.spritecollide(self.bucket.sprite, self.obstacle_group, True):
            self.SCORE += 1

    def life_lost(self):
        self.LIFE_COUNT -= 1
        if self.LIFE_COUNT == 0:
            self.game_state = GameState.GAME_OVER

    def update(self):
        if self.game_state == GameState.PLAYING:
            self.SCREEN.fill((255, 255, 255))
            self.obstacle_group.draw(self.SCREEN)
            self.obstacle_group.update()
            self.bucket.draw(self.SCREEN)
            self.bucket.update()
            self.is_collision()
            score_info = self.font.render(f'{self.SCORE}', False, (0, 0, 0))
            score_info_rect = score_info.get_rect(center=(400, 80))
            self.SCREEN.blit(score_info, score_info_rect)
            life_info = self.font.render(
                f'{self.LIFE_COUNT}', False, (0, 0, 0))
            life_info_rect = life_info.get_rect(center=(600, 80))
            self.SCREEN.blit(life_info, life_info_rect)
        elif self.game_state == GameState.INTRO:
            self.SCREEN.fill((94, 129, 162))
            self.input_box.update()
            self.input_box.draw(self.SCREEN)
            bucket_image = pygame.image.load(
                'graphics/bucket.png').convert_alpha()
            bucket_image = pygame.transform.rotozoom(bucket_image, 0, 2)
            bucket_image_rect = bucket_image.get_rect(center=(400, 260))
            enter_your_name = self.font.render(
                'Enter your name', False, "White")
            enter_your_name_rect = enter_your_name.get_rect(center=(400, 130))
            self.SCREEN.blit(bucket_image, bucket_image_rect)
            self.SCREEN.blit(enter_your_name, enter_your_name_rect)
        elif self.game_state == GameState.PAUSED:
            current_score = self.font.render(
                f"Your score: {self.SCORE}", False, "White")
            current_score_rect = current_score.get_rect(center=(400, 250))
            self.SCREEN.fill((94, 129, 162))
            pause = self.font.render("Pause", False, "White")
            pause_rect = pause.get_rect(center=(400, 200))
            self.SCREEN.blit(pause, pause_rect)
            self.SCREEN.blit(current_score, current_score_rect)
        elif self.game_state == GameState.GAME_OVER:
            current_score = self.font.render(
                f"Your score: {self.SCORE}", False, "White")
            current_score_rect = current_score.get_rect(center=(400, 250))
            self.SCREEN.fill((94, 129, 162))
            you_lost = self.font.render("You lost", False, "White")
            you_lost_rect = you_lost.get_rect(center=(400, 200))
            self.SCREEN.blit(you_lost, you_lost_rect)
            self.SCREEN.blit(current_score, current_score_rect)

    def run(self):
        while True:
            self.handle_events()
            self.update()
            pygame.display.update()
            self.CLOCK.tick(60)


game = Game()
game.run()
