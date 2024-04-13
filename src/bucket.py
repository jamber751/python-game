from pygame import sprite, image, mouse


class Bucket(sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()

        self.image = image.load('graphics/bucket.png')
        self.rect = self.image.get_rect(midbottom=(400, 600))

    def user_input(self):
        mouse_pos = mouse.get_pos()
        self.rect.centerx = mouse_pos[0]

    def update(self):
        self.user_input()
