from pygame import sprite, image, transform
from random import randint


class Obstacle(sprite.Sprite):
    def __init__(self, speed, life_lost_func) -> None:
        super().__init__()
        mushrooms_img = ['graphics/mushroom_common.png', 'graphics/mushroom_common2.png',
                         'graphics/mushroom_red.png', 'graphics/mushroom_purple.png']
        type = randint(1, 100)

        if type <= 65:
            self.type = 1
            self.image = image.load(
                mushrooms_img[randint(0, 1)]).convert_alpha()
        elif type <= 97:
            self.type = 2
            self.image = image.load(mushrooms_img[2]).convert_alpha()
        else:
            self.type = 3
            self.image = image.load(mushrooms_img[3]).convert_alpha()

        self.speed = speed
        self.image = transform.rotozoom(self.image, 0, 0.7)
        self.rect = self.image.get_rect(
            center=(randint(10, 790), randint(-300, -20)))
        self.life_lost_func = life_lost_func

    def move(self):
        self.rect.y += self.speed

    def is_outside(self):
        if (self.rect.top) >= 600:
            if self.type != 2:
                self.life_lost_func()
            self.kill()

    def update(self):
        self.move()
        self.is_outside()
