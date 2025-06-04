import pygame as pg

class Tile(pg.sprite.Sprite):
    def __init__(self, value, x_pos, y_pos, size, padding, callback, path): # -1 is bomb, then we have 0-8
        super().__init__()

        self.tile_size = size
        self.padding = padding

        self.path = path
        self.callback = callback

        self.image = pg.image.load(f'{path}images/unflipped-tile.png')

        self.x_pos = x_pos
        self.y_pos = y_pos

        pixel_x = x_pos * (self.tile_size + self.padding)
        pixel_y = y_pos * (self.tile_size + self.padding)
        self.rect = pg.Rect(pixel_x, pixel_y, size, size)

        self.value = value
        self.flipped = False
        self.flagged = False

    def update(self, events):
        for event in events:
            if event.type == pg.MOUSEBUTTONUP:
                if self.rect.collidepoint(event.pos):
                    if event.button == 1: # Left click
                        self.callback(self, True)
                    elif event.button == 3: # Right click
                        self.callback(self, False)
