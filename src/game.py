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
        self.TIMERS = (1000, 1200)
        self.SPEED = 5
        self.SCORE = 0
        self.LIFE_COUNT = 3
        self.NAME = ""
        self.PRIMARY_COLOR = "#644d37"
        self.input_box = InputBox(self.font, 370, 220, 140, 32)

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
                    self.TIMERS = (1000, 1400)
                    self.reset_game()

    def draw_life(self, x, y):
        if self.LIFE_COUNT == 3:
            life_image = pygame.image.load(
                'graphics/life3.png').convert_alpha()
        elif self.LIFE_COUNT == 2:
            life_image = pygame.image.load(
                'graphics/life2.png').convert_alpha()
        elif self.LIFE_COUNT == 1:
            life_image = pygame.image.load(
                'graphics/life1.png').convert_alpha()
        else:
            life_image = pygame.image.load(
                'graphics/life0.png').convert_alpha()

        life_image = pygame.transform.rotozoom(life_image, 0, 0.3)
        life_image_rect = life_image.get_rect(center=(x, y))
        self.SCREEN.blit(life_image, life_image_rect)

    def reset_game(self):
        self.game_state = GameState.INTRO
        self.LIFE_COUNT = 3
        self.SCORE = 0
        self.SPEED = 5
        pygame.time.set_timer(self.obstacle_timer, randint(
            self.TIMERS[0], self.TIMERS[1]))

    def is_collision(self):
        for obstacle in pygame.sprite.spritecollide(self.bucket.sprite, self.obstacle_group, True):
            if obstacle.type == 1:
                self.SCORE += 1
            elif obstacle.type == 2:
                self.life_lost()
            else:
                if self.LIFE_COUNT < 3:
                    self.LIFE_COUNT += 1
            if self.TIMERS[0] > 300 and self.TIMERS[1] > 400:
                self.TIMERS = (self.TIMERS[0] - 50, self.TIMERS[1] - 50)
            pygame.time.set_timer(self.obstacle_timer, randint(
                self.TIMERS[0], self.TIMERS[1]))

    def life_lost(self):
        self.LIFE_COUNT -= 1
        if self.LIFE_COUNT == 0:
            self.game_state = GameState.GAME_OVER

    def update(self):
        if self.game_state == GameState.PLAYING:
            background_image = pygame.image.load(
                'graphics/background.png').convert_alpha()
            background_image_rect = background_image.get_rect(
                center=(400, 300))
            self.SCREEN.blit(background_image, background_image_rect)
            self.obstacle_group.draw(self.SCREEN)
            self.obstacle_group.update()
            self.bucket.draw(self.SCREEN)
            self.bucket.update()
            self.is_collision()
            score_info = self.font.render(f'{self.SCORE}', False, (0, 0, 0))
            score_info_rect = score_info.get_rect(center=(400, 50))
            self.SCREEN.blit(score_info, score_info_rect)
            self.draw_life(650, 50)
        elif self.game_state == GameState.INTRO:
            background_image = pygame.image.load(
                'graphics/intro.png').convert_alpha()
            background_image_rect = background_image.get_rect(
                center=(400, 300))
            self.SCREEN.blit(background_image, background_image_rect)
            self.input_box.update()
            self.input_box.draw(self.SCREEN)
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
            game_over_backgroud = pygame.image.load(
                'graphics/game_over.png').convert_alpha()
            game_over_backgroud_rect = game_over_backgroud.get_rect(
                center=(400, 300))
            self.SCREEN.blit(game_over_backgroud, game_over_backgroud_rect)

            current_score = self.font.render(
                f"Your score: {self.SCORE}", False, self.PRIMARY_COLOR)
            current_score_rect = current_score.get_rect(center=(400, 190))
            self.SCREEN.blit(current_score, current_score_rect)

    def run(self):
        while True:
            self.handle_events()
            self.update()
            pygame.display.update()
            self.CLOCK.tick(60)


game = Game()
game.run()
