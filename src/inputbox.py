from pygame import draw, Color, Rect, KEYDOWN, K_BACKSPACE, K_RETURN

COLOR_INACTIVE = Color('black')
COLOR_ACTIVE = Color('white')


class InputBox:
    def __init__(self, font, x, y, w, h, text=''):
        self.font = font
        self.rect = Rect(x, y, w, h)
        self.rect.centerx = x
        self.rect.centery = y
        self.color = COLOR_ACTIVE
        self.text = text
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = True

    def handle_event(self, event):
        if event.type == KEYDOWN:
            if self.active:
                if event.key == K_RETURN:
                    if self.text != "":
                        return self.text, True
                elif event.key == K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = self.font.render(
                    self.text, True, self.color)
        return self.text, False

    def update(self):
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        draw.rect(screen, self.color, self.rect, 2)
