from pygame import sprite, Surface
from random import randint


class Obstacle(sprite.Sprite):
    def __init__(self, speed, life_lost_func) -> None:
        super().__init__()

        self.speed = speed
        self.image = Surface((20, 20))
        self.image.fill((94, 129, 162))
        self.rect = self.image.get_rect(
            center=(randint(10, 790), randint(-300, -20)))
        self.life_lost_func = life_lost_func

    def move(self):
        self.rect.y += self.speed

    def is_outside(self):
        if (self.rect.top) >= 600:
            self.life_lost_func()
            self.kill()

    def update(self):
        self.move()
        self.is_outside()
