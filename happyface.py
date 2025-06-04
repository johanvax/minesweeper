import pygame as pg

class HappyFace(pg.sprite.Sprite):
    def __init__(self, x_pos, y_pos, callback, happyface_image):
        super().__init__()

        self.tile_size = 32

        self.callback = callback

        self.image = happyface_image

        self.x_pos = x_pos
        self.y_pos = y_pos

        self.rect = pg.Rect(x_pos, y_pos, self.tile_size, self.tile_size)

    def update(self, events):
        for event in events:
            if event.type == pg.MOUSEBUTTONUP:
                if self.rect.collidepoint(event.pos):
                    if event.button == 1:
                        self.callback()
