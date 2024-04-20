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
        self.NAME = ("", False)
        self.PRIMARY_COLOR = "#644d37"
        self.input_box = InputBox(self.font, 370, 220, 140, 32)

        self.background_image = pygame.image.load(
            'graphics/intro.png').convert_alpha()
        self.background_image_rect = self.background_image.get_rect(
            center=(400, 300))

        self.theme_sound = pygame.mixer.Sound('audio/theme.mp3')
        self.theme_sound.set_volume(0.5)

        pygame.mixer.pre_init()
        pygame.mixer.init()
        self.channel_background = pygame.mixer.Channel(0)

        self.coin_sound = pygame.mixer.Sound('audio/coin.wav')
        self.fail_sound = pygame.mixer.Sound('audio/fail.wav')
        self.game_over_sound = pygame.mixer.Sound(
            'audio/game_over.wav')
        self.power_up_sound = pygame.mixer.Sound(
            'audio/power_up.wav')
        self.coin_sound.set_volume(0.1)
        self.fail_sound.set_volume(0.1)
        self.game_over_sound.set_volume(0.2)
        self.power_up_sound.set_volume(0.1)

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
                        self.channel_background.pause()
                        self.game_state = GameState.PAUSED
                        self.background_image = pygame.image.load(
                            'graphics/pause.png').convert_alpha()
                        self.background_image_rect = self.background_image.get_rect(
                            center=(400, 300))
                if event.type == self.obstacle_timer:
                    self.obstacle_group.add(
                        Obstacle(round(self.SPEED), self.life_lost))
            elif self.game_state == GameState.INTRO:
                self.NAME = self.input_box.handle_event(event)
                if self.NAME[1]:
                    self.game_state = GameState.PLAYING
                    self.obstacle_group.empty()
                    self.background_image = pygame.image.load(
                        'graphics/background.png').convert_alpha()
                    self.background_image_rect = self.background_image.get_rect(
                        center=(400, 300))
            elif self.game_state == GameState.PAUSED:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.channel_background.unpause()
                        self.game_state = GameState.PLAYING
                        self.background_image = pygame.image.load(
                            'graphics/background.png').convert_alpha()
                        self.background_image_rect = self.background_image.get_rect(
                            center=(400, 300))
            elif self.game_state == GameState.GAME_OVER:
                if event.type == pygame.KEYDOWN:
                    self.TIMERS = (1000, 1400)
                    self.SPEED = 5
                    self.reset_game()
                    self.background_image = pygame.image.load(
                        'graphics/intro.png').convert_alpha()
                    self.background_image_rect = self.background_image.get_rect(
                        center=(400, 300))

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
        self.channel_background.play(self.theme_sound, loops=-1)
        self.game_state = GameState.INTRO
        self.LIFE_COUNT = 3
        self.SCORE = 0
        self.SPEED = 5
        pygame.time.set_timer(self.obstacle_timer, randint(
            self.TIMERS[0], self.TIMERS[1]))

    def is_collision(self):
        collisions = pygame.sprite.spritecollide(
            self.bucket.sprite, self.obstacle_group, True)
        if not collisions:
            return
        for obstacle in collisions:
            if obstacle.type == 1:
                self.SCORE += 1
                self.coin_sound.play()
            elif obstacle.type == 2:
                self.life_lost()
            else:
                if self.LIFE_COUNT < 3:
                    self.LIFE_COUNT += 1
                    self.power_up_sound.play()
        if self.TIMERS[0] > 300 and self.TIMERS[1] > 400:
            self.TIMERS = (self.TIMERS[0] - 50, self.TIMERS[1] - 50)
        pygame.time.set_timer(self.obstacle_timer, randint(
            self.TIMERS[0], self.TIMERS[1]))
        if self.SPEED < 9:
            self.SPEED += 0.1

    def life_lost(self):
        self.LIFE_COUNT -= 1
        self.fail_sound.play()
        if self.LIFE_COUNT == 0:
            self.game_over_sound.play()
            self.channel_background.fadeout(1000)
            self.game_state = GameState.GAME_OVER
            self.background_image = pygame.image.load(
                'graphics/game_over.png').convert_alpha()
            self.background_image_rect = self.background_image.get_rect(
                center=(400, 300))

    def update(self):
        if self.game_state == GameState.PLAYING:
            self.SCREEN.blit(self.background_image, self.background_image_rect)
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
            self.SCREEN.blit(self.background_image, self.background_image_rect)
            self.input_box.update()
            self.input_box.draw(self.SCREEN)
        elif self.game_state == GameState.PAUSED:
            self.SCREEN.blit(self.background_image, self.background_image_rect)
            score_info = self.font.render(f'{self.SCORE}', False, (0, 0, 0))
            score_info_rect = score_info.get_rect(center=(400, 50))
            self.SCREEN.blit(score_info, score_info_rect)
            self.draw_life(650, 50)
        elif self.game_state == GameState.GAME_OVER:
            self.SCREEN.blit(self.background_image, self.background_image_rect)
            name = self.font.render(f"{self.NAME[0]}", False, self.PRIMARY_COLOR)
            name = pygame.transform.rotozoom(name, 0, 0.4)
            name_rect = name.get_rect(center=(710, 465))
            self.SCREEN.blit(name, name_rect)
            current_score = self.font.render(
                f"Your score: {self.SCORE}", False, self.PRIMARY_COLOR)
            current_score_rect = current_score.get_rect(center=(400, 190))
            self.SCREEN.blit(current_score, current_score_rect)

    def run(self):
        self.channel_background.play(self.theme_sound, loops=-1)
        while True:
            self.handle_events()
            self.update()
            pygame.display.update()
            self.CLOCK.tick(60)


game = Game()
game.run()
